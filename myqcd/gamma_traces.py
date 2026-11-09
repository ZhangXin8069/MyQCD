"""γ5 迹、手征投影迹与 epsilon 对应关系。"""

from __future__ import annotations

from typing import Sequence

import sympy as sp

from . import gamma


def _validate(indices: Sequence[int]) -> tuple[int, ...]:
    normalized = tuple(int(index) for index in indices)
    for index in normalized:
        if not 1 <= index <= 4:
            raise ValueError("gamma indices must be in 1..4")
    return normalized


def trace_gamma5(indices: Sequence[int]) -> sp.Expr:
    """返回 ``Tr[gamma5 gamma_{i1} ... gamma_{in}]``。

    四个指标时用 epsilon 闭式；其它长度用显式 4x4 矩阵计算。
    """

    normalized = _validate(indices)
    if len(normalized) < 4:
        return sp.Integer(0)
    if len(normalized) == 4:
        return trace_gamma5_four(*normalized)
    matrices = [gamma.gamma5()] + [gamma.gamma(index) for index in normalized]
    total = sp.eye(4)
    for matrix in matrices:
        total = total * matrix
    return sp.expand(gamma.dirac_trace(total))


def trace_gamma5_four(
    mu: int, nu: int, rho: int, sigma: int
) -> sp.Expr:
    """返回 ``Tr[gamma5 gamma_mu gamma_nu gamma_rho gamma_sigma]``。

    在 DR 基中 ``gamma5 = gamma1 gamma2 gamma3 gamma4``，因此该迹为
    ``4 epsilon_{mu nu rho sigma}``（指标映射到 1..4）。
    """

    for index in (mu, nu, rho, sigma):
        if not 1 <= index <= 4:
            raise ValueError("gamma indices must be in 1..4")
    return sp.Integer(4) * sp.LeviCivita(
        mu - 1, nu - 1, rho - 1, sigma - 1
    )


def trace_gamma5_four_residual() -> sp.Expr:
    """检查四个 gamma 的 γ5 迹与 epsilon 闭式的最大残差。"""

    residual = sp.Integer(0)
    for mu in range(1, 5):
        for nu in range(1, 5):
            for rho in range(1, 5):
                for sigma in range(1, 5):
                    explicit = trace_gamma5((mu, nu, rho, sigma))
                    residual += sp.Abs(
                        explicit - trace_gamma5_four(mu, nu, rho, sigma)
                    )
    return sp.simplify(residual)


def trace_left_projector() -> sp.Expr:
    """返回 ``Tr[P_L] = 2``。"""

    left, _ = gamma.chiral_projectors()
    return sp.expand(gamma.dirac_trace(left))


def trace_right_projector() -> sp.Expr:
    """返回 ``Tr[P_R] = 2``。"""

    _, right = gamma.chiral_projectors()
    return sp.expand(gamma.dirac_trace(right))


def trace_projector_orthogonality() -> dict[str, sp.Expr]:
    """返回手征投影迹的正交/完备关系。"""

    left, right = gamma.chiral_projectors()
    return {
        "Tr[P_L]": gamma.dirac_trace(left),
        "Tr[P_R]": gamma.dirac_trace(right),
        "Tr[P_L P_R]": gamma.dirac_trace(left * right),
        "Tr[P_L + P_R]": gamma.dirac_trace(left + right),
    }


def gamma5_anticommutator_residual(mu: int) -> sp.Matrix:
    """返回 ``{gamma5, gamma_mu}`` 的矩阵残差。"""

    if not 1 <= mu <= 4:
        raise ValueError("gamma index must be in 1..4")
    return sp.expand(
        gamma.gamma5() * gamma.gamma(mu)
        + gamma.gamma(mu) * gamma.gamma5()
    )


def trace_gamma5_table() -> tuple[dict[str, object], ...]:
    """返回若干 γ5 迹样本。"""

    samples = []
    for indices in ((1, 2, 3, 4), (1, 2, 3), (1, 2), (1, 2, 3, 4, 1, 2)):
        samples.append(
            {
                "indices": indices,
                "trace": str(trace_gamma5(indices)),
            }
        )
    return tuple(samples)


__all__ = [
    "gamma5_anticommutator_residual",
    "trace_gamma5",
    "trace_gamma5_four",
    "trace_gamma5_four_residual",
    "trace_gamma5_table",
    "trace_left_projector",
    "trace_projector_orthogonality",
    "trace_right_projector",
]
