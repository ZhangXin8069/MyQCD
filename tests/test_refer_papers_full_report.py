from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "docs" / "build_refer_papers_full_report.py"
MANIFEST = ROOT / "docs" / "report_refer_papers_all_contents_20260830.manifest.tsv"
REPORT = ROOT / "docs" / "report_refer_papers_all_contents_20260830.tex"


def run_generator(*arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *arguments],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )


def test_source_audit_matches_all_indexed_chinese_papers() -> None:
    result = run_generator("--audit")

    assert result.returncode == 0, result.stdout + result.stderr
    assert "papers=50" in result.stdout
    assert "indexed_zh_pages=1175 actual_zh_pages=1175" in result.stdout
    assert "missing_source_pdf=0" in result.stdout
    assert "page_mismatches=0" in result.stdout


def test_generated_report_has_full_content_embedding_and_traceable_manifest() -> None:
    result = run_generator("--generate")

    assert result.returncode == 0, result.stdout + result.stderr
    assert MANIFEST.is_file()
    assert REPORT.is_file()

    with MANIFEST.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    assert len(rows) == 50
    assert len({row["paper_id"] for row in rows}) == 50
    assert all(row["actual_pages"] == row["indexed_zh_pages"] for row in rows)
    assert all(row["sha256"] for row in rows)

    content = REPORT.read_text(encoding="utf-8")
    assert r"\documentclass[UTF8,11pt,oneside]{ctexbook}" in content
    assert r"\begin{table}[htbp]" in content
    assert r"\includepdf[pages=1-" in content
    assert "明文内容" in content
    assert "TODO" not in content
    assert "TBD" not in content
