"""Euclidean Dirac gamma 代数与 PyQCD DeGrand--Rossi 基。

本模块独立实现格点 QCD 算符构建所需的有限维 gamma 代数，并与
``refer/git-rep/PyQCD/pyqcd/lattice/_gamma.py`` 的索引约定保持一致：

* ``gamma(0)`` 是单位矩阵哨兵，不是第五个 Euclidean gamma；
* ``gamma(1..4)`` 依次为 x, y, z, t 方向的 DeGrand--Rossi 矩阵；
* ``gamma5 = gamma(1) gamma(2) gamma(3) gamma(4) = diag(1, 1, -1, -1)``；
* ``C = gamma(4) gamma(2)``；
* ``sigma(mu, nu) = (1/2) [gamma(mu), gamma(nu)]``。

所有对象都是 SymPy 精确矩阵或表达式，适合与 :mod:`myqcd.wick` 的组合层
配合，用于算符基、Fierz 重排和费曼规则审计。本模块不做格点张量收缩，
也不把有限维矩阵恒等式升级为真实系综或连续极限验证。
"""

from __future__ import annotations

from functools import lru_cache
from typing import Sequence, Tuple

import sympy as sp

SPINOR_DIM = 4
EUCLIDEAN_DIM = 4
GAMMA_INDEX_MAX = 17


def _dr_gamma_1() -> sp.Matrix:
    i = sp.I
    return sp.Matrix(
        [
            [0, 0, 0, i],
            [0, 0, i, 0],
            [0, -i, 0, 0],
            [-i, 0, 0, 0],
        ]
    )


def _dr_gamma_2() -> sp.Matrix:
    return sp.Matrix(
        [
            [0, 0, 0, -1],
            [0, 0, 1, 0],
            [0, 1, 0, 0],
            [-1, 0, 0, 0],
        ]
    )


def _dr_gamma_3() -> sp.Matrix:
    i = sp.I
    return sp.Matrix(
        [
            [0, 0, i, 0],
            [0, 0, 0, -i],
            [-i, 0, 0, 0],
            [0, i, 0, 0],
        ]
    )


def _dr_gamma_4() -> sp.Matrix:
    return sp.Matrix(
        [
            [0, 0, 1, 0],
            [0, 0, 0, 1],
            [1, 0, 0, 0],
            [0, 1, 0, 0],
        ]
    )


_IDENTITY = sp.eye(SPINOR_DIM)
_GAMMAS = (
    _IDENTITY,
    _dr_gamma_1(),
    _dr_gamma_2(),
    _dr_gamma_3(),
    _dr_gamma_4(),
)
_GAMMA5 = sp.expand(_GAMMAS[1] * _GAMMAS[2] * _GAMMAS[3] * _GAMMAS[4])

_GAMMA_CACHE = {
    0: _IDENTITY,
    1: _GAMMAS[1],
    2: _GAMMAS[2],
    3: _GAMMAS[3],
    4: _GAMMAS[4],
    5: _GAMMA5,
    6: _GAMMAS[2] * _GAMMAS[3],
    7: _GAMMAS[3] * _GAMMAS[1],
    8: _GAMMAS[1] * _GAMMAS[2],
    9: _GAMMAS[1] * _GAMMAS[4],
    10: _GAMMAS[2] * _GAMMAS[4],
    11: _GAMMAS[3] * _GAMMAS[4],
    12: _GAMMAS[1] * _GAMMA5,
    13: _GAMMAS[2] * _GAMMA5,
    14: _GAMMAS[3] * _GAMMA5,
    15: _GAMMAS[4] * _GAMMA5,
    16: (_GAMMAS[3] * _GAMMAS[1]) * ((_IDENTITY + _GAMMAS[4]) / 2),
    17: (_GAMMAS[3] * _GAMMAS[1]) * ((_IDENTITY - _GAMMAS[4]) / 2),
}


def gamma(index: int) -> sp.Matrix:
    """返回 PyQCD 约定下的第 ``index`` 个 gamma 矩阵。

    ``index=0`` 为单位矩阵，``1..4`` 为 DR gamma，``5`` 为 gamma5，
    ``6..17`` 为 PyQCD 预定义的组合。索引范围与
    ``PyQCD/pyqcd/lattice/_gamma.py`` 的 ``gamma(i)`` 一致。
    """

    if not isinstance(index, int) or isinstance(index, bool):
        raise TypeError("gamma index must be an int")
    if index not in _GAMMA_CACHE:
        raise ValueError(f"invalid gamma index {index}; expected 0..17")
    return sp.Matrix(_GAMMA_CACHE[index])


def gamma_matrices() -> Tuple[sp.Matrix, ...]:
    """返回四个 Euclidean gamma（x, y, z, t）。"""

    return tuple(sp.Matrix(matrix) for matrix in _GAMMAS[1:])


