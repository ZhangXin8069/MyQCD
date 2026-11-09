"""RGE 演化测试。"""

import sympy as sp
import pytest

from myqcd import evolution


def test_solve_z_and_anomalous_dimension():
    mu = sp.Symbol("mu", positive=True)
    mu0 = sp.Symbol("mu0", positive=True)
    gamma = sp.Symbol("gamma", real=True)
    z = evolution.solve_z(mu, mu0, gamma)
    assert sp.simplify(evolution.anomalous_dimension_from_z(z, mu) - gamma) == 0


def test_evolve_operator():
    mu = sp.Symbol("mu", positive=True)
    mu0 = sp.Symbol("mu0", positive=True)
    value = evolution.evolve_operator(3, 1, mu0, mu)
    assert sp.simplify(value - 3 * mu0 / mu) == 0
    assert evolution.evolution_residual(3, 1, mu0, mu) == 0


def test_diagonal_evolution_matrix():
    mu = sp.Symbol("mu", positive=True)
    mu0 = sp.Symbol("mu0", positive=True)
    matrix = evolution.diagonal_evolution_matrix((0, 1), mu0, mu)
    assert matrix.shape == (2, 2)
    assert sp.simplify(matrix[0, 0] - 1) == 0
    assert sp.simplify(matrix[1, 1] - mu0 / mu) == 0
    with pytest.raises(ValueError):
        evolution.diagonal_evolution_matrix((), mu0, mu)


def test_evolution_table():
    table = evolution.evolution_table()
    assert len(table) == 4
    assert table[0]["gamma"] == "0"
    with pytest.raises(ValueError):
        evolution.solve_z(1, 0, 1)
