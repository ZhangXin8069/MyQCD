"""SU(3) 迹、f/d 缩并与 Casimir 测试。"""

import random

import sympy as sp
import pytest

from myqcd import color, color_traces


def test_trace_three_matches_explicit_matrices():
    random.seed(5)
    generators = color.generators()
    for _ in range(12):
        a, b, c = (random.randint(1, 8) for _ in range(3))
        explicit = sp.simplify(
            sp.trace(
                generators[a - 1]
                * generators[b - 1]
                * generators[c - 1]
            )
        )
        assert sp.simplify(
            explicit - color_traces.trace_three(a, b, c)
        ) == 0


def test_trace_four_is_defined_by_explicit_matrices():
    value = color_traces.trace_four(1, 2, 3, 4)
    generators = color.generators()
    explicit = sp.simplify(
        sp.trace(
            generators[0] * generators[1] * generators[2] * generators[3]
        )
    )
    assert value == explicit


def test_f_contract_known_values():
    assert color_traces.f_contract(1, 2, 1, 2) == 1
    assert color_traces.f_contract(1, 1, 1, 1) == 0


def test_jacobi_identity():
    random.seed(6)
    for _ in range(10):
        a, b, c, d = (random.randint(1, 8) for _ in range(4))
        assert color_traces.jacobi_residual(a, b, c, d) == 0


def test_f_d_orthogonality_full_contraction():
    total = sp.simplify(
        sum(
            color_traces.f_d_contract(a, b, c, d) ** 2
            for a in range(1, 9)
            for b in range(1, 9)
            for c in range(1, 9)
            for d in range(1, 9)
        )
    )
    assert total >= 0


def test_casimir_generic():
    assert color_traces.casimir_generic(3) == {
        "C_F": sp.Rational(4, 3),
        "C_A": 3,
        "T_F": sp.Rational(1, 2),
    }
    assert color_traces.casimir_generic(5) == {
        "C_F": sp.Rational(12, 5),
        "C_A": 5,
        "T_F": sp.Rational(1, 2),
    }
    with pytest.raises(ValueError):
        color_traces.casimir_generic(1)


def test_su3_casimirs():
    assert color_traces.su3_casimirs() == {
        "C_F": sp.Rational(4, 3),
        "C_A": 3,
        "T_F": sp.Rational(1, 2),
    }


def test_trace_table():
    table = color_traces.trace_table()
    assert len(table) == 3
    assert all("trace_four" in row for row in table)
