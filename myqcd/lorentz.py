"""四维 Euclidean Lorentz 张量代数、epsilon 恒等式与投影算子。

本模块为算符构建提供独立于具体表示的 Lorentz 工具：度规、Levi-Civita
张量、双重缩并、Schouten 恒等式、横向/纵向投影以及横向无迹 spin-2
投影。所有对象都是 SymPy 精确表达式；模块不声称完成圈积分或真实系综
收缩。
"""

from __future__ import annotations

import itertools
from typing import Sequence

import sympy as sp

DIM = 4


def metric() -> sp.Matrix:
    """返回四维 Euclidean 度规 ``delta_{mu nu}``。"""

    return sp.eye(DIM)


def vector_components(prefix: str) -> tuple[sp.Symbol, ...]:
    """返回四个实符号，用作动量或极化矢量分量。"""

    return tuple(
        sp.Symbol(f"{prefix}{index}", real=True)
        for index in range(DIM)
    )


def contract_vectors(
    left: Sequence[sp.Expr], right: Sequence[sp.Expr]
) -> sp.Expr:
    """返回 Euclidean 内积 ``sum_mu left_mu right_mu``。"""

    if len(left) != DIM or len(right) != DIM:
        raise ValueError("Lorentz vectors must have four components")
    return sp.expand(
        sum(sp.sympify(left[index]) * sp.sympify(right[index]) for index in range(DIM))
    )


def epsilon_tensor() -> sp.Array:
    """返回四维 Levi-Civita 张量 ``epsilon_{mu nu rho sigma}``。"""

    return sp.Array(
        [
            [
                [
                    [sp.LeviCivita(mu, nu, rho, sigma) for sigma in range(DIM)]
                    for rho in range(DIM)
                ]
                for nu in range(DIM)
            ]
            for mu in range(DIM)
        ]
    )


def epsilon_square() -> sp.Expr:
    """返回 ``sum epsilon_{mu nu rho sigma}^2 = 4! = 24``。"""

    return sp.Integer(24)


def epsilon_two_contract(
    mu: int, nu: int, alpha: int, beta: int
) -> sp.Expr:
    """返回 ``sum_{rho sigma} epsilon_{mu nu rho sigma}
    epsilon_{alpha beta rho sigma}`` 的闭式。

    在四维 Euclidean 约定下为
    ``2 (delta_{mu alpha} delta_{nu beta}
    - delta_{mu beta} delta_{nu alpha})``。
    """

    for index in (mu, nu, alpha, beta):
        if not 0 <= index < DIM:
            raise ValueError("epsilon indices must be in 0..3")
    return sp.expand(
        2
        * (
            sp.KroneckerDelta(mu, alpha) * sp.KroneckerDelta(nu, beta)
            - sp.KroneckerDelta(mu, beta) * sp.KroneckerDelta(nu, alpha)
        )
    )


def epsilon_four_contract(
    mu: int, nu: int, rho: int, sigma: int,
    alpha: int, beta: int, gamma: int, delta: int,
) -> sp.Expr:
    """返回两个 epsilon 全指标缩并的行列式形式。

    ``epsilon_{mu nu rho sigma} epsilon_{alpha beta gamma delta}``
    等于 ``det(delta_{i j})``，其中行指标为
    ``(mu, nu, rho, sigma)``，列指标为
    ``(alpha, beta, gamma, delta)``。
    """

    indices = (mu, nu, rho, sigma, alpha, beta, gamma, delta)
    if any(not 0 <= index < DIM for index in indices):
        raise ValueError("epsilon indices must be in 0..3")
    rows = (mu, nu, rho, sigma)
    columns = (alpha, beta, gamma, delta)
    return sp.expand(
        sp.Matrix(
            DIM,
            DIM,
            lambda row, column: sp.KroneckerDelta(rows[row], columns[column]),
        ).det()
    )


def epsilon_two_contract_residual() -> sp.Expr:
    """检查双重缩并闭式的最大残差。"""

    residual = sp.Integer(0)
    for mu in range(DIM):
        for nu in range(DIM):
            for alpha in range(DIM):
                for beta in range(DIM):
                    direct = sum(
                        sp.LeviCivita(mu, nu, rho, sigma)
                        * sp.LeviCivita(alpha, beta, rho, sigma)
                        for rho in range(DIM)
                        for sigma in range(DIM)
                    )
                    residual += sp.Abs(
                        sp.expand(direct - epsilon_two_contract(mu, nu, alpha, beta))
                    )
    return sp.simplify(residual)


