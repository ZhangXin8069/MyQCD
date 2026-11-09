"""Dirac 双线性算符构建测试。"""

import sympy as sp
import pytest

from myqcd import gamma, operators


def test_structure_count_and_classification():
    structures = operators.dirac_bilinear_structures()
    assert len(structures) == 16
    counts = {
        label: sum(
            operators.structure_label(name) == label
            for name in structures
        )
        for label in operators.DIRAC_STRUCTURE_LABELS
    }
    assert counts == {"S": 1, "P": 1, "V": 4, "A": 4, "T": 6}


def test_decomposition_roundtrip():
    for matrix in operators.dirac_bilinear_structures().values():
        coefficients = operators.decompose_dirac_bilinear(matrix)
        rebuilt = operators.reconstruct_dirac_bilinear(coefficients)
        assert (rebuilt - matrix).is_zero_matrix


def test_decomposition_of_gamma_product():
    matrix = gamma.gamma(1) * gamma.gamma(2)
    coefficients = operators.decompose_dirac_bilinear(matrix)
    assert sp.simplify(coefficients["T12"] - 1) == 0
    assert all(
        sp.simplify(value) == 0
        for name, value in coefficients.items()
        if name != "T12"
    )


def test_pyqcd_index_mapping():
    assert operators.pyqcd_gamma_index(gamma.identity()) == 0
    assert operators.pyqcd_gamma_index(gamma.gamma5()) == 5
    assert operators.pyqcd_gamma_index(gamma.gamma(4)) == 4
    assert operators.pyqcd_gamma_index(gamma.sigma(2, 3)) == 6
    assert operators.pyqcd_gamma_index(gamma.sigma(1, 3)) is None


def test_bilinear_operator_fields():
    operator = operators.BilinearOperator(
        name="O_V4",
        left_flavor="u",
        right_flavor="d",
        structure="V4",
    )
    assert operator.label == "V"
    assert operator.mass_dimension == 3
    assert operator.parity_sign == 1
    assert operator.pyqcd_gamma_index == 4
    assert "\\bar{q}_{u}" in operator.latex()
    assert operator.to_dict()["structure"] == "V4"


def test_bilinear_operator_invalid_inputs():
    with pytest.raises(ValueError):
        operators.BilinearOperator("x", "u", "d", "unknown")
    with pytest.raises(ValueError):
        operators.BilinearOperator("x", "u", "d", "S", color="triplet")
    with pytest.raises(ValueError):
        operators.BilinearOperator("x", "u", "d", "S", derivatives=-1)


def test_operator_mass_dimension_counts():
    assert operators.operator_mass_dimension() == 3
    assert operators.operator_mass_dimension(derivatives=2) == 5
    assert operators.operator_mass_dimension(gluon_field_strengths=1) == 5


def test_enumerate_bilinear_operators():
    selected = operators.enumerate_bilinear_operators(
        ("u", "d"), structures=("S", "V4")
    )
    assert len(selected) == 2 * 2 * 2
    names = {operator.name for operator in selected}
    assert "u_d_S" in names
    assert "d_u_V4" in names


def test_structure_summary_maps_pyqcd_indices():
    summary = operators.structure_summary()
    assert summary["count"] == 16
    assert summary["basis_rank"] == 16
    assert summary["pyqcd_indices"]["S"] == 0
    assert summary["pyqcd_indices"]["P"] == 5
