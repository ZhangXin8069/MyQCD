"""SU(3) 颜色代数与 QCD 颜色因子审计。

本模块为算符构建提供精确的 Gell-Mann 基、结构常数、对称常数、Casimir
不变量和颜色 Fierz 恒等式。所有对象是 SymPy 精确值，不依赖数值线性代数。

约定：

* ``T^a = lambda^a / 2``，``a = 1..8``；
* ``Tr[T^a T^b] = delta^{ab} / 2``；
* ``[T^a, T^b] = i f^{abc} T^c``；
* ``{T^a, T^b} = delta^{ab} / 3 + d^{abc} T^c``。

这些约定与格点 QCD 算符中常用的颜色归一化一致；本模块不证明具体系综或
数值张量收缩已经通过。
"""

from __future__ import annotations

from functools import lru_cache
from typing import Tuple

import sympy as sp

N_COLORS = 3
N_GENERATORS = 8


def gell_mann_matrices() -> Tuple[sp.Matrix, ...]:
    """返回八个标准 Gell-Mann 矩阵。"""

    i = sp.I
    return (
        sp.Matrix([[0, 1, 0], [1, 0, 0], [0, 0, 0]]),
        sp.Matrix([[0, -i, 0], [i, 0, 0], [0, 0, 0]]),
        sp.Matrix([[1, 0, 0], [0, -1, 0], [0, 0, 0]]),
        sp.Matrix([[0, 0, 1], [0, 0, 0], [1, 0, 0]]),
        sp.Matrix([[0, 0, -i], [0, 0, 0], [i, 0, 0]]),
        sp.Matrix([[0, 0, 0], [0, 0, 1], [0, 1, 0]]),
        sp.Matrix([[0, 0, 0], [0, 0, -i], [0, i, 0]]),
        sp.Matrix(
            [
                [1, 0, 0],
                [0, 1, 0],
                [0, 0, -2],
            ]
        )
        / sp.sqrt(3),
    )


def generators() -> Tuple[sp.Matrix, ...]:
    """返回 ``T^a = lambda^a / 2``。"""

    return tuple(matrix / 2 for matrix in gell_mann_matrices())


def _validate_generator_index(index: int, name: str = "generator") -> None:
    if (
        not isinstance(index, int)
        or isinstance(index, bool)
        or not 1 <= index <= N_GENERATORS
    ):
        raise ValueError(f"{name} index must be an int in 1..8")


@lru_cache(maxsize=1)
def structure_constants() -> Tuple[Tuple[Tuple[sp.Expr, ...], ...], ...]:
    """返回完全反对称结构常数 ``f^{abc}``（8×8×8）。"""

    matrices = generators()
    values = []
    for a in range(N_GENERATORS):
        plane = []
        for b in range(N_GENERATORS):
            row = []
            commutator = sp.expand(matrices[a] * matrices[b] - matrices[b] * matrices[a])
            for c in range(N_GENERATORS):
                coefficient = sp.simplify(
                    -2 * sp.I * sp.trace(commutator * matrices[c])
                )
                row.append(sp.nsimplify(coefficient))
            plane.append(tuple(row))
        values.append(tuple(plane))
    return tuple(values)


@lru_cache(maxsize=1)
def symmetric_constants() -> Tuple[Tuple[Tuple[sp.Expr, ...], ...], ...]:
    """返回完全对称常数 ``d^{abc}``（8×8×8）。"""

    matrices = generators()
    values = []
    for a in range(N_GENERATORS):
        plane = []
        for b in range(N_GENERATORS):
            row = []
            anticommutator = sp.expand(matrices[a] * matrices[b] + matrices[b] * matrices[a])
            for c in range(N_GENERATORS):
                coefficient = sp.simplify(2 * sp.trace(anticommutator * matrices[c]))
                row.append(sp.nsimplify(coefficient))
            plane.append(tuple(row))
        values.append(tuple(plane))
    return tuple(values)


def fundamental_trace(a: int, b: int) -> sp.Expr:
    """返回 ``Tr[T^a T^b] = delta^{ab}/2``。"""

    _validate_generator_index(a)
    _validate_generator_index(b)
    return sp.Rational(1, 2) if a == b else sp.Integer(0)


def adjoint_trace(a: int, b: int) -> sp.Expr:
    """返回 ``f^{acd} f^{bcd} = 3 delta^{ab}``。"""

    _validate_generator_index(a)
    _validate_generator_index(b)
    f = structure_constants()
    return sp.simplify(
        sum(f[a - 1][c - 1][d - 1] * f[b - 1][c - 1][d - 1] for c in range(1, 9) for d in range(1, 9))
    )


def casimir_fundamental() -> sp.Expr:
    """返回基本表示 Casimir ``C_F = 4/3``。"""

    matrices = generators()
    total = sum(
        (matrix * matrix for matrix in matrices),
        sp.zeros(N_COLORS),
    )
    return sp.simplify(total[0, 0])


def casimir_adjoint() -> sp.Expr:
    """返回伴随表示 Casimir ``C_A = 3``。"""

    return adjoint_trace(1, 1)


def color_fierz_tensor() -> Tuple[Tuple[Tuple[sp.Expr, ...], ...], ...]:
    """返回颜色 Fierz 恒等式的残差张量（ijk l 四指标压缩为 9×9）。

    恒等式为 ``sum_a T^a_ij T^a_kl = (1/2)(delta_il delta_kj
    - (1/3) delta_ij delta_kl)``。返回按 ``(i,j) x (k,l)`` 排列的残差。
    """

    matrices = generators()
    residual = []
    for i in range(N_COLORS):
        for j in range(N_COLORS):
            row = []
            for k in range(N_COLORS):
                for ell in range(N_COLORS):
                    left = sum(matrix[i, j] * matrix[k, ell] for matrix in matrices)
                    right = (
                        sp.KroneckerDelta(i, ell) * sp.KroneckerDelta(k, j)
                        - sp.Rational(1, N_COLORS)
                        * sp.KroneckerDelta(i, j)
                        * sp.KroneckerDelta(k, ell)
                    ) / 2
                    row.append(sp.simplify(left - right))
            residual.append(tuple(row))
    return tuple(residual)


def color_fierz_residual() -> sp.Expr:
    """返回颜色 Fierz 恒等式的最大残差；精确零表示通过。"""

    return sp.simplify(
        sum(
            sp.Abs(value)
            for row in color_fierz_tensor()
            for value in row
        )
    )


def quark_gluon_vertex(a: int) -> sp.Matrix:
    """返回夸克-胶子顶点的颜色因子 ``T^a``。"""

    _validate_generator_index(a)
    return sp.Matrix(generators()[a - 1])


def epsilon_tensor() -> sp.Array:
    """返回三色完全反对称张量 ``epsilon_{abc}``（Levi-Civita）。"""

    return sp.Array(
        [
            [
                [sp.LeviCivita(a, b, c) for c in range(N_COLORS)]
                for b in range(N_COLORS)
            ]
            for a in range(N_COLORS)
        ]
    )


__all__ = [
    "N_COLORS",
    "N_GENERATORS",
    "adjoint_trace",
    "casimir_adjoint",
    "casimir_fundamental",
    "color_fierz_residual",
    "color_fierz_tensor",
    "epsilon_tensor",
    "fundamental_trace",
    "gell_mann_matrices",
    "generators",
    "quark_gluon_vertex",
    "structure_constants",
    "symmetric_constants",
]
