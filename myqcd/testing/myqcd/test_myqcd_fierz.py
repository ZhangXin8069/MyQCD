"""通用 Dirac Fierz 变换测试。"""

import random

import sympy as sp
import pytest

from myqcd import fierz


def _spinors(seed: int = 11):
    random.seed(seed)
    return [
        [
            complex(random.uniform(-1, 1), random.uniform(-1, 1))
            for _ in range(4)
        ]
        for _ in range(4)
    ]


def test_dual_completeness_relation():
    for i in range(4):
        for j in range(4):
            for k in range(4):
                for l in range(4):
                    total = sum(
                        fierz.basis_matrix(name)[i, j]
                        * fierz.dual_basis_matrix(name)[k, l]
                        for name in fierz.BASIS_NAMES
                    )
                    expected = 4 * (
                        1 if i == l else 0
                    ) * (1 if k == j else 0)
                    assert sp.simplify(total - expected) == 0


@pytest.mark.parametrize(
    "pair",
    [
        ("S", "S"),
        ("P", "P"),
        ("V1", "V1"),
        ("A1", "A1"),
        ("T12", "T12"),
        ("S", "V1"),
        ("V1", "V2"),
        ("P", "T12"),
        ("A2", "T34"),
    ],
)
def test_matrix_identity(pair):
    left, right = pair
    coefficients = fierz.fierz_transform(left, right)
    left_matrix = fierz.basis_matrix(left)
    right_matrix = fierz.basis_matrix(right)
    for i in range(4):
        for j in range(4):
            for k in range(4):
                for l in range(4):
                    lhs = left_matrix[i, j] * right_matrix[k, l]
                    rhs = sum(
                        coefficient
                        * fierz.basis_matrix(left_name)[i, l]
                        * fierz.basis_matrix(right_name)[k, j]
                        for (left_name, right_name), coefficient
                        in coefficients.items()
                    )
                    assert sp.simplify(lhs - rhs) == 0


@pytest.mark.parametrize(
    "pair",
    [
        ("S", "S"),
        ("P", "P"),
        ("V1", "V1"),
        ("A1", "A1"),
        ("T12", "T12"),
        ("S", "V1"),
        ("V1", "V2"),
        ("P", "T12"),
    ],
)
def test_spinor_residual(pair):
    residual = fierz.fierz_residual(*pair, _spinors())
    assert abs(residual) < 1e-9


def test_scalar_scalar_coefficients():
    coefficients = fierz.fierz_transform("S", "S")
    assert coefficients[("S", "S")] == sp.Rational(1, 4)
    assert coefficients[("V1", "V1")] == sp.Rational(1, 4)
    assert coefficients[("A1", "A1")] == -sp.Rational(1, 4)
    assert coefficients[("T12", "T12")] == -sp.Rational(1, 4)


def test_common_identities_are_nonempty():
    identities = fierz.common_identities()
    assert set(identities) == {"S-S", "P-P", "V1-V1", "A1-A1", "T12-T12"}
    assert all(identities.values())


def test_unknown_basis_element_rejected():
    with pytest.raises(ValueError):
        fierz.basis_matrix("unknown")
    with pytest.raises(ValueError):
        fierz.fierz_transform("S", "unknown")


def test_expand_in_basis_roundtrip():
    matrix = fierz.basis_matrix("V1") + 2 * fierz.basis_matrix("T12")
    coefficients = fierz.expand_in_basis(matrix)
    rebuilt = sum(
        (
            coefficient * fierz.basis_matrix(name)
            for name, coefficient in coefficients.items()
        ),
        sp.zeros(4),
    )
    assert (sp.expand(rebuilt - matrix)).is_zero_matrix
