"""QCD 传播子、Ward 恒等式与顶点规则测试。"""

import sympy as sp
import pytest

from myqcd import gamma, lorentz, qcd_rules


def _momentum(prefix="p"):
    return lorentz.vector_components(prefix)


def test_quark_propagator_inverse():
    momentum = _momentum()
    mass = sp.Symbol("m", positive=True)
    assert qcd_rules.quark_propagator_residual(momentum, mass).is_zero_matrix


def test_ward_identity():
    assert qcd_rules.ward_identity_residual(_momentum()).is_zero_matrix


def test_gluon_transversality_in_landau_gauge():
    momentum = _momentum()
    assert all(
        qcd_rules.gluon_transversality(momentum, nu, gauge_parameter=0) == 0
        for nu in range(4)
    )


def test_gluon_feynman_gauge_not_transverse():
    momentum = _momentum()
    p2 = lorentz.contract_vectors(momentum, momentum)
    for nu in range(4):
        value = qcd_rules.gluon_transversality(
            momentum, nu, gauge_parameter=1
        )
        assert sp.simplify(value - momentum[nu] / p2) == 0


def test_ghost_propagator():
    momentum = _momentum()
    p2 = lorentz.contract_vectors(momentum, momentum)
    assert sp.simplify(qcd_rules.ghost_propagator(momentum) - 1 / p2) == 0


def test_three_gluon_lorentz_is_nonzero():
    k1 = _momentum("k1")
    k2 = _momentum("k2")
    k3 = tuple(-k1[index] - k2[index] for index in range(4))
    value = qcd_rules.three_gluon_lorentz(k1, k2, k3, 0, 1, 0)
    assert sp.simplify(value) != 0


def test_vertex_catalog():
    rules = qcd_rules.gluon_vertex_factors()
    assert len(rules) == 4
    assert {rule.name for rule in rules} == {
        "quark-antiquark-gluon",
        "three-gluon",
        "four-gluon",
        "ghost-antighost-gluon",
    }
    assert rules[0].mass_dimension == 0
    assert rules[1].mass_dimension == 1
    assert rules[2].coupling_power == 2


def test_rule_audit():
    audit = qcd_rules.rule_audit()
    assert audit["vertex_count"] == 4
    assert len(audit["four_gluon_colors"]) == 3
    assert audit["propagator_dimensions"] == {
        "quark": -1,
        "gluon": -2,
        "ghost": -2,
    }


def test_zero_momentum_rejected():
    zero = (sp.Integer(0),) * 4
    with pytest.raises(ValueError):
        qcd_rules.quark_propagator(zero, sp.Integer(0))
    with pytest.raises(ValueError):
        qcd_rules.gluon_propagator(zero, 0, 1)
    with pytest.raises(ValueError):
        qcd_rules.ghost_propagator(zero)
