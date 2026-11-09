"""RI/MOM 投影器、Z 因子与混合矩阵代数。"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence, Tuple

import sympy as sp

from . import gamma, operators


@dataclass(frozen=True)
class DiracProjector:
    """一个双线性投影器及其归一化。"""

    name: str
    matrix: sp.Matrix
    normalization: sp.Expr

    def __post_init__(self) -> None:
        if self.matrix.shape != (4, 4):
            raise ValueError("projector must be a 4x4 matrix")
        if sp.simplify(self.normalization) == 0:
            raise ValueError("projector normalization must be nonzero")

    def projection(self, vertex: sp.MatrixBase) -> sp.Expr:
        """返回 ``Tr[P vertex] / Tr[P P]``。"""

        vertex = sp.Matrix(vertex)
        if vertex.shape != (4, 4):
            raise ValueError("vertex must be a 4x4 matrix")
        return sp.simplify(
            gamma.dirac_trace(self.matrix * vertex) / self.normalization
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "normalization": str(self.normalization),
        }


def bilinear_projectors() -> Mapping[str, DiracProjector]:
    """返回 16 个双线性投影器。"""

    result = {}
    for name, matrix in operators.dirac_bilinear_structures().items():
        result[name] = DiracProjector(
            name=name,
            matrix=matrix,
            normalization=gamma.dirac_trace(matrix * matrix),
        )
    return result


def tree_level_projection(
    projector_name: str, vertex: sp.MatrixBase | None = None
) -> sp.Expr:
    """返回树级投影；缺省顶点等于投影器自身。"""

    projectors = bilinear_projectors()
    if projector_name not in projectors:
        raise ValueError(f"unknown projector {projector_name!r}")
    projector = projectors[projector_name]
    vertex = projector.matrix if vertex is None else vertex
    return projector.projection(vertex)


def z_factor(tree_value: sp.Expr, loop_value: sp.Expr) -> sp.Expr:
    """由 RI/MOM 条件 ``Z * loop = tree`` 解出 ``Z``。"""

    loop_value = sp.sympify(loop_value)
    if sp.simplify(loop_value) == 0:
        raise ValueError("loop projection must be nonzero")
    return sp.simplify(sp.sympify(tree_value) / loop_value)


def anomalous_dimension(z: sp.Expr, mu: sp.Symbol) -> sp.Expr:
    """返回 ``gamma = - d log Z / d log mu``。"""

    z = sp.sympify(z)
    if sp.simplify(z) == 0:
        raise ValueError("Z must be nonzero")
    return sp.simplify(-mu * sp.diff(sp.log(z), mu))


def mixing_matrix_is_invertible(matrix: sp.MatrixBase) -> bool:
    """检查混合矩阵是否可逆。"""

    matrix = sp.Matrix(matrix)
    if matrix.rows != matrix.cols:
        raise ValueError("mixing matrix must be square")
    return sp.simplify(matrix.det()) != 0


def identity_z_matrix(dimension: int) -> sp.Matrix:
    """返回树级单位混合矩阵。"""

    if dimension <= 0:
        raise ValueError("dimension must be positive")
    return sp.eye(dimension)


def projector_table() -> Tuple[dict[str, object], ...]:
    """返回投影器表。"""

    return tuple(
        projector.to_dict()
        for projector in bilinear_projectors().values()
    )


__all__ = [
    "DiracProjector",
    "anomalous_dimension",
    "bilinear_projectors",
    "identity_z_matrix",
    "mixing_matrix_is_invertible",
    "projector_table",
    "tree_level_projection",
    "z_factor",
]
