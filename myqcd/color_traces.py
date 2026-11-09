"""SU(3) 生成元迹、f/d 缩并与 Casimir 恒等式。"""

from __future__ import annotations

from typing import Tuple

import sympy as sp

from . import color


def trace_two(a: int, b: int) -> sp.Expr:
    """返回 ``Tr[T^a T^b] = delta^{ab}/2``。"""

    return color.fundamental_trace(a, b)


def trace_three(a: int, b: int, c: int) -> sp.Expr:
    """返回 ``Tr[T^a T^b T^c] = (d^{abc} + i f^{abc})/4``。"""

    for index in (a, b, c):
        color._validate_generator_index(index)
    f = color.structure_constants()
    d = color.symmetric_constants()
    return sp.simplify(
        (d[a - 1][b - 1][c - 1] + sp.I * f[a - 1][b - 1][c - 1]) / 4
    )


def trace_four(a: int, b: int, c: int, d: int) -> sp.Expr:
    """用显式 Gell-Mann 矩阵计算四生成元迹。"""

    for index in (a, b, c, d):
        color._validate_generator_index(index)
    generators = color.generators()
    return sp.simplify(
        sp.trace(
            generators[a - 1]
            * generators[b - 1]
            * generators[c - 1]
            * generators[d - 1]
        )
    )


def _validated_pair(a: int, b: int, c: int, d: int) -> None:
    for index in (a, b, c, d):
        color._validate_generator_index(index)


def f_contract(a: int, b: int, c: int, d: int) -> sp.Expr:
    """返回 ``sum_e f^{abe} f^{cde}``。"""

    _validated_pair(a, b, c, d)
    f = color.structure_constants()
    return sp.simplify(
        sum(
            f[a - 1][b - 1][e - 1] * f[c - 1][d - 1][e - 1]
            for e in range(1, 9)
        )
    )


def d_contract(a: int, b: int, c: int, d: int) -> sp.Expr:
    """返回 ``sum_e d^{abe} d^{cde}``。"""

    _validated_pair(a, b, c, d)
    symmetric = color.symmetric_constants()
    return sp.simplify(
        sum(
            symmetric[a - 1][b - 1][e - 1]
            * symmetric[c - 1][d - 1][e - 1]
            for e in range(1, 9)
        )
    )


def f_d_contract(a: int, b: int, c: int, d: int) -> sp.Expr:
    """返回 ``sum_e f^{abe} d^{cde}``。"""

    _validated_pair(a, b, c, d)
    structure = color.structure_constants()
    symmetric = color.symmetric_constants()
    return sp.simplify(
        sum(
            structure[a - 1][b - 1][e - 1]
            * symmetric[c - 1][d - 1][e - 1]
            for e in range(1, 9)
        )
    )


def jacobi_residual(a: int, b: int, c: int, d: int) -> sp.Expr:
    """返回 Jacobi 恒等式的残差（应为 0）。"""

    _validated_pair(a, b, c, d)
    return sp.simplify(
        f_contract(a, b, c, d)
        + f_contract(b, c, a, d)
        + f_contract(c, a, b, d)
    )


def casimir_generic(n: sp.Expr) -> dict[str, sp.Expr]:
    """返回 SU(N) 的 ``C_F``、``C_A`` 与 ``T_F``。"""

    n = sp.sympify(n)
    if sp.simplify(n - 1) <= 0:
        raise ValueError("SU(N) requires N > 1")
    return {
        "C_F": sp.simplify((n**2 - 1) / (2 * n)),
        "C_A": n,
        "T_F": sp.Rational(1, 2),
    }


def su3_casimirs() -> dict[str, sp.Expr]:
    """返回 SU(3) 的 Casimir 值。"""

    return {
        "C_F": color.casimir_fundamental(),
        "C_A": color.casimir_adjoint(),
        "T_F": color.fundamental_trace(1, 1),
    }


def trace_table() -> Tuple[dict[str, object], ...]:
    """返回常用 SU(3) 迹与缩并样本。"""

    samples = []
    for a, b, c, d in ((1, 2, 3, 4), (1, 4, 7, 8), (3, 3, 6, 7)):
        samples.append(
            {
                "indices": (a, b, c, d),
                "trace_three": str(trace_three(a, b, c)),
                "trace_four": str(trace_four(a, b, c, d)),
                "f_contract": str(f_contract(a, b, c, d)),
                "d_contract": str(d_contract(a, b, c, d)),
            }
        )
    return tuple(samples)


__all__ = [
    "casimir_generic",
    "d_contract",
    "f_contract",
    "f_d_contract",
    "jacobi_residual",
    "su3_casimirs",
    "trace_four",
    "trace_table",
    "trace_three",
    "trace_two",
]