def gamma5() -> sp.Matrix:
    """返回 ``gamma5 = gamma1 gamma2 gamma3 gamma4``。"""

    return sp.Matrix(_GAMMA5)


def identity() -> sp.Matrix:
    """返回四维单位矩阵。"""

    return sp.Matrix(_IDENTITY)


def sigma(mu: int, nu: int) -> sp.Matrix:
    """返回 ``sigma_{mu nu} = (1/2)[gamma_mu, gamma_nu]``。

    ``mu`` 与 ``nu`` 使用 DR 索引 1..4（1=x, 2=y, 3=z, 4=t）。
    """

    for index in (mu, nu):
        if not isinstance(index, int) or isinstance(index, bool) or not 1 <= index <= 4:
            raise ValueError("sigma indices must be DR gamma indices 1..4")
    return sp.expand((gamma(mu) * gamma(nu) - gamma(nu) * gamma(mu)) / 2)


def dirac_slash(momentum: Sequence[sp.Expr]) -> sp.Matrix:
    """返回 ``p_slash = sum_{mu=1..4} p_mu gamma_mu``。"""

    if len(momentum) != EUCLIDEAN_DIM:
        raise ValueError("momentum must contain four components")
    return sp.expand(
        sum(
            (
                sp.sympify(component) * _GAMMAS[index + 1]
                for index, component in enumerate(momentum)
            ),
            sp.zeros(SPINOR_DIM),
        )
    )


def dirac_adjoint(matrix: sp.MatrixBase) -> sp.Matrix:
    """返回 Euclidean Dirac 伴随 ``gamma4 M^dagger gamma4``。"""

    matrix = sp.Matrix(matrix)
    if matrix.shape != (SPINOR_DIM, SPINOR_DIM):
        raise ValueError("gamma algebra expects a 4x4 matrix")
    return sp.expand(_GAMMAS[4] * matrix.H * _GAMMAS[4])


def dirac_trace(matrix: sp.MatrixBase) -> sp.Expr:
    """显式求四维矩阵的 Dirac 迹。"""

    matrix = sp.Matrix(matrix)
    if matrix.shape != (SPINOR_DIM, SPINOR_DIM):
        raise ValueError("Dirac trace expects a 4x4 matrix")
    return sp.expand(sum(matrix[index, index] for index in range(SPINOR_DIM)))


@lru_cache(maxsize=None)
def _trace_product(indices: Tuple[int, ...]) -> sp.Expr:
    if len(indices) % 2:
        return sp.Integer(0)
    if not indices:
        return sp.Integer(SPINOR_DIM)
    if len(indices) == 2:
        mu, nu = indices
        return sp.Integer(SPINOR_DIM) * sp.KroneckerDelta(mu, nu)
    head = indices[0]
    total = sp.Integer(0)
    for position in range(1, len(indices)):
        sign = (-1) ** (position + 1)
        rest = indices[1:position] + indices[position + 1 :]
        total += (
            sign
            * sp.KroneckerDelta(head, indices[position])
            * _trace_product(rest)
        )
    return sp.expand(total)


def trace_gamma_product(indices: Sequence[int]) -> sp.Expr:
    """用迹定理计算 ``Tr[gamma_{i1} ... gamma_{in}]``。

    索引取 DR gamma 索引 1..4。奇数个 gamma 的迹为零；本函数不构造显式
    矩阵，因此可直接用于较长链的符号化简。
    """

    normalized = tuple(int(index) for index in indices)
    for index in normalized:
        if not 1 <= index <= 4:
            raise ValueError("trace indices must be DR gamma indices 1..4")
    return _trace_product(normalized)


def gamma_basis() -> Tuple[Tuple[str, sp.Matrix], ...]:
    """返回 16 个正交归一的 Dirac bilinear 基。

    归一化为 ``Tr[Gamma_A Gamma_B] = 4 delta_AB``，基的顺序是
    ``I, gamma_mu, sigma_mu_nu (mu<nu), gamma_mu gamma5, gamma5``。
    """

    entries: list[Tuple[str, sp.Matrix]] = [("I", identity())]
    entries.extend(
        (f"gamma_{index}", gamma(index)) for index in range(1, 5)
    )
    entries.extend(
        (f"sigma_{mu}{nu}", sigma(mu, nu))
        for mu in range(1, 5)
        for nu in range(mu + 1, 5)
    )
    entries.extend(
        (f"gamma_{index}_gamma5", sp.expand(gamma(index) * gamma5()))
        for index in range(1, 5)
    )
    entries.append(("gamma5", gamma5()))
    return tuple(entries)


def gamma_basis_gram() -> sp.Matrix:
    """返回 16 个 Dirac bilinear 基的 Gram 矩阵 ``Tr[Gamma_A Gamma_B]``。

    Euclidean 基中 ``sigma_mu_nu`` 与 ``gamma_mu gamma5`` 是反厄米结构，
    Gram 对角元为 ``-4``；其余为 ``+4``。非对角元应为零。
    """

    basis = gamma_basis()
    count = len(basis)
    return sp.Matrix(
        count,
        count,
        lambda left, right: dirac_trace(
            basis[left][1] * basis[right][1]
        ),
    )


