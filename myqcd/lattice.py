"""格点动量、Fourier 相位与色散关系。"""

from __future__ import annotations

import cmath
import math
from typing import Sequence, Tuple

TAU = 2.0 * math.pi


def momentum_from_indices(
    indices: Sequence[int], extent: Sequence[int]
) -> Tuple[float, ...]:
    """把格点整数指标 ``n`` 转成 ``2 pi n / L`` 动量。"""

    if len(indices) != len(extent):
        raise ValueError("indices and extent must have the same length")
    if any(size <= 0 for size in extent):
        raise ValueError("extent entries must be positive")
    return tuple(
        TAU * index / size
        for index, size in zip(indices, extent)
    )


def momentum_squared(momentum: Sequence[float]) -> float:
    """返回 Euclidean ``sum_i p_i^2``。"""

    return sum(component * component for component in momentum)


def fourier_phase(
    momentum: Sequence[float], position: Sequence[int]
) -> complex:
    """返回 ``exp(-i p . x)``。"""

    if len(momentum) != len(position):
        raise ValueError("momentum and position lengths differ")
    return cmath.exp(
        -1j * sum(p * x for p, x in zip(momentum, position))
    )


def lattice_dispersion(
    momentum: Sequence[float], spacing: float = 1.0
) -> float:
    """返回格点色散 ``4/a^2 sum_i sin^2(p_i a/2)``。"""

    if spacing <= 0:
        raise ValueError("spacing must be positive")
    return (
        4.0
        / (spacing * spacing)
        * sum(
            math.sin(component * spacing / 2.0) ** 2
            for component in momentum
        )
    )


def continuum_dispersion(momentum: Sequence[float]) -> float:
    """返回连续色散 ``sum_i p_i^2``。"""

    return momentum_squared(momentum)


def spatial_momenta(
    extent: Sequence[int], *, max_index: int | None = None
) -> Tuple[Tuple[int, ...], ...]:
    """枚举空间动量指标（不含时间方向）。"""

    if not extent:
        raise ValueError("extent must be nonempty")
    limit = max_index if max_index is not None else max(extent) // 2
    if limit < 0:
        raise ValueError("max_index must be nonnegative")
    values = range(-limit, limit + 1)
    if len(extent) == 1:
        return tuple((value,) for value in values)
    if len(extent) == 2:
        return tuple((a, b) for a in values for b in values)
    if len(extent) == 3:
        return tuple(
            (a, b, c) for a in values for b in values for c in values
        )
    raise ValueError("only one to three spatial dimensions are supported")


def momentum_permutations(
    momentum: Sequence[float],
) -> Tuple[Tuple[float, ...], ...]:
    """返回动量分量的全部不同置换。"""

    import itertools

    unique = set(itertools.permutations(tuple(momentum)))
    return tuple(sorted(unique))


__all__ = [
    "TAU",
    "continuum_dispersion",
    "fourier_phase",
    "lattice_dispersion",
    "momentum_from_indices",
    "momentum_permutations",
    "momentum_squared",
    "spatial_momenta",
]
