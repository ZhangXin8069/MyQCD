"""QCD 双线性算符构建与 Dirac 结构分类。

本模块把 16 个 Dirac 双线性结构按标量 (S)、赝标量 (P)、矢量 (V)、
轴矢量 (A) 和张量 (T) 分类，提供精确分解、宇称与电荷共轭符号、质量量纲
计数，以及与 PyQCD ``gamma(i)`` 索引的对接。

算符对象只描述旋量结构与味标签；颜色单态/八重态、导数和 Wilson 线等
附加结构通过独立字段记录。本模块不声称已经完成重整化、混合或矩阵元
匹配。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping, Sequence, Tuple

import sympy as sp

from . import gamma as gamma_module

DIRAC_STRUCTURE_LABELS = ("S", "P", "V", "A", "T")
COLOR_REPRESENTATIONS = ("singlet", "octet")


def dirac_bilinear_structures() -> dict[str, sp.Matrix]:
    """返回 16 个 Dirac 双线性结构：``S, P, V_mu, A_mu, T_{mu nu}``。"""

    structures: dict[str, sp.Matrix] = {
        "S": gamma_module.identity(),
        "P": gamma_module.gamma5(),
    }
    structures.update(
        {
            f"V{mu}": gamma_module.gamma(mu)
            for mu in range(1, gamma_module.EUCLIDEAN_DIM + 1)
        }
    )
    structures.update(
        {
            f"A{mu}": sp.expand(
                gamma_module.gamma(mu) * gamma_module.gamma5()
            )
            for mu in range(1, gamma_module.EUCLIDEAN_DIM + 1)
        }
    )
    structures.update(
        {
            f"T{mu}{nu}": gamma_module.sigma(mu, nu)
            for mu in range(1, gamma_module.EUCLIDEAN_DIM + 1)
            for nu in range(mu + 1, gamma_module.EUCLIDEAN_DIM + 1)
        }
    )
    return structures


def structure_label(name: str) -> str:
    """返回结构名的物理分类标签 ``S/P/V/A/T``。"""

    if name not in dirac_bilinear_structures():
        raise ValueError(f"unknown Dirac structure {name!r}")
    if name in ("S", "P"):
        return name
    return name[0]


def structure_matrix(name: str) -> sp.Matrix:
    """返回结构名对应的 4x4 矩阵。"""

    structures = dirac_bilinear_structures()
    if name not in structures:
        raise ValueError(f"unknown Dirac structure {name!r}")
    return sp.Matrix(structures[name])


def decompose_dirac_bilinear(matrix: sp.MatrixBase) -> dict[str, sp.Expr]:
    """把任意 4x4 矩阵分解到 16 个双线性基上。

    使用 Gram 正交性 ``Tr[Gamma_A Gamma_B] = 0 (A != B)``；基的归一化
    自动读取，因此 Euclidean 下 ``sigma`` 与 ``gamma_mu gamma5`` 的
    ``-4`` 对角元不会引入符号错误。
    """

    matrix = sp.Matrix(matrix)
    if matrix.shape != (
        gamma_module.SPINOR_DIM,
        gamma_module.SPINOR_DIM,
    ):
        raise ValueError("bilinear decomposition expects a 4x4 matrix")
    coefficients: dict[str, sp.Expr] = {}
    for name, basis in dirac_bilinear_structures().items():
        denominator = gamma_module.dirac_trace(basis * basis)
        if sp.simplify(denominator) == 0:
            raise ValueError(f"degenerate Dirac basis element {name!r}")
        coefficients[name] = sp.simplify(
            gamma_module.dirac_trace(basis * matrix) / denominator
        )
    return coefficients


def reconstruct_dirac_bilinear(
    coefficients: Mapping[str, sp.Expr],
) -> sp.Matrix:
    """把结构系数重组为 4x4 矩阵，用于分解往返验证。"""

    structures = dirac_bilinear_structures()
    total = sp.zeros(gamma_module.SPINOR_DIM)
    for name, coefficient in coefficients.items():
        if name not in structures:
            raise ValueError(f"unknown Dirac structure {name!r}")
        total += sp.sympify(coefficient) * structures[name]
    return sp.expand(total)


def operator_mass_dimension(
    derivatives: int = 0,
    gluon_field_strengths: int = 0,
) -> sp.Expr:
    """返回 4 维欧氏空间中算符的质量量纲。

    ``psi_bar Gamma psi`` 的量纲为 3；每个协变导数 ``D`` 增加 1；
    每个场强张量 ``F`` 增加 2。
    """

    if derivatives < 0 or gluon_field_strengths < 0:
        raise ValueError("operator multiplicities must be nonnegative")
    return sp.Integer(3 + derivatives + 2 * gluon_field_strengths)


def pyqcd_gamma_index(matrix: sp.MatrixBase) -> int | None:
    """返回与 PyQCD ``gamma(i)`` 精确相同的索引；无精确匹配返回 ``None``。"""

    matrix = sp.Matrix(matrix)
    for index in range(gamma_module.GAMMA_INDEX_MAX + 1):
        if (gamma_module.gamma(index) - matrix).is_zero_matrix:
            return index
    return None


def _structure_latex(name: str) -> str:
    if name == "S":
        return "1"
    if name == "P":
        return r"\gamma_5"
    if name.startswith("V"):
        return rf"\gamma_{{{name[1:]}}}"
    if name.startswith("A"):
        return rf"\gamma_{{{name[1:]}}}\gamma_5"
    if name.startswith("T"):
        return rf"\sigma_{{{name[1]}{name[2]}}}"
    raise ValueError(f"unknown Dirac structure {name!r}")


@dataclass(frozen=True)
class BilinearOperator:
    """一个夸克双线性算符 ``bar{q}_L Gamma q_R`` 的结构描述。"""

    name: str
    left_flavor: str
    right_flavor: str
    structure: str
    derivatives: int = 0
    color: str = "singlet"

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("operator name must be a nonempty string")
        for flavor in (self.left_flavor, self.right_flavor):
            if not isinstance(flavor, str) or not flavor.strip():
                raise ValueError("flavor labels must be nonempty strings")
        if self.structure not in dirac_bilinear_structures():
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

    @property
    def matrix(self) -> sp.Matrix:
        return structure_matrix(self.structure)

    @property
    def label(self) -> str:
        return structure_label(self.structure)

    @property
    def mass_dimension(self) -> sp.Expr:
        return operator_mass_dimension(self.derivatives)

    @property
    def parity_sign(self) -> int:
        return gamma_module.parity_sign(self.matrix)

    @property
    def charge_conjugation_sign(self) -> int:
        return gamma_module.charge_conjugation_sign(self.matrix)

    @property
    def pyqcd_gamma_index(self) -> int | None:
        return pyqcd_gamma_index(self.matrix)

    def latex(self) -> str:
        """返回算符的 LaTeX 结构式。"""

        return (
            rf"\bar{{q}}_{{{self.left_flavor}}}"
            rf"{_structure_latex(self.structure)}"
            rf"q_{{{self.right_flavor}}}"
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "left_flavor": self.left_flavor,
            "right_flavor": self.right_flavor,
            "structure": self.structure,
            "label": self.label,
            "derivatives": self.derivatives,
            "color": self.color,
            "mass_dimension": str(self.mass_dimension),
            "parity_sign": self.parity_sign,
            "charge_conjugation_sign": self.charge_conjugation_sign,
            "pyqcd_gamma_index": self.pyqcd_gamma_index,
            "latex": self.latex(),
        }


def enumerate_bilinear_operators(
    flavors: Sequence[str],
    structures: Iterable[str] | None = None,
    derivatives: int = 0,
    color: str = "singlet",
) -> Tuple[BilinearOperator, ...]:
    """枚举味对与 Dirac 结构的双线性算符。

    结构名缺省为全部 16 个；味对包含同味与不同味的有序组合。
    """

    if not flavors:
        raise ValueError("at least one flavor is required")
    selected = (
        tuple(dirac_bilinear_structures())
        if structures is None
        else tuple(structures)
    )
    operators = []
    for left in flavors:
        for right in flavors:
            for structure in selected:
                operators.append(
                    BilinearOperator(
                        name=f"{left}_{right}_{structure}",
                        left_flavor=left,
                        right_flavor=right,
                        structure=structure,
                        derivatives=derivatives,
                        color=color,
                    )
                )
    return tuple(operators)


def structure_summary() -> dict[str, object]:
    """返回结构层的机器可读摘要，供 CLI 审计使用。"""

    structures = dirac_bilinear_structures()
    labels = {
        label: sorted(
            name for name in structures if structure_label(name) == label
        )
        for label in DIRAC_STRUCTURE_LABELS
    }
    return {
        "count": len(structures),
        "labels": labels,
        "basis_rank": gamma_module.gamma_basis_rank(),
        "pyqcd_indices": {
            name: pyqcd_gamma_index(matrix)
            for name, matrix in structures.items()
        },
    }


__all__ = [
    "BilinearOperator",
    "COLOR_REPRESENTATIONS",
    "DIRAC_STRUCTURE_LABELS",
    "decompose_dirac_bilinear",
    "dirac_bilinear_structures",
    "enumerate_bilinear_operators",
    "operator_mass_dimension",
    "pyqcd_gamma_index",
    "reconstruct_dirac_bilinear",
    "structure_label",
    "structure_matrix",
    "structure_summary",
]
