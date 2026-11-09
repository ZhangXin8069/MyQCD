"""费曼图结构、Wick 配对图与 QCD 规则测试。"""

import pytest

from myqcd import feynman, wick


def _triangle():
    return feynman.Diagram(
        vertices=("a", "b", "c"),
        edges=(
            feynman.Edge(0, 1, "gluon"),
            feynman.Edge(1, 2, "gluon"),
            feynman.Edge(2, 0, "gluon"),
        ),
        name="triangle",
    )


def test_chain_has_zero_loops():
    diagram = feynman.Diagram(
        vertices=("a", "b", "c"),
        edges=(
            feynman.Edge(0, 1, "quark"),
            feynman.Edge(1, 2, "quark"),
        ),
    )
    assert diagram.vertex_count == 3
    assert diagram.edge_count == 2
    assert diagram.connected_components() == 1
    assert diagram.loop_count == 0
    assert diagram.is_connected


def test_triangle_has_one_loop():
    diagram = _triangle()
    assert diagram.connected_components() == 1
    assert diagram.loop_count == 1


def test_disconnected_components():
    diagram = feynman.Diagram(
        vertices=("a", "b", "c", "d"),
        edges=(feynman.Edge(0, 1, "gluon"),),
    )
    assert diagram.connected_components() == 3
    assert not diagram.is_connected
    assert diagram.loop_count == 1 - 4 + 3


def test_edge_validation():
    with pytest.raises(ValueError):
        feynman.Edge(0, 0, "quark")
    with pytest.raises(ValueError):
        feynman.Edge(0, 1, "unknown")
    with pytest.raises(ValueError):
        feynman.Diagram(("a",), (feynman.Edge(0, 2, "quark"),))


def test_wick_pairing_diagram():
    fields = wick.fermion_fields(["u"], ["u"])
    pairing = wick.enumerate_wick_pairings(fields)[0]
    diagram = feynman.wick_pairing_diagram(fields, pairing)
    assert diagram.vertices == ("u", "ubar")
    assert diagram.edge_count == 1
    assert diagram.loop_count == 0
    assert diagram.sign == pairing.sign


def test_qcd_rule_catalog():
    audit = feynman.rule_audit()
    assert audit["vertex_count"] >= 4
    assert audit["propagator_count"] >= 3
    assert audit["all_colors_nonempty"]
    assert audit["all_lorentz_nonempty"]
    assert audit["coupling_powers"]["four-gluon"] == 2


def test_diagram_to_dict():
    data = _triangle().to_dict()
    assert data["loop_count"] == 1
    assert data["connected_components"] == 1
    assert data["edge_count"] == 3
