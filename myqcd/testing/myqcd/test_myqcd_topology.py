"""图拓扑不变量、同构与枚举测试。"""

import pytest

from myqcd import feynman, topology


def test_chain_is_tree():
    chain = topology.build_chain(4)
    assert chain.loop_count == 0
    assert topology.is_tree(chain)
    assert not topology.is_cycle(chain)
    assert topology.degree_sequence(chain) == (1, 1, 2, 2)
    assert topology.external_leg_count(chain) == 0


def test_cycle_has_one_loop():
    cycle = topology.build_cycle(4)
    assert cycle.loop_count == 1
    assert topology.is_cycle(cycle)
    assert not topology.is_tree(cycle)


def test_self_energy_and_sunset():
    self_energy = topology.build_self_energy()
    assert self_energy.loop_count == 1
    assert topology.external_leg_count(self_energy) == 2
    assert not topology.is_tree(self_energy)

    sunset = topology.build_sunset()
    assert sunset.loop_count == 2
    assert topology.external_leg_count(sunset) == 2


def test_canonical_signature_is_relabel_invariant():
    left = feynman.Diagram(
        vertices=("a", "b", "c"),
        edges=(
            feynman.Edge(0, 1, "gluon"),
            feynman.Edge(1, 2, "gluon"),
            feynman.Edge(2, 0, "gluon"),
        ),
    )
    right = feynman.Diagram(
        vertices=("c", "a", "b"),
        edges=(
            feynman.Edge(2, 0, "gluon"),
            feynman.Edge(0, 1, "gluon"),
            feynman.Edge(1, 2, "gluon"),
        ),
    )
    assert topology.canonical_signature(left) == topology.canonical_signature(
        right
    )
    assert topology.is_isomorphic(left, right)


def test_non_isomorphic_graphs():
    triangle = topology.build_cycle(3)
    chain = topology.build_chain(3)
    assert not topology.is_isomorphic(triangle, chain)
    assert not topology.is_isomorphic(triangle, topology.build_cycle(4))


def test_enumerate_connected_topologies():
    triangles = topology.enumerate_connected_topologies(3, 3)
    assert len(triangles) == 1
    assert topology.is_cycle(triangles[0])

    trees = topology.enumerate_connected_topologies(4, 3)
    assert len(trees) == 2
    assert all(topology.is_tree(tree) for tree in trees)


def test_topology_table():
    table = topology.topology_table(topology.build_self_energy())
    assert table["loop_count"] == 1
    assert table["external_leg_count"] == 2
    assert table["internal_edge_count"] == 2
    assert table["is_tree"] is False


def test_builder_validation():
    with pytest.raises(ValueError):
        topology.build_chain(1)
    with pytest.raises(ValueError):
        topology.build_cycle(2)
    with pytest.raises(ValueError):
        topology.enumerate_connected_topologies(0, 0)
