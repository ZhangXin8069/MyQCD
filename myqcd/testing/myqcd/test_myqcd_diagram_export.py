"""费曼图零依赖导出测试。"""

import pytest

from myqcd import diagram_export, feynman


def _diagram():
    return feynman.Diagram(
        vertices=("a", "b", "c"),
        edges=(
            feynman.Edge(0, 1, "quark"),
            feynman.Edge(1, 2, "gluon"),
            feynman.Edge(2, 0, "gluon"),
        ),
        external_legs=("a", "c"),
        name="sample",
    )


def test_dot_export():
    text = diagram_export.to_dot(_diagram())
    assert text.startswith("digraph")
    assert '"a"' in text
    assert "v0 -> v1" in text


def test_tikz_export():
    text = diagram_export.to_tikz(_diagram())
    assert "\\begin{feynman}" in text
    assert "\\diagram*" in text
    assert "[fermion]" in text
    assert "[gluon]" in text


def test_tikz_declares_external_vertex():
    diagram = feynman.Diagram(
        vertices=("a", "b"),
        edges=(
            feynman.Edge(0, 1, "quark"),
            feynman.Edge(0, -1, "quark"),
        ),
    )
    text = diagram_export.to_tikz(diagram)
    assert "\\vertex (external)" in text
    assert "(external)" in text


def test_svg_export():
    text = diagram_export.to_svg(_diagram())
    assert text.startswith("<?xml")
    assert "<svg" in text
    assert text.count("<circle") == 3
    assert text.count("<line") == 3


def test_render_dispatch_and_error():
    assert diagram_export.render(_diagram(), "dot").startswith("digraph")
    assert diagram_export.render(_diagram(), "TIKZ").startswith("%")
    with pytest.raises(ValueError):
        diagram_export.render(_diagram(), "pdf")


def test_export_audit():
    audit = diagram_export.export_audit(_diagram())
    assert audit["formats"] == ["dot", "svg", "tikz"]
    assert audit["nonempty"]
    assert audit["svg_well_formed_prefix"]
    assert audit["tikz_has_feynman_environment"]
    assert audit["dot_has_digraph"]
