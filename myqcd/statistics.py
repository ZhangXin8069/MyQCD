"""Jackknife、bootstrap 与有效质量估计（纯标准库）。"""

from __future__ import annotations

import math
import random
from statistics import mean
from typing import Sequence, Tuple


def jackknife_samples(
    samples: Sequence[Sequence[float]],
) -> Tuple[Tuple[float, ...], ...]:
    """返回 leave-one-out 样本。"""

    if len(samples) < 2:
        raise ValueError("jackknife requires at least two samples")
    width = len(samples[0])
    if any(len(sample) != width for sample in samples):
        raise ValueError("all samples must have the same dimension")
    total = tuple(
        sum(sample[index] for sample in samples)
        for index in range(width)
    )
    count = len(samples)
    return tuple(
        tuple(
            (total[index] - sample[index]) / (count - 1)
            for index in range(width)
        )
        for sample in samples
    )


def jackknife_mean(
    samples: Sequence[Sequence[float]],
) -> Tuple[float, ...]:
    """返回 jackknife 均值。"""

    return tuple(
        mean(values)
        for values in zip(*jackknife_samples(samples))
    )


def jackknife_covariance(
    samples: Sequence[Sequence[float]],
) -> Tuple[Tuple[float, ...], ...]:
    """返回 jackknife 协方差 ``(N-1)/N sum (x_i - mean)(x_j - mean)``。

    其中 ``x_i`` 是 leave-one-out 估计，``mean`` 是这些估计的均值。
    """

    if len(samples) < 2:
        raise ValueError("jackknife requires at least two samples")
    width = len(samples[0])
    jackknife = jackknife_samples(samples)
    mean_vector = tuple(
        sum(sample[index] for sample in jackknife) / len(jackknife)
        for index in range(width)
    )
    covariance = [[0.0] * width for _ in range(width)]
    for sample in jackknife:
        residual = tuple(
            sample[index] - mean_vector[index]
            for index in range(width)
        )
        for left in range(width):
            for right in range(width):
                covariance[left][right] += residual[left] * residual[right]
    factor = (len(samples) - 1) / len(samples)
    return tuple(
        tuple(factor * value for value in row)
        for row in covariance
    )


def bootstrap_indices(
    count: int, resamples: int, *, seed: int = 0
) -> Tuple[Tuple[int, ...], ...]:
    """返回确定性的 bootstrap 重采样指标。"""

    if count <= 0 or resamples <= 0:
        raise ValueError("count and resamples must be positive")
    generator = random.Random(seed)
    return tuple(
        tuple(generator.randrange(count) for _ in range(count))
        for _ in range(resamples)
    )


def bootstrap_mean(
    values: Sequence[float],
    resamples: int = 1000,
    *,
    seed: int = 0,
) -> dict[str, float]:
    """返回 bootstrap 均值与标准误。"""

    if not values:
        raise ValueError("values must be nonempty")
    indices = bootstrap_indices(len(values), resamples, seed=seed)
    means = [mean(values[index] for index in draw) for draw in indices]
    average = mean(means)
    variance = sum((value - average) ** 2 for value in means) / len(means)
    return {"mean": average, "stderr": math.sqrt(variance)}


def effective_mass(
    correlator: Sequence[float],
) -> Tuple[float, ...]:
    """返回相邻时间片的 ``log(C(t)/C(t+1))``。"""

    if len(correlator) < 2:
        raise ValueError("correlator needs at least two points")
    masses = []
    for current, following in zip(correlator, correlator[1:]):
        if current <= 0 or following <= 0:
            masses.append(float("nan"))
        else:
            masses.append(math.log(current / following))
    return tuple(masses)


__all__ = [
    "bootstrap_indices",
    "bootstrap_mean",
    "effective_mass",
    "jackknife_covariance",
    "jackknife_mean",
    "jackknife_samples",
]
