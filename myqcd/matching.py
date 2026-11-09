"""树级匹配核、Fourier 前因子与 hybrid 开关的符号检查。"""

from __future__ import annotations

from typing import Tuple

import sympy as sp


def fourier_prefactor() -> sp.Expr:
    """返回一维 Fourier 变换前因子 ``1/pi``。"""

    return 1 / sp.pi


def tree_level_matching(operator_name: str) -> sp.Expr:
    """返回树级匹配系数（本层约定为 1）。"""

    if not operator_name.strip():
        raise ValueError("operator name must be nonempty")
    return sp.Integer(1)


def hybrid_switch(
    x: sp.Expr, x0: sp.Expr = sp.Rational(1, 2), width: sp.Expr = sp.Rational(1, 10)
) -> sp.Expr:
    """返回 logistic hybrid 开关。"""

    x = sp.sympify(x)
    x0 = sp.sympify(x0)
    width = sp.sympify(width)
    if sp.simplify(width) == 0:
        raise ValueError("width must be nonzero")
    return 1 / (1 + sp.exp(-(x - x0) / width))


def hybrid_continuity_residual(
    x0: sp.Expr = sp.Rational(1, 2), width: sp.Expr = sp.Rational(1, 10)
) -> sp.Expr:
    """返回开关在中点的 ``f(x0)-1/2``。"""

    return sp.simplify(hybrid_switch(x0, x0, width) - sp.Rational(1, 2))


def matching_residual(
    tree_value: sp.Expr, loop_value: sp.Expr, z_factor: sp.Expr
) -> sp.Expr:
    """返回 ``tree - Z * loop``。"""

    return sp.simplify(
        sp.sympify(tree_value) - sp.sympify(z_factor) * sp.sympify(loop_value)
    )


def matching_table(names: Tuple[str, ...] = ("S", "P", "V", "A", "T")) -> tuple[dict[str, object], ...]:
    """返回树级匹配表。"""

    return tuple(
        {
            "operator": name,
            "tree_matching": str(tree_level_matching(name)),
            "fourier_prefactor": str(fourier_prefactor()),
        }
        for name in names
    )


__all__ = [
    "fourier_prefactor",
    "hybrid_continuity_residual",
    "hybrid_switch",
    "matching_residual",
    "matching_table",
    "tree_level_matching",
]
