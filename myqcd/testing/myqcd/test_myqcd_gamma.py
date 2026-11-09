"""Euclidean gamma 代数测试。"""

import sympy as sp
import pytest

from myqcd import gamma


def test_gamma5_matches_dr_diagonal():
    assert gamma.gamma5() == sp.diag(1, 1, -1, -1)


def test_gamma_index_rejects_out_of_range():
    with pytest.raises(ValueError):
        gamma.gamma(18)
    with pytest.raises(ValueError):
        gamma.gamma(-1)


def test_gamma_index_rejects_non_int():
    with pytest.raises(TypeError):
        gamma.gamma(1.5)


def test_clifford_algebra():
    assert all(
        gamma.clifford_residual(mu, nu).is_zero_matrix
        for mu in range(1, 5)
        for nu in range(1, 5)
    )


@pytest.mark.parametrize(
    "indices",
    [
        (1, 1, 1, 1),
        (1, 2, 1, 2),
        (1, 2, 2, 1),
        (1, 2, 3, 4),
        (1, 2, 3, 4, 1, 2),
    ],
)
def test_trace_theorem_matches_explicit_matrix(indices):
    explicit = gamma.dirac_trace(
        sp.prod([gamma.gamma(index) for index in indices])
    )
    assert sp.simplify(gamma.trace_gamma_product(indices) - explicit) == 0


def test_odd_trace_is_zero():
    assert gamma.trace_gamma_product((1, 2, 3)) == 0
    assert gamma.trace_gamma_product((1,)) == 0


def test_trace_two_gammas():
    assert gamma.trace_gamma_product((1, 1)) == 4
    assert gamma.trace_gamma_product((1, 2)) == 0


def test_basis_is_complete():
    assert gamma.gamma_basis_rank() == 16
    gram = gamma.gamma_basis_gram()
    assert gram.shape == (16, 16)
    assert all(
        sp.simplify(gram[left, right]) == 0
        for left in range(16)
        for right in range(16)
        if left != right
    )


def test_charge_conjugation_transpose_relation():
    conjugation = gamma.charge_conjugation_matrix()
    assert all(
        (
            conjugation * gamma.gamma(mu) * conjugation.H
            + gamma.gamma(mu).T
        ).is_zero_matrix
        for mu in range(1, 5)
    )


def test_parity_projectors_are_complete_and_idempotent():
    plus, minus = gamma.parity_projectors()
    identity = gamma.identity()
    assert (plus * plus - plus).is_zero_matrix
    assert (minus * minus - minus).is_zero_matrix
    assert (plus * minus).is_zero_matrix
    assert (plus + minus - identity).is_zero_matrix


def test_gamma_properties_known_signs():
    properties = gamma.gamma_properties()
    assert properties["gamma_5"] == {"H": 1, "T": 1, "C": 1}
    assert properties["gamma_1"] == {"H": 1, "T": -1, "C": 1}


def test_dirac_slash_is_linear_combination():
    momentum = sp.symbols("p1:5")
    expected = sum(
        (momentum[index] * gamma.gamma(index + 1) for index in range(4)),
        sp.zeros(4),
    )
    assert sp.expand(gamma.dirac_slash(momentum) - expected) == sp.zeros(4)


def test_dirac_slash_requires_four_components():
    with pytest.raises(ValueError):
        gamma.dirac_slash((1, 2, 3))
