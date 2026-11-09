"""Documentation and repository contracts that guard release drift."""

from __future__ import annotations

import re
import shutil
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

from myqcd import operators

ROOT = Path(__file__).resolve().parents[3]
DOCS = ROOT / "docs"
PAGES = (
    "overview",
    "tutorial",
    "usage",
    "operators",
    "operator-basis",
    "fierz",
    "lorentz",
    "gamma-traces",
    "color-algebra",
    "qcd-rules",
    "topology",
    "diagrams",
    "diagram-formats",
    "lattice-geometry",
    "statistics",
    "worked-examples",
    "install",
)
SVG_ASSETS = (
    "two_point_chain.svg",
    "three_gluon_triangle.svg",
    "quark_self_energy.svg",
    "sunset_two_loop.svg",
    "wick_pairing.svg",
)


def _blocks(path: Path) -> list[tuple[str, str]]:
    text = path.read_text(encoding="utf-8")
    return re.findall(r"```(\w+)\n(.*?)```", text, re.S)


def _toctree(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    body = re.search(
        r"\.\. toctree::\n(?:[ \t]*:[^\n]+\n)*\n((?:[ \t]+\S+\n)+)",
        text,
    )
    assert body is not None
    return [line.strip() for line in body.group(1).strip().splitlines()]


@pytest.mark.parametrize("page", PAGES)
def test_bilingual_code_blocks_are_byte_identical(page: str) -> None:
    assert _blocks(DOCS / "en" / f"{page}.md") == _blocks(
        DOCS / "zh" / f"{page}.md"
    )


def test_toctree_matches_pages_on_disk() -> None:
    en = _toctree(DOCS / "en" / "index.rst")
    zh = _toctree(DOCS / "zh" / "index.rst")
    assert en == zh
    assert set(en) == {path.stem for path in (DOCS / "en").glob("*.md")}
    assert set(zh) == {path.stem for path in (DOCS / "zh").glob("*.md")}


@pytest.mark.parametrize(
    "page",
    ("tutorial", "usage", "operators", "operator-basis", "fierz", "lorentz", "gamma-traces", "color-algebra", "qcd-rules", "topology", "diagrams", "diagram-formats", "lattice-geometry", "statistics", "worked-examples"),
)
def test_documentation_python_blocks_execute(page: str) -> None:
    namespace: dict[str, object] = {}
    blocks = [
        block for language, block in _blocks(DOCS / "en" / f"{page}.md")
        if language == "python"
    ]
    assert blocks
    for index, block in enumerate(blocks, 1):
        exec(compile(block, f"docs/en/{page}.md#{index}", "exec"), namespace)


def test_operator_table_matches_generated_values() -> None:
    text = (DOCS / "en" / "operators.md").read_text(encoding="utf-8")
    rows = re.findall(
        r"^\| `([A-Z0-9]+)` \| ([SPVAT]) \| ([+-]1) \| ([+-]1) "
        r"\| (\d+) \| ([0-9]+|—) \|$",
        text,
        re.M,
    )
    assert len(rows) == 16
    for name, label, parity, conjugation, dimension, index in rows:
        operator = operators.BilinearOperator(
            name=f"O_{name}",
            left_flavor="u",
            right_flavor="d",
            structure=name,
        )
        assert label == operator.label
        assert int(parity) == operator.parity_sign
        assert int(conjugation) == operator.charge_conjugation_sign
        assert int(dimension) == operator.mass_dimension
        expected = (
            "—"
            if operator.pyqcd_gamma_index is None
            else str(operator.pyqcd_gamma_index)
        )
        assert index == expected


@pytest.mark.parametrize("language", ("en", "zh"))
def test_diagram_assets_are_present_and_well_formed(language: str) -> None:
    for name in SVG_ASSETS:
        path = DOCS / language / "_static" / name
        assert path.is_file()
        root = ET.parse(path).getroot()
        assert root.tag.endswith("svg")


@pytest.mark.parametrize("language", ("en", "zh"))
def test_diagram_pages_reference_all_assets(language: str) -> None:
    text = (DOCS / language / "diagrams.md").read_text(encoding="utf-8")
    for name in SVG_ASSETS:
        assert f"_static/{name}" in text


@pytest.mark.parametrize("language", ("en", "zh"))
def test_docs_enable_latex_math(language: str) -> None:
    conf = (DOCS / language / "conf.py").read_text(encoding="utf-8")
    assert "sphinx.ext.mathjax" in conf
    assert "dollarmath" in conf
    operators_page = (DOCS / language / "operators.md").read_text(
        encoding="utf-8"
    )
    diagrams_page = (DOCS / language / "diagrams.md").read_text(
        encoding="utf-8"
    )
    assert "$" in operators_page
    assert "$" in diagrams_page


def test_packaging_and_readme_files_are_tracked() -> None:
    if shutil.which("git") is None:
        pytest.skip("git is not available")
    required = {
        "pyproject.toml",
        "MANIFEST.in",
        "README.md",
        "README.zh-CN.md",
        "myqcd/py.typed",
    }
    result = subprocess.run(
        ["git", "-C", str(ROOT), "ls-files", *sorted(required)],
        check=True,
        capture_output=True,
        text=True,
    )
    assert set(result.stdout.splitlines()) == required
