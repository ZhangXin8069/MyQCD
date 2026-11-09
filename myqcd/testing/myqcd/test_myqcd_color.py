"""SU(3) 颜色代数测试。"""

import sympy as sp

from myqcd import color


def test_generators_are_hermitian_and_traceless():
    for generator in color.generators():
        assert (generator - generator.H).is_zero_matrix
        assert sp.simplify(sp.trace(generator)) == 0


def test_fundamental_trace_normalization():
    assert color.fundamental_trace(1, 1) == sp.Rational(1, 2)
    assert color.fundamental_trace(1, 2) == 0


def test_structure_constants_known_values():
    f = color.structure_constants()
    assert f[0][1][2] == 1
    assert f[0][3][6] == sp.Rational(1, 2)
    assert sp.simplify(f[3][4][7] - sp.sqrt(3) / 2) == 0


def test_structure_constants_are_antisymmetric():
    f = color.structure_constants()
    assert all(
        sp.simplify(f[a][b][c] + f[b][a][c]) == 0
        for a in range(8)
        for b in range(8)
        for c in range(8)
    )


def test_symmetric_constants_known_values():
    d = color.symmetric_constants()
    assert sp.simplify(d[0][0][7] - sp.sqrt(3) / 3) == 0
    assert d[0][3][5] == sp.Rational(1, 2)


def test_casimir_invariants():
    assert color.casimir_fundamental() == sp.Rational(4, 3)
    assert color.casimir_adjoint() == 3
    assert color.adjoint_trace(1, 1) == 3
    assert color.adjoint_trace(1, 2) == 0


def test_color_fierz_identity():
    assert color.color_fierz_residual() == 0


def test_quark_gluon_vertex_is_generator():
    assert color.quark_gluon_vertex(1) == color.generators()[0]


def test_generator_index_validation():
    import pytest

    with pytest.raises(ValueError):
        color.quark_gluon_vertex(9)


def test_epsilon_tensor_values():
    epsilon = color.epsilon_tensor()
    assert epsilon[0, 1, 2] == 1
    assert epsilon[2, 1, 0] == -1
    assert epsilon[0, 0, 1] == 0
