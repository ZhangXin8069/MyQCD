"""Wilson 路径、链接乘积与规范协变性。"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence, Tuple

import sympy as sp

from . import color


@dataclass(frozen=True)
class WilsonPath:
    """按路径顺序排列的规范链接乘积。"""

    links: Tuple[sp.Matrix, ...]
    name: str = ""

    def __post_init__(self) -> None:
        if not self.links:
            raise ValueError("Wilson path must contain at least one link")
        for link in self.links:
            if link.shape != (3, 3):
                raise ValueError("links must be 3x3 matrices")

    def product(self) -> sp.Matrix:
        """返回按路径顺序的矩阵乘积 ``U0 U1 ...``。"""

        result = sp.eye(3)
        for link in self.links:
            result = result * link
        return sp.expand(result)

    def dagger(self) -> "WilsonPath":
        """返回共轭路径：反向并逐链接取厄米共轭。"""

        return WilsonPath(
            links=tuple(link.H for link in reversed(self.links)),
            name=f"{self.name}^dagger" if self.name else "",
        )

    def gauge_transformed(
        self, start: sp.Matrix, end: sp.Matrix
    ) -> sp.Matrix:
        """返回 ``G_start W G_end^dagger``。"""

        return sp.expand(start * self.product() * end.H)

    def to_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "link_count": len(self.links),
            "product": str(self.product()),
        }


def straight_path(links: Iterable[sp.Matrix], name: str = "straight") -> WilsonPath:
    """构造直线 Wilson 路径。"""

    return WilsonPath(tuple(sp.Matrix(link) for link in links), name=name)


def transformed_links(
    links: Sequence[sp.Matrix],
    gauge_matrices: Sequence[sp.Matrix],
) -> Tuple[sp.Matrix, ...]:
    """返回 ``G_i U_i G_{i+1}^dagger`` 的链接序列。

    ``gauge_matrices`` 需要有 ``len(links)+1`` 个端点变换。
    """

    if len(gauge_matrices) != len(links) + 1:
        raise ValueError("need one extra gauge matrix for the endpoint")
    return tuple(
        sp.expand(gauge_matrices[index] * link * gauge_matrices[index + 1].H)
        for index, link in enumerate(links)
    )


def covariance_residual(
    links: Sequence[sp.Matrix],
    gauge_matrices: Sequence[sp.Matrix],
) -> sp.Matrix:
    """返回变换后路径与 ``G_start W G_end^dagger`` 的差。"""

    path = straight_path(links)
    transformed = straight_path(
        transformed_links(links, gauge_matrices),
        name="transformed",
    )
    expected = path.gauge_transformed(
        gauge_matrices[0], gauge_matrices[-1]
    )
    return sp.simplify(transformed.product() - expected)


def staple_descriptors(z: int, b: int, length: int) -> Tuple[Tuple[str, int], ...]:
    """返回三段 staple 路径的方向/长度描述。"""

    if length <= 0:
        raise ValueError("length must be positive")
    if z == b:
        raise ValueError("staple requires distinct directions")
    return (
        ("z", -length),
        ("b", b),
        ("z", length + z),
    )


def unitary_phases(angles: Sequence[sp.Expr]) -> sp.Matrix:
    """由三个相位构造 3x3 对角幺正矩阵。"""

    if len(angles) != color.N_COLORS:
        raise ValueError("expected three angles")
    return sp.diag(
        *[sp.exp(sp.I * sp.sympify(angle)) for angle in angles]
    )


def path_audit(path: WilsonPath) -> dict[str, object]:
    """返回路径的尺寸与可逆性摘要。"""

    product = path.product()
    determinant = sp.simplify(product.det())
    return {
        "link_count": len(path.links),
        "shape": product.shape,
        "determinant": str(determinant),
        "reversible": determinant != 0,
    }


__all__ = [
    "WilsonPath",
    "covariance_residual",
    "path_audit",
    "staple_descriptors",
    "straight_path",
    "transformed_links",
    "unitary_phases",
]
