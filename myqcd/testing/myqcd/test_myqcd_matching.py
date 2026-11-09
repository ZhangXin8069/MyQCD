"""树级匹配与 hybrid 开关测试。"""

import sympy as sp
import pytest

from myqcd import matching


def test_fourier_prefactor():
    assert matching.fourier_prefactor() == 1 / sp.pi


def test_tree_level_matching():
    assert matching.tree_level_matching("S") == 1
    with pytest.raises(ValueError):
        matching.tree_level_matching("")


def test_hybrid_switch_continuity():
    assert matching.hybrid_continuity_residual() == 0
    x = sp.Symbol("x")
    value = matching.hybrid_switch(x)
    assert sp.limit(value, x, -sp.oo) == 0
    assert sp.limit(value, x, sp.oo) == 1


def test_matching_residual():
    assert matching.matching_residual(2, 4, sp.Rational(1, 2)) == 0
    assert matching.matching_residual(2, 4, 1) == -2


def test_matching_table():
    table = matching.matching_table(("S", "V"))
    assert len(table) == 2
    assert all(row["tree_matching"] == "1" for row in table)