def gamma_basis_rank() -> int:
    """返回 16 个 Dirac bilinear 基的秩；满秩 16 表示构成完备基。"""

    return int(gamma_basis_gram().rank())


def parity_projectors() -> Tuple[sp.Matrix, sp.Matrix]:
    """返回 PyQCD 的双宇称投影 ``P_pm = (1 +/- gamma4)/2``。"""

    return (
        sp.expand((_IDENTITY + _GAMMAS[4]) / 2),
        sp.expand((_IDENTITY - _GAMMAS[4]) / 2),
    )


def chiral_projectors() -> Tuple[sp.Matrix, sp.Matrix]:
    """返回 ``(P_L, P_R) = ((1-gamma5)/2, (1+gamma5)/2)``。"""

    return (
        sp.expand((_IDENTITY - _GAMMA5) / 2),
        sp.expand((_IDENTITY + _GAMMA5) / 2),
    )


def charge_conjugation_matrix() -> sp.Matrix:
    """返回 DR 基中的电荷共轭矩阵 ``C = gamma4 gamma2``。"""

    return sp.expand(_GAMMAS[4] * _GAMMAS[2])


def _proportional_sign(reference: sp.Matrix, result: sp.Matrix) -> int:
    reference = sp.Matrix(reference)
    result = sp.Matrix(result)
    denominator = dirac_trace(reference.H * reference)
    if sp.simplify(denominator) == 0:
        return 0
    ratio = sp.simplify(dirac_trace(reference.H * result) / denominator)
    if ratio == 1:
        return 1
    if ratio == -1:
        return -1
    return 0


def transpose_sign(matrix: sp.MatrixBase) -> int:
    """返回 ``matrix^T = s * matrix`` 的符号 ``s``，非比例结构返回 0。"""

    matrix = sp.Matrix(matrix)
    return _proportional_sign(matrix, matrix.T)


def hermiticity_sign(matrix: sp.MatrixBase) -> int:
    """返回 ``matrix^H = s * matrix`` 的符号 ``s``，非比例结构返回 0。"""

    matrix = sp.Matrix(matrix)
    return _proportional_sign(matrix, matrix.H)


def charge_conjugation_sign(matrix: sp.MatrixBase) -> int:
    """返回 ``C^{-1} matrix C = s * matrix`` 的符号 ``s``。"""

    matrix = sp.Matrix(matrix)
    conjugation = charge_conjugation_matrix()
    return _proportional_sign(
        matrix,
        sp.expand(conjugation.H * matrix * conjugation),
    )


def parity_sign(matrix: sp.MatrixBase) -> int:
    """返回双线性宇称变换 ``gamma4 M gamma4 = s * M`` 的符号。"""

    matrix = sp.Matrix(matrix)
    return _proportional_sign(
        matrix,
        sp.expand(_GAMMAS[4] * matrix * _GAMMAS[4]),
    )


def gamma_properties() -> dict[str, dict[str, int]]:
    """返回 PyQCD 索引 1..17 的 H/T/C 变换符号。"""

    properties: dict[str, dict[str, int]] = {}
    for index in range(1, GAMMA_INDEX_MAX + 1):
        matrix = gamma(index)
        properties[f"gamma_{index}"] = {
            "H": hermiticity_sign(matrix),
            "T": transpose_sign(matrix),
            "C": charge_conjugation_sign(matrix),
        }
    return properties


def clifford_residual(mu: int, nu: int) -> sp.Matrix:
    """返回 ``{gamma_mu, gamma_nu} - 2 delta_{mu nu}`` 的显式矩阵。"""

    if not 1 <= mu <= 4 or not 1 <= nu <= 4:
        raise ValueError("Clifford indices must be DR gamma indices 1..4")
    return sp.expand(
        gamma(mu) * gamma(nu)
        + gamma(nu) * gamma(mu)
        - 2 * (1 if mu == nu else 0) * identity()
    )


__all__ = [
    "EUCLIDEAN_DIM",
    "GAMMA_INDEX_MAX",
    "SPINOR_DIM",
    "charge_conjugation_matrix",
    "charge_conjugation_sign",
    "chiral_projectors",
    "clifford_residual",
    "dirac_adjoint",
    "dirac_slash",
    "dirac_trace",
    "gamma",
    "gamma5",
    "gamma_basis",
    "gamma_basis_gram",
    "gamma_basis_rank",
    "gamma_matrices",
    "gamma_properties",
    "hermiticity_sign",
    "identity",
    "parity_projectors",
    "parity_sign",
    "sigma",
    "trace_gamma_product",
    "transpose_sign",
]
