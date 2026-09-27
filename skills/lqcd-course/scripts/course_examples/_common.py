"""课程 SymPy 示例的公共数据结构与精确判零工具。"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence, Tuple

import sympy as sp


@dataclass(frozen=True)
class SymbolicExample:
    """一项可执行推导，以及它能够和不能够证明的内容。"""

    example_id: str
    title: str
    course_refs: Tuple[str, ...]
    equations: Mapping[str, Any]
    checks: Mapping[str, bool]
    assumptions: Tuple[str, ...]
    boundary: str
    source_refs: Tuple[str, ...]

    @property
    def status(self) -> str:
        return "verified" if self.checks and all(self.checks.values()) else "failed"

    def as_dict(self) -> Mapping[str, Any]:
        """转换为稳定、可写入 JSON 的教学记录。"""

        return {
            "example_id": self.example_id,
            "title": self.title,
            "course_refs": list(self.course_refs),
            "status": self.status,
            "checks": dict(self.checks),
            "assumptions": list(self.assumptions),
            "boundary": self.boundary,
            "source_refs": list(self.source_refs),
            "equations": {
                name: sp.sstr(value) for name, value in self.equations.items()
            },
        }


def is_zero(value: Any) -> bool:
    """将 SymPy 的精确等式判断收敛为普通布尔值。"""

    try:
        return bool(sp.simplify(value) == 0)
    except (TypeError, ValueError, NotImplementedError):
        return False


def matrix_is_zero(value: sp.MatrixBase) -> bool:
    """逐元检查有限维矩阵为零。"""

    return all(is_zero(entry) for entry in value)


def make_example(
    example_id: str,
    title: str,
    course_refs: Sequence[str],
    equations: Mapping[str, Any],
    checks: Mapping[str, object],
    assumptions: Sequence[str],
    boundary: str,
    source_refs: Sequence[str],
) -> SymbolicExample:
    """归一化记录，并拒绝没有检查项的“空验证”。"""

    normalized_checks = {name: bool(value) for name, value in checks.items()}
    if not normalized_checks:
        raise ValueError(f"{example_id}: 至少需要一个可执行检查")
    return SymbolicExample(
        example_id=example_id,
        title=title,
        course_refs=tuple(course_refs),
        equations=equations,
        checks=normalized_checks,
        assumptions=tuple(assumptions),
        boundary=boundary,
        source_refs=tuple(source_refs),
    )

