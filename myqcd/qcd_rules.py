"""QCD 费曼规则的符号表示与结构检查。

本模块给出四维 Euclidean 约定下的传播子、顶点颜色/Lorentz 因子与
量纲记账。它是**规则层**：不做圈积分、不推导对称因子，也不把这里的
结构式升级为完整微扰计算。不同文献的 Minkowski 符号约定可能相差
整体符号，使用前应显式核对 ``convention`` 字段。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence, Tuple

import sympy as sp

from . import color, gamma, lorentz

CONVENTION = "Euclidean; overall vertex signs follow the stated formulas"


@dataclass(frozen=True)
class VertexFactor:
    """一个顶点的颜色与 Lorentz 因子。"""

    name: str
    particles: Tuple[str, ...]
    color_factor: str
    lorentz_factor: str
    coupling_power: int
    mass_dimension: int
    notes: str = ""

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("vertex name must be nonempty")
        if not self.particles:
            raise ValueError("vertex must contain particles")
        if self.coupling_power < 0:
            raise ValueError("coupling power must be nonnegative")

    def to_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "particles": list(self.particles),
            "color_factor": self.color_factor,
            "lorentz_factor": self.lorentz_factor,
            "coupling_power": self.coupling_power,
            "mass_dimension": self.mass_dimension,
            "notes": self.notes,
            "convention": CONVENTION,
        }


def quark_propagator(
    momentum: Sequence[sp.Expr], mass: sp.Expr
) -> sp.Matrix:
    """返回 Euclidean 夸克传播子 ``(m - i p_slash)/(p^2 + m^2)``。"""

    if len(momentum) != lorentz.DIM:
        raise ValueError("momentum must contain four components")
    mass = sp.sympify(mass)
    pslash = gamma.dirac_slash(momentum)
    p2 = lorentz.contract_vectors(momentum, momentum)
    denominator = sp.simplify(p2 + mass**2)
    if sp.simplify(denominator) == 0:
        raise ValueError("quark propagator pole: p^2 + m^2 = 0")
    return sp.simplify(
        (mass * gamma.identity() - sp.I * pslash) / denominator
    )


def quark_propagator_inverse(
    momentum: Sequence[sp.Expr], mass: sp.Expr
) -> sp.Matrix:
    """返回夸克传播子的 Dirac 逆 ``m + i p_slash``。"""

    mass = sp.sympify(mass)
    return sp.expand(mass * gamma.identity() + sp.I * gamma.dirac_slash(momentum))


def quark_propagator_residual(
    momentum: Sequence[sp.Expr], mass: sp.Expr
) -> sp.Matrix:
    """返回 ``(m + i p_slash) S(p) - 1`` 的矩阵残差。"""

    product = sp.expand(
        quark_propagator_inverse(momentum, mass)
        * quark_propagator(momentum, mass)
    )
    return sp.simplify(product - gamma.identity())


def gluon_propagator(
    momentum: Sequence[sp.Expr],
    mu: int,
    nu: int,
    *,
    gauge_parameter: sp.Expr = sp.Integer(1),
) -> sp.Expr:
    """返回胶子传播子（协变规范）。

    ``D_{mu nu} = delta_{mu nu}/p^2
    - (1 - xi) p_mu p_nu / p^4``；``xi=1`` 为 Feynman 规范，
    ``xi=0`` 为 Landau 规范。
    """

    if len(momentum) != lorentz.DIM:
        raise ValueError("momentum must contain four components")
    for index in (mu, nu):
        if not 0 <= index < lorentz.DIM:
            raise ValueError("gluon indices must be in 0..3")
    p2 = lorentz.contract_vectors(momentum, momentum)
    if sp.simplify(p2) == 0:
        raise ValueError("gluon propagator requires p^2 != 0")
    xi = sp.sympify(gauge_parameter)
    return sp.expand(
        sp.KroneckerDelta(mu, nu) / p2
        - (1 - xi)
        * sp.sympify(momentum[mu])
        * sp.sympify(momentum[nu])
        / p2**2
    )


def gluon_transversality(
    momentum: Sequence[sp.Expr], nu: int, *, gauge_parameter: sp.Expr = 0
) -> sp.Expr:
    """返回 ``p_mu D^{mu nu}``；Landau 规范下应为 0。"""

    return sp.simplify(
        sum(
            sp.sympify(momentum[mu])
            * gluon_propagator(
                momentum, mu, nu, gauge_parameter=gauge_parameter
            )
            for mu in range(lorentz.DIM)
        )
    )


def ghost_propagator(momentum: Sequence[sp.Expr]) -> sp.Expr:
    """返回鬼场传播子 ``1/p^2``。"""

    p2 = lorentz.contract_vectors(momentum, momentum)
    if sp.simplify(p2) == 0:
        raise ValueError("ghost propagator requires p^2 != 0")
    return sp.simplify(1 / p2)


def ward_identity_residual(momentum: Sequence[sp.Expr]) -> sp.Matrix:
    """返回 ``p_slash p_slash - p^2``（无质量 Ward 代数代理）。"""

    pslash = gamma.dirac_slash(momentum)
    p2 = lorentz.contract_vectors(momentum, momentum)
    return sp.simplify(pslash * pslash - p2 * gamma.identity())


def three_gluon_lorentz(
    k1: Sequence[sp.Expr],
    k2: Sequence[sp.Expr],
    k3: Sequence[sp.Expr],
    mu: int,
    nu: int,
    rho: int,
) -> sp.Expr:
    """返回三胶子顶点的 Lorentz 张量（全部入流动量）。"""

    for vector in (k1, k2, k3):
        if len(vector) != lorentz.DIM:
            raise ValueError("momenta must contain four components")
    return sp.expand(
        (sp.sympify(k1[rho]) - sp.sympify(k2[rho]))
        * sp.KroneckerDelta(mu, nu)
        + (sp.sympify(k2[mu]) - sp.sympify(k3[mu]))
        * sp.KroneckerDelta(nu, rho)
        + (sp.sympify(k3[nu]) - sp.sympify(k1[nu]))
        * sp.KroneckerDelta(rho, mu)
    )


def four_gluon_color_structures() -> Tuple[str, ...]:
    """返回四胶子顶点的三组颜色收缩。"""

    return (
        "f^{abe} f^{cde}",
        "f^{ace} f^{bde}",
        "f^{ade} f^{bce}",
    )


def gluon_vertex_factors() -> Tuple[VertexFactor, ...]:
    """返回 QCD 顶点因子清单。"""

    return (
        VertexFactor(
            name="quark-antiquark-gluon",
            particles=("quark", "antiquark", "gluon"),
            color_factor="T^a_{ij}",
            lorentz_factor="gamma_mu",
            coupling_power=1,
            mass_dimension=0,
            notes="g T^a gamma_mu",
        ),
        VertexFactor(
            name="three-gluon",
            particles=("gluon", "gluon", "gluon"),
            color_factor="f^{abc}",
            lorentz_factor=(
                "(k1-k2)_rho delta_{mu nu} + "
                "(k2-k3)_mu delta_{nu rho} + "
                "(k3-k1)_nu delta_{rho mu}"
            ),
            coupling_power=1,
            mass_dimension=1,
            notes="g f^{abc} V_{mu nu rho}",
        ),
        VertexFactor(
            name="four-gluon",
            particles=("gluon", "gluon", "gluon", "gluon"),
            color_factor="f^{abe} f^{cde} + permutations",
            lorentz_factor="delta delta permutations",
            coupling_power=2,
            mass_dimension=0,
            notes="g^2 times three color contractions",
        ),
        VertexFactor(
            name="ghost-antighost-gluon",
            particles=("ghost", "antighost", "gluon"),
            color_factor="f^{abc}",
            lorentz_factor="k_mu",
            coupling_power=1,
            mass_dimension=1,
            notes="g f^{abc} k_mu",
        ),
    )


def propagator_mass_dimensions() -> dict[str, int]:
    """返回传播子的质量量纲（四维）。"""

    return {"quark": -1, "gluon": -2, "ghost": -2}


def rule_audit() -> dict[str, object]:
    """返回规则层的结构自检。"""

    vertices = gluon_vertex_factors()
    return {
        "convention": CONVENTION,
        "vertex_count": len(vertices),
        "vertices": [vertex.to_dict() for vertex in vertices],
        "propagator_dimensions": propagator_mass_dimensions(),
        "four_gluon_colors": list(four_gluon_color_structures()),
    }


__all__ = [
    "CONVENTION",
    "VertexFactor",
    "four_gluon_color_structures",
    "ghost_propagator",
    "gluon_propagator",
    "gluon_transversality",
    "gluon_vertex_factors",
    "propagator_mass_dimensions",
    "quark_propagator",
    "quark_propagator_inverse",
    "quark_propagator_residual",
    "rule_audit",
    "three_gluon_lorentz",
    "ward_identity_residual",
]
