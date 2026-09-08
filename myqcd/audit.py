"""命令行审计入口：核心 SymPy 检查 + 论文显示公式索引。"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, Iterable, Sequence

from .derivations import run_core_checks
from .latex_inventory import (
    InventoryReport,
    scan_refer_papers as _scan_refer_papers,
    write_inventory,
)


class _AppendPaperIDSource(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        sources = getattr(namespace, "paper_id_sources", None)
        if sources is None:
            sources = []
            setattr(namespace, "paper_id_sources", sources)
        source_type = "paper_ids" if option_string == "--paper-id" else "paper_id_file"
        sources.append((source_type, values))


def _normalize_paper_id_inputs(paper_ids: Iterable[str] | str | None) -> tuple[str, ...]:
    if paper_ids is None:
        return ()
    if isinstance(paper_ids, str):
        paper_ids = (paper_ids,)

    normalized: list[str] = []
    seen: set[str] = set()
    for paper_id in paper_ids:
        for chunk in paper_id.split(","):
            candidate = chunk.strip()
            if candidate and candidate not in seen:
                seen.add(candidate)
                normalized.append(candidate)
    return tuple(normalized)


def _paper_ids_from_file(path: Path) -> tuple[str, ...]:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise ValueError(f"无法读取 paper id 文件 {path}: {exc}") from exc

    paper_ids: list[str] = []
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        paper_ids.append(stripped)
    return tuple(paper_ids)


def _merge_paper_ids(
    paper_ids: Iterable[str] | str | None = None,
    paper_id_files: Iterable[Path | str] | None = None,
) -> tuple[str, ...]:
    sources: list[tuple[str, Iterable[str] | str | Path]] = []
    if paper_ids is not None:
        sources.append(("paper_ids", paper_ids))
    if paper_id_files:
        for file_path in paper_id_files:
            sources.append(("paper_id_file", file_path))
    return _merge_paper_id_sources(sources)


def _merge_paper_id_sources(
    paper_id_sources: Sequence[tuple[str, Iterable[str] | str | Path]]
) -> tuple[str, ...]:
    merged: list[str] = []
    seen: set[str] = set()
    for source_type, source_value in paper_id_sources:
        if source_type == "paper_ids":
            candidates = _normalize_paper_id_inputs(source_value)
        elif source_type == "paper_id_file":
            candidates = _paper_ids_from_file(Path(source_value))
        else:
            raise ValueError(f"不支持的 paper id 来源: {source_type}")
        for candidate in candidates:
            if candidate not in seen:
                seen.add(candidate)
                merged.append(candidate)
    return tuple(merged)


def _cli_error_message(exc: ValueError) -> str:
    message = str(exc)
    prefix = "paper_ids 中存在未收录的论文编号: "
    if message.startswith(prefix):
        return "不存在的 paper id: " + message[len(prefix) :]
    return message


def scan_refer_papers(
    root: Path | str,
    paper_ids: Iterable[str] | str | None = None,
    paper_id_files: Iterable[Path | str] | None = None,
) -> InventoryReport:
    """扫描 refer/papers，并按 paper_id 过滤结果。"""

    root_path = Path(root).resolve()
    normalized_paper_ids = _merge_paper_ids(paper_ids=paper_ids, paper_id_files=paper_id_files)
    if not normalized_paper_ids:
        return _scan_refer_papers(root_path)
    return _scan_refer_papers(root_path, paper_ids=normalized_paper_ids)


def _unique_source_files(records) -> tuple[str, ...]:
    return tuple(dict.fromkeys(record.source_file for record in records))


def _build_audit_bundle(
    root: Path | str,
    paper_ids: Iterable[str] | str | None = None,
    paper_id_files: Iterable[Path | str] | None = None,
) -> tuple[Dict[str, Any], InventoryReport]:
    core = run_core_checks()
    requested_paper_ids = _merge_paper_ids(
        paper_ids=paper_ids,
        paper_id_files=paper_id_files,
    )
    inventory = scan_refer_papers(root, paper_ids=requested_paper_ids)
    paper_filter = {
        "enabled": bool(requested_paper_ids),
        "requested_paper_ids": list(requested_paper_ids),
        "requested_count": len(requested_paper_ids),
        "selected_paper_count": inventory.paper_count,
        "source_files": list(_unique_source_files(inventory.records)),
    }
    report = {
        "status": "verified_core_with_unparsed_inventory"
        if core["status"] == "verified"
        else "failed",
        "core": core,
        "paper_ids": list(requested_paper_ids),
        "paper_filter": paper_filter,
        "inventory": {
            "paper_count": inventory.paper_count,
            "source_file_count": inventory.source_file_count,
            "formula_count": inventory.formula_count,
            "unparsed_count": inventory.unparsed_count,
        },
    }
    return report, inventory


def build_audit_report(
    root: Path | str,
    paper_ids: Iterable[str] | str | None = None,
    paper_id_files: Iterable[Path | str] | None = None,
) -> Dict[str, Any]:
    report, _ = _build_audit_bundle(
        root,
        paper_ids=paper_ids,
        paper_id_files=paper_id_files,
    )
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.set_defaults(paper_id_sources=[])
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="MyQCD 工作区根目录",
    )
    parser.add_argument(
        "--paper-id",
        action=_AppendPaperIDSource,
        metavar="PAPER_ID",
        help="可重复指定，或用逗号分隔多个编号，例如 --paper-id P01 --paper-id P02 或 --paper-id P01,P02",
    )
    parser.add_argument(
        "--paper-id-file",
        action=_AppendPaperIDSource,
        type=Path,
        metavar="PATH",
        help="每行一个 paper id，支持空行和以 # 开头的注释",
    )
    parser.add_argument(
        "--inventory-json",
        type=Path,
        help="可选：将逐公式索引写入指定 JSON 文件",
    )
    args = parser.parse_args()

    try:
        requested_paper_ids = _merge_paper_id_sources(
            getattr(args, "paper_id_sources", ())
        )
        report, inventory = _build_audit_bundle(
            args.root,
            paper_ids=requested_paper_ids,
        )
    except ValueError as exc:
        parser.exit(2, f"error: {_cli_error_message(exc)}\n")
    if args.inventory_json is not None:
        write_inventory(args.inventory_json, inventory)
        report["inventory_json"] = str(args.inventory_json)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] != "failed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
