"""算符基构建：Dirac 结构、导数、手征组合与颜色表示。

本模块在 :mod:`myqcd.operators` 的双线性结构上增加导数和颜色维度，
用于构造格点 QCD 中常见的双线性算符基。它只处理结构、量子数与量纲；
Wilson 线、涂抹、矩阵元匹配和重整化常数属于独立层。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence, Tuple

import sympy as sp

from . import fierz, gamma, operators

COLOR_REPRESENTATIONS = ("singlet", "octet")


@dataclass(frozen=True)
class DerivativeOperator:
    """带导数计数的双线性算符结构。"""

    name: str
    structure: str
    derivatives: int = 0
    color: str = "singlet"
    left_flavor: str = "q"
    right_flavor: str = "q"

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("operator name must be a nonempty string")
        if self.structure not in operators.dirac_bilinear_structures():
            raise ValueError(f"unknown Dirac structure {self.structure!r}")
        if (
            not isinstance(self.derivatives, int)
            or isinstance(self.derivatives, bool)
            or self.derivatives < 0
        ):
            raise ValueError("derivatives must be a nonnegative int")
        if self.color not in COLOR_REPRESENTATIONS:
            raise ValueError(
                f"color must be one of {COLOR_REPRESENTATIONS}"
            )
        for flavor in (self.left_flavor, self.right_flavor):
            if not isinstance(flavor, str) or not flavor.strip():
                raise ValueError("flavor labels must be nonempty strings")

    @property
    def base(self) -> operators.BilinearOperator:
        return operators.BilinearOperator(
            name=self.name,
            left_flavor=self.left_flavor,
            right_flavor=self.right_flavor,
            structure=self.structure,
            derivatives=self.derivatives,
            color=self.color,
        )

    @property
    def matrix(self) -> sp.Matrix:
        return self.base.matrix

    @property
    def label(self) -> str:
        return self.base.label

    @property
    def mass_dimension(self) -> sp.Expr:
        return self.base.mass_dimension

    @property
    def parity_sign(self) -> int:
        return self.base.parity_sign

    @property
    def charge_conjugation_sign(self) -> int:
        return self.base.charge_conjugation_sign

    @property
    def pyqcd_gamma_index(self) -> int | None:
        return self.base.pyqcd_gamma_index

    def latex(self) -> str:
        base = self.base.latex()
        if self.derivatives == 0:
            return base
        return rf"D^{{{self.derivatives}}}{base}"

    def to_dict(self) -> dict[str, object]:
        data = self.base.to_dict()
        data["name"] = self.name
        data["derivatives"] = self.derivatives
        data["color"] = self.color
        data["latex"] = self.latex()
        return data


def enumerate_derivative_operators(
    flavors: Sequence[str] = ("u", "d"),
    *,
    max_derivatives: int = 2,
    colors: Sequence[str] = COLOR_REPRESENTATIONS,
    structures: Iterable[str] | None = None,
) -> Tuple[DerivativeOperator, ...]:
    """枚举味、Dirac 结构、导数阶数与颜色表示的组合。"""

    if not flavors:
        raise ValueError("at least one flavor is required")
    if max_derivatives < 0:
        raise ValueError("max_derivatives must be nonnegative")
    for color in colors:
        if color not in COLOR_REPRESENTATIONS:
            raise ValueError(f"unknown color representation {color!r}")
    selected = (
        tuple(operators.dirac_bilinear_structures())
        if structures is None
        else tuple(structures)
    )
    result: list[DerivativeOperator] = []
    for left in flavors:
        for right in flavors:
            for structure in selected:
                for derivatives in range(max_derivatives + 1):
                    for color in colors:
                        result.append(
                            DerivativeOperator(
                                name=(
                                    f"{left}_{right}_{structure}"
                                    f"_d{derivatives}_{color}"
                                ),
                                structure=structure,
                                derivatives=derivatives,
                                color=color,
                                left_flavor=left,
                                right_flavor=right,
                            )
                        )
    return tuple(result)


def chiral_bilinear_structures(
    mu: int = 3,
) -> dict[str, sp.Matrix]:
    """返回 ``P_a gamma_mu P_b`` 四种手征组合。

    键 ``LL``、``RR``、``LR``、``RL`` 分别表示左右手征投影器的
    组合；由于 ``gamma5`` 与 ``gamma_mu`` 反交换，``LR`` 与
    ``gamma_mu P_R``、``RL`` 与 ``gamma_mu P_L`` 等价。
    """

    if not 1 <= mu <= gamma.EUCLIDEAN_DIM:
        raise ValueError("mu must be a DR gamma index 1..4")
    gamma_mu = gamma.gamma(mu)
    left, right = gamma.chiral_projectors()
    return {
        "LL": sp.expand(left * gamma_mu * left),
        "RR": sp.expand(right * gamma_mu * right),
        "LR": sp.expand(left * gamma_mu * right),
        "RL": sp.expand(right * gamma_mu * left),
    }


def vector_axial_combinations(mu: int = 3) -> dict[str, sp.Matrix]:
    """返回 ``V_mu +/- A_mu`` 的矩阵。"""

    if not 1 <= mu <= gamma.EUCLIDEAN_DIM:
        raise ValueError("mu must be a DR gamma index 1..4")
    vector = gamma.gamma(mu)
    axial = sp.expand(gamma.gamma(mu) * gamma.gamma5())
    return {
        "V+A": sp.expand(vector + axial),
        "V-A": sp.expand(vector - axial),
    }


def chiral_projector_identities() -> dict[str, bool]:
    """检查手征投影与 ``V +/- A`` 的代数恒等式。"""

    left, right = gamma.chiral_projectors()
    checks = {
        "left_idempotent": (left * left - left).is_zero_matrix,
        "right_idempotent": (right * right - right).is_zero_matrix,
        "orthogonal": (left * right).is_zero_matrix,
        "complete": (left + right - gamma.identity()).is_zero_matrix,
    }
    for mu in range(1, gamma.EUCLIDEAN_DIM + 1):
        vector = gamma.gamma(mu)
        axial = sp.expand(gamma.gamma(mu) * gamma.gamma5())
        checks[f"VA_left_{mu}"] = (
            sp.expand(vector + axial) - 2 * (gamma.gamma(mu) * right)
        ).is_zero_matrix
        checks[f"VA_right_{mu}"] = (
            sp.expand(vector - axial) - 2 * (gamma.gamma(mu) * left)
        ).is_zero_matrix
    return checks


def fierz_rearrangement(
    left_structure: str, right_structure: str
) -> Tuple[Tuple[str, str, sp.Expr], ...]:
    """返回两个双线性结构乘积的 Fierz 重排项。"""

    return fierz.fierz_terms(left_structure, right_structure)


def color_factor(representation: str, adjoint_index: int | None = None) -> str:
    """返回颜色因子标签；``octet`` 需要 adjoint 指标。"""

    if representation == "singlet":
        if adjoint_index is not None:
            raise ValueError("singlet color factor takes no adjoint index")
        return "1"
    if representation == "octet":
        if adjoint_index is None or not 1 <= adjoint_index <= 8:
            raise ValueError("octet color factor requires an index in 1..8")
        return f"T^{adjoint_index}"
    raise ValueError(f"unknown color representation {representation!r}")


def operator_table(
    *,
    max_derivatives: int = 1,
    flavors: Sequence[str] = ("u", "d"),
    colors: Sequence[str] = ("singlet",),
) -> Tuple[dict[str, object], ...]:
    """返回可直接序列化的算符基表。"""

    return tuple(
        operator.to_dict()
        for operator in enumerate_derivative_operators(
            flavors,
            max_derivatives=max_derivatives,
            colors=colors,
        )
    )


def quantum_number_summary() -> dict[str, object]:
    """返回 16 个结构的类别、数量与示例。"""

    structures = operators.dirac_bilinear_structures()
    labels = {
        label: tuple(
            name
            for name in structures
            if operators.structure_label(name) == label
        )
        for label in operators.DIRAC_STRUCTURE_LABELS
    }
    return {
        "count": len(structures),
        "labels": labels,
        "derivative_dimension": {
            derivatives: str(operators.operator_mass_dimension(derivatives))
            for derivatives in range(4)
        },
    }


__all__ = [
    "COLOR_REPRESENTATIONS",
    "DerivativeOperator",
    "chiral_bilinear_structures",
    "chiral_projector_identities",
    "color_factor",
    "enumerate_derivative_operators",
    "fierz_rearrangement",
    "operator_table",
    "quantum_number_summary",
    "vector_axial_combinations",
]
