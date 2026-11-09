"""重正化投影器、Z 因子与混合矩阵测试。"""

import sympy as sp
import pytest

from myqcd import gamma, renormalization


def test_projector_table():
    projectors = renormalization.bilinear_projectors()
    assert len(projectors) == 16
    assert all(projector.matrix.shape == (4, 4) for projector in projectors.values())


def test_tree_level_self_projections():
    for name in renormalization.bilinear_projectors():
        assert sp.simplify(
            renormalization.tree_level_projection(name) - 1
        ) == 0


def test_cross_projections_vanish():
    projectors = renormalization.bilinear_projectors()
    assert sp.simplify(
        projectors["S"].projection(gamma.gamma(1))
    ) == 0
    assert sp.simplify(
        projectors["V1"].projection(gamma.gamma(2))
    ) == 0


def test_z_factor():
    assert renormalization.z_factor(sp.Integer(2), sp.Integer(4)) == sp.Rational(1, 2)
    with pytest.raises(ValueError):
        renormalization.z_factor(1, 0)


def test_anomalous_dimension():
    mu = sp.Symbol("mu", positive=True)
    gamma_value = sp.Symbol("gamma", real=True)
    z = mu**gamma_value
    assert sp.simplify(
        renormalization.anomalous_dimension(z, mu) + gamma_value
    ) == 0


def test_mixing_matrix():
    assert renormalization.mixing_matrix_is_invertible(sp.eye(3))
    assert not renormalization.mixing_matrix_is_invertible(
        sp.Matrix([[1, 2], [2, 4]])
    )
    with pytest.raises(ValueError):
        renormalization.mixing_matrix_is_invertible(sp.Matrix([[1, 2, 3]]))
    assert renormalization.identity_z_matrix(3) == sp.eye(3)


def test_projector_table_serialization():
    table = renormalization.projector_table()
    assert len(table) == 16
    assert all("normalization" in row for row in table)
