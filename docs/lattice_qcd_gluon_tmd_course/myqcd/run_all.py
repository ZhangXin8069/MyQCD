"""运行课程 myqcd 子目录中的全部 SymPy 教学例题。"""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Mapping, Sequence, Tuple


if __package__ in {None, ""}:
    COURSE_DIR = Path(__file__).resolve().parent.parent
    course_dir_text = str(COURSE_DIR)
    if course_dir_text in sys.path:
        sys.path.remove(course_dir_text)
    sys.path.insert(0, course_dir_text)
    from myqcd import all_examples  # type: ignore[no-redef]
else:
    from . import all_examples


EXPECTED_EXAMPLE_IDS: Tuple[str, ...] = (
    *(f"MYQCD-GQ-{index:02d}" for index in range(1, 7)),
    *(f"MYQCD-SP-{index:02d}" for index in range(1, 9)),
    *(f"MYQCD-RT-{index:02d}" for index in range(1, 13)),
)


def _nonblank_sequence(value: object) -> bool:
    return (
        isinstance(value, tuple)
        and bool(value)
        and all(isinstance(item, str) and bool(item.strip()) for item in value)
    )


def _validate_examples(examples: object) -> tuple:
    if not isinstance(examples, tuple):
        raise AssertionError("all_examples() 必须返回 tuple")
    ids = tuple(getattr(item, "example_id", None) for item in examples)
    if ids != EXPECTED_EXAMPLE_IDS:
        missing = sorted(set(EXPECTED_EXAMPLE_IDS) - set(ids))
        extra = sorted(set(ids) - set(EXPECTED_EXAMPLE_IDS), key=str)
        raise AssertionError(
            "教学例题必须按固定顺序精确为 26 个预期 ID："
            f"actual={len(ids)} missing={missing} extra={extra}"
        )
    for item in examples:
        example_id = item.example_id
        for field in ("title", "boundary"):
            value = getattr(item, field, None)
            if not isinstance(value, str) or not value.strip():
                raise AssertionError(f"{example_id}: {field} 必须是非空字符串")
        for field in ("course_refs", "assumptions", "source_refs"):
            if not _nonblank_sequence(getattr(item, field, None)):
                raise AssertionError(f"{example_id}: {field} 必须是非空字符串 tuple")
        checks = getattr(item, "checks", None)
        if not isinstance(checks, Mapping) or not checks:
            raise AssertionError(f"{example_id}: checks 必须是非空映射")
        if any(not isinstance(name, str) or not name.strip() for name in checks):
            raise AssertionError(f"{example_id}: checks 名称不得为空")
        if any(type(value) is not bool for value in checks.values()):
            raise AssertionError(f"{example_id}: checks 值必须是 bool")
        equations = getattr(item, "equations", None)
        if not isinstance(equations, Mapping) or not equations:
            raise AssertionError(f"{example_id}: equations 必须是非空映射")
        if any(
            not isinstance(name, str) or not name.strip() for name in equations
        ):
            raise AssertionError(f"{example_id}: equations 名称不得为空")
    return examples


def _write_json_atomic(path: Path, payload: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temporary = Path(handle.name)
            handle.write(
                (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode(
                    "utf-8"
                )
            )
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        temporary = None
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--json",
        type=Path,
        help="可选：把逐例公式、假设和边界写入指定 JSON 文件",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="只打印最终汇总和失败项",
    )
    args = parser.parse_args(argv)

    examples = _validate_examples(all_examples())

    failed = [item for item in examples if item.status != "verified"]
    if not args.quiet:
        for item in examples:
            passed = sum(item.checks.values())
            marker = "PASS" if item.status == "verified" else "FAIL"
            print(
                f"[{marker}] {item.example_id} {item.title} "
                f"({passed}/{len(item.checks)})"
            )
            if item.status != "verified":
                for name, ok in item.checks.items():
                    if not ok:
                        print(f"       failed: {name}")

    payload = {
        "schema": "lqcd-course-myqcd-examples-v1",
        "total": len(examples),
        "passed": len(examples) - len(failed),
        "records": [item.as_dict() for item in examples],
    }
    if args.json is not None:
        _write_json_atomic(args.json, payload)

    print(f"myqcd teaching examples: {len(examples) - len(failed)}/{len(examples)} passed")
    if failed:
        print("failed examples:", ", ".join(item.example_id for item in failed))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
