"""格点动量、相位与色散测试。"""

import cmath
import math

import pytest

from myqcd import lattice


def test_momentum_from_indices():
    momentum = lattice.momentum_from_indices((1, -1), (4, 8))
    assert momentum[0] == pytest.approx(math.pi / 2)
    assert momentum[1] == pytest.approx(-math.pi / 4)


def test_fourier_phase():
    phase = lattice.fourier_phase((math.pi / 2, 0), (1, 0))
    assert phase == pytest.approx(-1j)


def test_dispersion_limits():
    momentum = (0.1, 0.2, 0.3, 0.4)
    lattice_value = lattice.lattice_dispersion(momentum, spacing=1.0)
    continuum_value = lattice.continuum_dispersion(momentum)
    assert 0 < lattice_value < continuum_value
    assert lattice.lattice_dispersion((0.0,)) == 0


def test_spatial_momenta_counts():
    assert len(lattice.spatial_momenta((4,), max_index=2)) == 5
    assert len(lattice.spatial_momenta((4, 4), max_index=1)) == 9
    assert len(lattice.spatial_momenta((4, 4, 4), max_index=1)) == 27


def test_momentum_permutations():
    permutations = lattice.momentum_permutations((1.0, 0.0, 0.0))
    assert (1.0, 0.0, 0.0) in permutations
    assert (0.0, 1.0, 0.0) in permutations
    assert len(permutations) == 3


def test_validation():
    with pytest.raises(ValueError):
        lattice.momentum_from_indices((1,), (4, 8))
    with pytest.raises(ValueError):
        lattice.fourier_phase((1.0,), (0, 1))
    with pytest.raises(ValueError):
        lattice.lattice_dispersion((1.0,), spacing=0)
    with pytest.raises(ValueError):
        lattice.spatial_momenta(())
