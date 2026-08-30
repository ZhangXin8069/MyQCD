"""命令行审计入口：核心 SymPy 检查 + 论文显示公式索引。"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict

from .derivations import run_core_checks
from .latex_inventory import scan_refer_papers, write_inventory


def build_audit_report(root: Path | str) -> Dict[str, Any]:
    root_path = Path(root).resolve()
    core = run_core_checks()
    inventory = scan_refer_papers(root_path)
    return {
        "status": "verified_core_with_unparsed_inventory"
        if core["status"] == "verified"
        else "failed",
        "core": core,
        "inventory": {
            "paper_count": inventory.paper_count,
            "source_file_count": inventory.source_file_count,
            "formula_count": inventory.formula_count,
            "unparsed_count": inventory.unparsed_count,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="MyQCD 工作区根目录",
    )
    parser.add_argument(
        "--inventory-json",
        type=Path,
        help="可选：将逐公式索引写入指定 JSON 文件",
    )
    args = parser.parse_args()

    report = build_audit_report(args.root)
    if args.inventory_json is not None:
        write_inventory(args.inventory_json, scan_refer_papers(args.root))
        report["inventory_json"] = str(args.inventory_json)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] != "failed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
