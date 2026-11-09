"""Jackknife/bootstrap 与有效质量测试。"""

import math

import pytest

from myqcd import statistics


def test_jackknife_samples_and_mean():
    samples = [(1.0, 2.0), (2.0, 4.0), (3.0, 6.0)]
    jackknife = statistics.jackknife_samples(samples)
    assert len(jackknife) == 3
    assert jackknife[0] == pytest.approx((2.5, 5.0))
    assert statistics.jackknife_mean(samples) == pytest.approx((2.0, 4.0))


def test_jackknife_covariance_matches_direct_formula():
    samples = [(1.0, 2.0), (2.0, 4.0), (3.0, 6.0), (4.0, 8.0)]
    covariance = statistics.jackknife_covariance(samples)
    average = (2.5, 5.0)
    direct = [[0.0, 0.0], [0.0, 0.0]]
    for sample in samples:
        dx = sample[0] - average[0]
        dy = sample[1] - average[1]
        direct[0][0] += dx * dx
        direct[0][1] += dx * dy
        direct[1][0] += dx * dy
        direct[1][1] += dy * dy
    factor = 1.0 / (len(samples) * (len(samples) - 1))
    expected = [[factor * direct[i][j] for j in range(2)] for i in range(2)]
    for i in range(2):
        for j in range(2):
            assert covariance[i][j] == pytest.approx(expected[i][j])


def test_bootstrap_is_deterministic():
    values = [1.0, 2.0, 3.0, 4.0]
    first = statistics.bootstrap_indices(4, 10, seed=7)
    second = statistics.bootstrap_indices(4, 10, seed=7)
    assert first == second
    assert len(first) == 10
    assert all(len(draw) == 4 for draw in first)


def test_bootstrap_mean():
    result = statistics.bootstrap_mean([1.0, 2.0, 3.0, 4.0], 100, seed=3)
    assert result["mean"] == pytest.approx(2.5, abs=0.5)
    assert result["stderr"] >= 0


def test_effective_mass():
    correlator = [math.exp(-1.0 * time) for time in range(5)]
    masses = statistics.effective_mass(correlator)
    assert len(masses) == 4
    assert all(mass == pytest.approx(1.0) for mass in masses)


def test_validation():
    with pytest.raises(ValueError):
        statistics.jackknife_samples([(1.0,)])
    with pytest.raises(ValueError):
        statistics.jackknife_samples([(1.0,), (1.0, 2.0)])
    with pytest.raises(ValueError):
        statistics.bootstrap_indices(0, 1)
    with pytest.raises(ValueError):
        statistics.effective_mass([1.0])
