"""图自同构与平行边交换测试。"""

from myqcd import symmetry, topology


def test_triangle_automorphisms():
    triangle = topology.build_cycle(3)
    assert symmetry.automorphism_count(triangle) == 6


def test_chain_automorphisms():
    chain = topology.build_chain(4)
    assert symmetry.automorphism_count(chain) == 2
    assert symmetry.edge_exchange_count(chain) == 1


def test_self_energy_automorphisms():
    diagram = topology.build_self_energy()
    assert symmetry.automorphism_count(diagram) == 2
    table = symmetry.symmetry_table(diagram)
    assert table["automorphism_count"] == 2
    assert "physics symmetry factors" in table["note"]


def test_sunset_edge_exchange():
    diagram = topology.build_sunset()
    assert symmetry.automorphism_count(diagram) == 2
    assert symmetry.edge_exchange_count(diagram) == 6


def test_parallel_edges_count():
    diagram = topology.build_sunset()
    assert symmetry.edge_exchange_count(diagram) == 6
