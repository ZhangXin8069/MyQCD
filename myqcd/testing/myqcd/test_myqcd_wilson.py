"""Wilson 路径与规范协变性测试。"""

import sympy as sp
import pytest

from myqcd import wilson


def _diagonal_phases(values):
    return sp.diag(*[sp.exp(sp.I * value) for value in values])


def test_path_product_and_dagger():
    u0 = sp.diag(1, 1, -1)
    u1 = sp.diag(1, -1, 1)
    path = wilson.straight_path((u0, u1))
    assert path.product() == u0 * u1
    assert path.dagger().product() == u1.H * u0.H
    assert (path.dagger().product() - path.product().H).is_zero_matrix


def test_gauge_covariance_with_diagonal_phases():
    angles = (sp.Rational(1, 5), sp.Rational(2, 5), sp.Rational(3, 5))
    links = tuple(_diagonal_phases(angles) for _ in range(3))
    gauges = tuple(
        _diagonal_phases((sp.Rational(i, 7), sp.Rational(i + 1, 7), sp.Rational(i + 2, 7)))
        for i in range(4)
    )
    residual = wilson.covariance_residual(links, gauges)
    assert residual.is_zero_matrix


def test_dagger_path_audit():
    path = wilson.straight_path(
        (sp.diag(1, 1, -1), sp.diag(-1, 1, 1))
    )
    audit = wilson.path_audit(path)
    assert audit["link_count"] == 2
    assert audit["shape"] == (3, 3)


def test_staple_descriptors():
    assert wilson.staple_descriptors(2, 1, 5) == (
        ("z", -5),
        ("b", 1),
        ("z", 7),
    )
    with pytest.raises(ValueError):
        wilson.staple_descriptors(1, 1, 5)
    with pytest.raises(ValueError):
        wilson.staple_descriptors(2, 1, 0)


def test_unitary_phases_and_validation():
    matrix = wilson.unitary_phases((0, sp.pi / 2, sp.pi))
    assert (matrix * matrix.H - sp.eye(3)).is_zero_matrix
    with pytest.raises(ValueError):
        wilson.unitary_phases((0, 0))
    with pytest.raises(ValueError):
        wilson.WilsonPath(())
    with pytest.raises(ValueError):
        wilson.WilsonPath((sp.eye(2),))


def test_transformed_links_length():
    links = (sp.eye(3),)
    gauges = (sp.eye(3), sp.eye(3))
    assert len(wilson.transformed_links(links, gauges)) == 1
    with pytest.raises(ValueError):
        wilson.transformed_links(links, (sp.eye(3),))
