"""单圈型 RGE 的符号/数值演化工具。"""

from __future__ import annotations

from typing import Sequence, Tuple

import sympy as sp


def solve_z(
    mu: sp.Expr, mu0: sp.Expr, gamma: sp.Expr
) -> sp.Expr:
    """返回 ``Z(mu) = (mu/mu0)^(-gamma)``。"""

    mu = sp.sympify(mu)
    mu0 = sp.sympify(mu0)
    if sp.simplify(mu0) == 0:
        raise ValueError("mu0 must be nonzero")
    return sp.simplify((mu / mu0) ** (-sp.sympify(gamma)))


def anomalous_dimension_from_z(z: sp.Expr, mu: sp.Symbol) -> sp.Expr:
    """返回 ``gamma = - d log Z / d log mu``。"""

    z = sp.sympify(z)
    if sp.simplify(z) == 0:
        raise ValueError("Z must be nonzero")
    return sp.simplify(-mu * sp.diff(sp.log(z), mu))


def evolve_operator(
    initial: sp.Expr, gamma: sp.Expr, mu0: sp.Expr, mu: sp.Expr
) -> sp.Expr:
    """返回单算符演化 ``initial * (mu/mu0)^(-gamma)``。"""

    return sp.simplify(
        sp.sympify(initial) * solve_z(mu, mu0, gamma)
    )


def diagonal_evolution_matrix(
    gammas: Sequence[sp.Expr], mu0: sp.Expr, mu: sp.Expr
) -> sp.Matrix:
    """返回对角演化矩阵。"""

    if not gammas:
        raise ValueError("gammas must be nonempty")
    return sp.diag(*[solve_z(mu, mu0, gamma) for gamma in gammas])


def evolution_residual(
    initial: sp.Expr, gamma: sp.Expr, mu0: sp.Expr, mu: sp.Expr
) -> sp.Expr:
    """检查演化结果是否满足 ``Z`` 的幂律。"""

    evolved = evolve_operator(initial, gamma, mu0, mu)
    expected = sp.simplify(initial * solve_z(mu, mu0, gamma))
    return sp.simplify(evolved - expected)


def evolution_table() -> Tuple[dict[str, object], ...]:
    """返回若干 gamma 的演化样本。"""

    mu0 = sp.Symbol("mu0", positive=True)
    mu = sp.Symbol("mu", positive=True)
    return tuple(
        {
            "gamma": str(gamma),
            "ratio": str(sp.simplify(solve_z(mu, mu0, gamma))),
        }
        for gamma in (0, sp.Rational(1, 2), 1, -1)
    )


__all__ = [
    "anomalous_dimension_from_z",
    "diagonal_evolution_matrix",
    "evolution_residual",
    "evolution_table",
    "evolve_operator",
    "solve_z",
]
