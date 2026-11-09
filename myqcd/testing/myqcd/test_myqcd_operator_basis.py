"""算符基、手征组合与颜色表示测试。"""

import sympy as sp
import pytest

from myqcd import gamma, operator_basis, operators


def test_derivative_operator_mass_dimension():
    operator = operator_basis.DerivativeOperator(
        "O", "V3", derivatives=2, color="octet"
    )
    assert operator.mass_dimension == 5
    assert operator.label == "V"
    assert operator.pyqcd_gamma_index == 3
    assert "D^{2}" in operator.latex()
    assert operator.to_dict()["color"] == "octet"


def test_enumerate_counts_all_combinations():
    operators_list = operator_basis.enumerate_derivative_operators(
        ("u", "d"), max_derivatives=2, colors=("singlet", "octet")
    )
    assert len(operators_list) == 2 * 2 * 16 * 3 * 2


def test_chiral_structures_are_projectors():
    structures = operator_basis.chiral_bilinear_structures(3)
    left, right = gamma.chiral_projectors()
    gamma_mu = gamma.gamma(3)
    assert (
        sp.expand(structures["LL"] + structures["LR"])
        - sp.expand(left * gamma_mu)
    ).is_zero_matrix
    assert (
        sp.expand(structures["RR"] + structures["RL"])
        - sp.expand(right * gamma_mu)
    ).is_zero_matrix


def test_vector_axial_combinations():
    combinations = operator_basis.vector_axial_combinations(4)
    left, right = gamma.chiral_projectors()
    gamma_mu = gamma.gamma(4)
    assert (
        combinations["V+A"] - sp.expand(2 * gamma_mu * right)
    ).is_zero_matrix
    assert (
        combinations["V-A"] - sp.expand(2 * gamma_mu * left)
    ).is_zero_matrix


def test_chiral_projector_identities():
    checks = operator_basis.chiral_projector_identities()
    assert checks
    assert all(checks.values())


def test_color_factor_labels():
    assert operator_basis.color_factor("singlet") == "1"
    assert operator_basis.color_factor("octet", 3) == "T^3"
    with pytest.raises(ValueError):
        operator_basis.color_factor("octet")
    with pytest.raises(ValueError):
        operator_basis.color_factor("singlet", 1)


def test_fierz_rearrangement_is_nonempty():
    terms = operator_basis.fierz_rearrangement("S", "V1")
    assert terms
    assert any(coefficient != 0 for _, _, coefficient in terms)


def test_operator_table_serialization():
    table = operator_basis.operator_table(
        max_derivatives=1, flavors=("u",), colors=("singlet",)
    )
    assert len(table) == 16 * 2
    assert all("latex" in row for row in table)
    assert all("mass_dimension" in row for row in table)


def test_quantum_number_summary():
    summary = operator_basis.quantum_number_summary()
    assert summary["count"] == 16
    assert summary["labels"]["S"] == ("S",)
    assert summary["derivative_dimension"][0] == "3"


def test_invalid_operator_inputs():
    with pytest.raises(ValueError):
        operator_basis.DerivativeOperator("x", "unknown")
    with pytest.raises(ValueError):
        operator_basis.DerivativeOperator("x", "S", derivatives=-1)
    with pytest.raises(ValueError):
        operator_basis.DerivativeOperator("x", "S", color="triplet")
    with pytest.raises(ValueError):
        operator_basis.enumerate_derivative_operators(("u",), max_derivatives=-1)