def schouten_residual(
    momentum: Sequence[sp.Expr],
) -> sp.Expr:
    """返回四维 Schouten 恒等式的标量残差。

    对五条 Lorentz 指标 ``(a,b,c,d,e)``，检查

    ``epsilon_{abcd} p_e + epsilon_{bcde} p_a
    + epsilon_{cdea} p_b + epsilon_{deab} p_c
    + epsilon_{eabc} p_d = 0``。

    这是四维中五指标全反对称张量不存在导致的恒等式。
    """

    if len(momentum) != DIM:
        raise ValueError("momentum must contain four components")
    components = tuple(sp.sympify(component) for component in momentum)
    total = sp.Integer(0)
    for a, b, c, d, e in itertools.product(range(DIM), repeat=5):
        total += (
            sp.LeviCivita(a, b, c, d) * components[e]
            + sp.LeviCivita(b, c, d, e) * components[a]
            + sp.LeviCivita(c, d, e, a) * components[b]
            + sp.LeviCivita(d, e, a, b) * components[c]
            + sp.LeviCivita(e, a, b, c) * components[d]
        )
    return sp.simplify(total)


def transverse_projector(
    momentum: Sequence[sp.Expr], mu: int, nu: int
) -> sp.Expr:
    """返回横向投影 ``delta_{mu nu} - p_mu p_nu / p^2``。"""

    if len(momentum) != DIM:
        raise ValueError("momentum must contain four components")
    for index in (mu, nu):
        if not 0 <= index < DIM:
            raise ValueError("projector indices must be in 0..3")
    p2 = contract_vectors(momentum, momentum)
    if sp.simplify(p2) == 0:
        raise ValueError("transverse projector requires p^2 != 0")
    return sp.expand(
        sp.KroneckerDelta(mu, nu)
        - sp.sympify(momentum[mu]) * sp.sympify(momentum[nu]) / p2
    )


def longitudinal_projector(
    momentum: Sequence[sp.Expr], mu: int, nu: int
) -> sp.Expr:
    """返回纵向投影 ``p_mu p_nu / p^2``。"""

    if len(momentum) != DIM:
        raise ValueError("momentum must contain four components")
    p2 = contract_vectors(momentum, momentum)
    if sp.simplify(p2) == 0:
        raise ValueError("longitudinal projector requires p^2 != 0")
    return sp.expand(
        sp.sympify(momentum[mu]) * sp.sympify(momentum[nu]) / p2
    )


def transverse_traceless_spin2(
    momentum: Sequence[sp.Expr],
    mu: int,
    nu: int,
    rho: int,
    sigma: int,
) -> sp.Expr:
    """返回横向无迹 spin-2 投影。

    ``P2 = 1/2 (T_{mu rho} T_{nu sigma} + T_{mu sigma} T_{nu rho})
    - 1/3 T_{mu nu} T_{rho sigma}``，其中 ``T`` 是横向投影。
    """

    t_mr = transverse_projector(momentum, mu, rho)
    t_ns = transverse_projector(momentum, nu, sigma)
    t_ms = transverse_projector(momentum, mu, sigma)
    t_nr = transverse_projector(momentum, nu, rho)
    t_mn = transverse_projector(momentum, mu, nu)
    t_rs = transverse_projector(momentum, rho, sigma)
    return sp.expand(
        (t_mr * t_ns + t_ms * t_nr) / 2
        - t_mn * t_rs / 3
    )


def spin2_traceless_check(momentum: Sequence[sp.Expr]) -> sp.Expr:
    """返回 ``sum_rho P2_{mu nu rho rho}`` 的总残差（应为 0）。"""

    return sp.simplify(
        sum(
            transverse_traceless_spin2(momentum, mu, nu, rho, rho)
            for mu in range(DIM)
            for nu in range(DIM)
            for rho in range(DIM)
        )
    )


def spin2_dimension(momentum: Sequence[sp.Expr]) -> sp.Expr:
    """返回全缩并 ``sum_{mu nu} P2_{mu nu mu nu}``。

    四维中横向无迹 spin-2 投影对应三维空间对称无迹张量，
    维数为 ``(D-1)D/2 - 1 = 5``。
    """

    return sp.simplify(
        sum(
            transverse_traceless_spin2(momentum, mu, nu, mu, nu)
            for mu in range(DIM)
            for nu in range(DIM)
        )
    )


__all__ = [
    "DIM",
    "contract_vectors",
    "epsilon_four_contract",
    "epsilon_square",
    "epsilon_tensor",
    "epsilon_two_contract",
    "epsilon_two_contract_residual",
    "longitudinal_projector",
    "metric",
    "schouten_residual",
    "spin2_dimension",
    "spin2_traceless_check",
    "transverse_projector",
    "transverse_traceless_spin2",
    "vector_components",
]
