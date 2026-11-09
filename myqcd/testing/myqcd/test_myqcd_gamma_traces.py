"""γ5 迹与手征投影迹测试。"""

import pytest

from myqcd import gamma, gamma_traces


def test_gamma5_four_trace_matches_epsilon():
    assert gamma_traces.trace_gamma5_four_residual() == 0
    assert gamma_traces.trace_gamma5((1, 2, 3, 4)) == 4
    assert gamma_traces.trace_gamma5((2, 1, 3, 4)) == -4


def test_short_gamma5_traces_vanish():
    assert gamma_traces.trace_gamma5(()) == 0
    assert gamma_traces.trace_gamma5((1, 2)) == 0
    assert gamma_traces.trace_gamma5((1, 2, 3)) == 0


def test_long_gamma5_trace_uses_explicit_matrix():
    value = gamma_traces.trace_gamma5((1, 2, 3, 4, 1, 2))
    assert value == 0
    assert isinstance(value, object)


def test_chiral_projector_traces():
    traces = gamma_traces.trace_projector_orthogonality()
    assert traces["Tr[P_L]"] == 2
    assert traces["Tr[P_R]"] == 2
    assert traces["Tr[P_L P_R]"] == 0
    assert traces["Tr[P_L + P_R]"] == 4
    assert gamma_traces.trace_left_projector() == 2
    assert gamma_traces.trace_right_projector() == 2


def test_gamma5_anticommutator():
    assert all(
        gamma_traces.gamma5_anticommutator_residual(mu).is_zero_matrix
        for mu in range(1, 5)
    )


def test_gamma5_table():
    table = gamma_traces.trace_gamma5_table()
    assert table[0]["trace"] == "4"
    assert table[1]["trace"] == "0"
    assert len(table) == 4


def test_index_validation():
    with pytest.raises(ValueError):
        gamma_traces.trace_gamma5((0,))
    with pytest.raises(ValueError):
        gamma_traces.trace_gamma5_four(1, 2, 3, 5)
    with pytest.raises(ValueError):
        gamma_traces.gamma5_anticommutator_residual(0)


def test_gamma5_is_product_of_gammas():
    product = (
        gamma.gamma(1)
        * gamma.gamma(2)
        * gamma.gamma(3)
        * gamma.gamma(4)
    )
    assert (product - gamma.gamma5()).is_zero_matrix
