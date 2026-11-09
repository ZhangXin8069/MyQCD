"""通用 Dirac Fierz 变换（16 个双线性基）。

给定 ``(bar psi1 Gamma_A psi2)(bar psi3 Gamma_B psi4)``，本模块把它重排为

``sum_{C,D} F_AB^CD (bar psi1 Gamma_C psi4)(bar psi3 Gamma_D psi2)``。

系数由基展开精确计算：

``F_AB^CD = (1/4) [Gamma_C] in Gamma_A Gamma_D^T Gamma_B``。

基的 Gram 归一化从 :mod:`myqcd.gamma` 读取，因此 Euclidean 下
``sigma``/``gamma_mu gamma5`` 的 ``-4`` 对角不会引入符号错误。
"""

from __future__ import annotations

from functools import lru_cache
from typing import Iterable, Mapping, Sequence, Tuple

import sympy as sp

from . import gamma, operators

BASIS_NAMES: Tuple[str, ...] = tuple(operators.dirac_bilinear_structures())
_BASIS = dict(operators.dirac_bilinear_structures())


def basis_matrix(name: str) -> sp.Matrix:
    """返回双线性基名对应的 4x4 矩阵。"""

    if name not in _BASIS:
        raise ValueError(f"unknown Dirac basis element {name!r}")
    return sp.Matrix(_BASIS[name])


def dual_basis_matrix(name: str) -> sp.Matrix:
    """返回对偶基 ``Gamma^A = Gamma_A / g_A``。

    ``g_A = Tr[Gamma_A Gamma_A] / 4`` 在 Euclidean 基中为 ``+1`` 或
    ``-1``。使用对偶基后完备性写作
    ``sum_A Gamma_A[i,j] Gamma^A[k,l] = 4 delta_{i,l} delta_{k,j}``。
    """

    matrix = basis_matrix(name)
    gram = sp.simplify(gamma.dirac_trace(matrix * matrix) / 4)
    if gram == 0:
        raise ValueError(f"degenerate Dirac basis element {name!r}")
    return sp.Matrix(matrix / gram)


def expand_in_basis(matrix: sp.MatrixBase) -> dict[str, sp.Expr]:
    """把任意 4x4 矩阵精确展开到 16 个 Dirac 基上。"""

    matrix = sp.Matrix(matrix)
    if matrix.shape != (4, 4):
        raise ValueError("Fierz expansion expects a 4x4 matrix")
    coefficients: dict[str, sp.Expr] = {}
    for name in BASIS_NAMES:
        basis = _BASIS[name]
        denominator = gamma.dirac_trace(basis * basis)
        if sp.simplify(denominator) == 0:
            raise ValueError(f"degenerate Dirac basis element {name!r}")
        coefficients[name] = sp.simplify(
            gamma.dirac_trace(basis * matrix) / denominator
        )
    return coefficients


@lru_cache(maxsize=None)
def _fierz_terms(left_name: str, right_name: str) -> Tuple[Tuple[str, str, sp.Expr], ...]:
    left = basis_matrix(left_name)
    right = basis_matrix(right_name)
    terms: list[Tuple[str, str, sp.Expr]] = []
    for left_contraction in BASIS_NAMES:
        left_dual = dual_basis_matrix(left_contraction)
        for right_contraction in BASIS_NAMES:
            right_dual = dual_basis_matrix(right_contraction)
            # Project
            # Gamma_A[i,j] Gamma_B[k,l]
            # = sum_CD F_AB^CD Gamma_C[i,l] Gamma_D[k,j]
            # onto the transposed dual basis.  The index pairing is
            # (l,i) for C and (j,k) for D; solving the 256x256 system
            # confirms this reproduces the physical RHS coefficients.
            total = sp.Integer(0)
            for i in range(4):
                for j in range(4):
                    for k in range(4):
                        for l in range(4):
                            total += (
                                left[i, j]
                                * right[k, l]
                                * left_dual[l, i]
                                * right_dual[j, k]
                            )
            coefficient = sp.simplify(total / 16)
            if coefficient != 0:
                terms.append(
                    (
                        left_contraction,
                        right_contraction,
                        coefficient,
                    )
                )
    return tuple(terms)


def fierz_terms(
    left_name: str, right_name: str
) -> Tuple[Tuple[str, str, sp.Expr], ...]:
    """返回 Fierz 重排的非零项 ``(Gamma_C, Gamma_D, coefficient)``。"""

    if left_name not in _BASIS:
        raise ValueError(f"unknown Dirac basis element {left_name!r}")
    if right_name not in _BASIS:
        raise ValueError(f"unknown Dirac basis element {right_name!r}")
    return _fierz_terms(left_name, right_name)


def fierz_transform(
    left_name: str, right_name: str
) -> dict[Tuple[str, str], sp.Expr]:
    """返回以 ``(Gamma_C, Gamma_D)`` 为键的 Fierz 系数字典。"""

    return {
        (left_contraction, right_contraction): coefficient
        for left_contraction, right_contraction, coefficient
        in fierz_terms(left_name, right_name)
    }


def fierz_residual(
    left_name: str,
    right_name: str,
    spinors: Sequence[Sequence[complex]],
) -> complex:
    """用四个数值旋量检查一条 Fierz 恒等式的残差。

    ``spinors`` 必须包含四个四分量复旋量。返回
    ``LHS - RHS`` 的复残差；调用方负责选择随机旋量。
    """

    if len(spinors) != 4 or any(len(spinor) != 4 for spinor in spinors):
        raise ValueError("expected four four-component spinors")
    psi1, psi2, psi3, psi4 = [
        sp.Matrix(4, 1, lambda row, column: sp.sympify(spinor[row]))
        for spinor in spinors
    ]
    gamma4 = gamma.gamma(4)

    def bilinear(left: sp.Matrix, right: sp.Matrix, name: str) -> sp.Expr:
        bar = left.H * gamma4
        return sp.simplify((bar * basis_matrix(name) * right)[0, 0])

    lhs = bilinear(psi1, psi2, left_name) * bilinear(
        psi3, psi4, right_name
    )
    rhs = sp.Integer(0)
    for left_contraction, right_contraction, coefficient in fierz_terms(
        left_name, right_name
    ):
        rhs += coefficient * bilinear(
            psi1, psi4, left_contraction
        ) * bilinear(psi3, psi2, right_contraction)
    return complex(sp.N(sp.simplify(lhs - rhs)))


def fierz_table(
    names: Iterable[str] | None = None,
) -> dict[Tuple[str, str], dict[Tuple[str, str], sp.Expr]]:
    """返回若干 ``(A,B)`` 对的完整 Fierz 系数表。"""

    selected = tuple(BASIS_NAMES if names is None else names)
    for name in selected:
        if name not in _BASIS:
            raise ValueError(f"unknown Dirac basis element {name!r}")
    return {
        (left, right): fierz_transform(left, right)
        for left in selected
        for right in selected
    }


def common_identities() -> dict[str, Mapping[Tuple[str, str], sp.Expr]]:
    """返回文档常用的 Fierz 恒等式（命名便于引用）。"""

    return {
        "S-S": fierz_transform("S", "S"),
        "P-P": fierz_transform("P", "P"),
        "V1-V1": fierz_transform("V1", "V1"),
        "A1-A1": fierz_transform("A1", "A1"),
        "T12-T12": fierz_transform("T12", "T12"),
    }


__all__ = [
    "BASIS_NAMES",
    "basis_matrix",
    "common_identities",
    "dual_basis_matrix",
    "expand_in_basis",
    "fierz_residual",
    "fierz_table",
    "fierz_terms",
    "fierz_transform",
]
