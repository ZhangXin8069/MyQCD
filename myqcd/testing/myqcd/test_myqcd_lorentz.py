"""Lorentz 张量代数与投影测试。"""

import sympy as sp

from myqcd import lorentz


def test_metric_is_euclidean():
    assert lorentz.metric() == sp.eye(4)
    assert lorentz.contract_vectors((1, 0, 0, 0), (1, 0, 0, 0)) == 1
    assert lorentz.contract_vectors((1, 2, 3, 4), (4, 3, 2, 1)) == 20


def test_epsilon_square_and_double_contraction():
    assert lorentz.epsilon_square() == 24
    assert lorentz.epsilon_two_contract_residual() == 0
    assert lorentz.epsilon_two_contract(0, 1, 0, 1) == 2
    assert lorentz.epsilon_two_contract(0, 1, 1, 0) == -2


def test_epsilon_four_contraction_is_determinant():
    assert lorentz.epsilon_four_contract(0, 1, 2, 3, 0, 1, 2, 3) == 1
    assert lorentz.epsilon_four_contract(0, 1, 2, 3, 1, 0, 2, 3) == -1
    assert lorentz.epsilon_four_contract(0, 0, 2, 3, 0, 1, 2, 3) == 0


def test_schouten_identity_is_exact():
    momentum = lorentz.vector_components("p")
    assert lorentz.schouten_residual(momentum) == 0


def test_transverse_projector_is_idempotent_and_transverse():
    momentum = lorentz.vector_components("p")

    def projector(mu, nu):
        return lorentz.transverse_projector(momentum, mu, nu)

    assert sp.simplify(
        sum(projector(0, nu) * projector(nu, 2) for nu in range(4))
        - projector(0, 2)
    ) == 0
    assert all(
        sp.simplify(sum(momentum[mu] * projector(mu, nu) for mu in range(4)))
        == 0
        for nu in range(4)
    )


def test_longitudinal_plus_transverse_is_identity():
    momentum = lorentz.vector_components("p")
    for mu in range(4):
        for nu in range(4):
            total = (
                lorentz.transverse_projector(momentum, mu, nu)
                + lorentz.longitudinal_projector(momentum, mu, nu)
            )
            assert sp.simplify(total - sp.KroneckerDelta(mu, nu)) == 0


def test_spin2_projector_is_transverse_traceless_and_symmetric():
    momentum = lorentz.vector_components("p")
    assert lorentz.spin2_traceless_check(momentum) == 0
    assert lorentz.spin2_dimension(momentum) == 5
    assert sp.simplify(
        lorentz.transverse_traceless_spin2(momentum, 0, 1, 2, 3)
        - lorentz.transverse_traceless_spin2(momentum, 2, 3, 0, 1)
    ) == 0
    assert all(
        sp.simplify(
            sum(
                momentum[mu]
                * lorentz.transverse_traceless_spin2(
                    momentum, mu, nu, 2, 3
                )
                for mu in range(4)
            )
        )
        == 0
        for nu in range(4)
    )


def test_projector_rejects_zero_momentum():
    zero = (sp.Integer(0),) * 4
    import pytest

    with pytest.raises(ValueError):
        lorentz.transverse_projector(zero, 0, 1)
