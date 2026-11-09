"""费曼图的零依赖导出：TikZ-Feynman、Graphviz DOT 与 SVG。

导出器只消费 :class:`myqcd.feynman.Diagram` 的组合结构，不绘制物理上
未经验证的顶点细节。TikZ 输出需要 LaTeX 侧的 ``tikz-feynman`` 宏包；
DOT 输出可由 Graphviz 渲染；SVG 由本模块直接生成，不依赖外部进程。

布局规则：树图用水平链；纯环图（每个顶点度数 2）用圆周布局；两个顶点
之间的平行边用二次曲线分开；外部腿边画成短桩。这样一圈自能、两圈
sunset 和三角形不会退化成重叠的直线。
"""

from __future__ import annotations

import json
import math
from collections import Counter
from typing import Mapping

from .feynman import Diagram


_TIKZ_STYLES = {
    "quark": "fermion",
    "antiquark": "anti fermion",
    "gluon": "gluon",
    "ghost": "ghost",
    "scalar": "scalar",
    "photon": "photon",
}

_SVG_COLORS = {
    "quark": "#1f4e79",
    "antiquark": "#1f4e79",
    "gluon": "#c00000",
    "ghost": "#7f7f7f",
    "scalar": "#548235",
    "photon": "#bf9000",
}


def _xml_escape(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def _dot_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def _internal_edges(diagram: Diagram) -> tuple:
    return tuple(
        edge
        for edge in diagram.edges
        if edge.left >= 0 and edge.right >= 0
    )


def _is_cycle(diagram: Diagram) -> bool:
    if diagram.vertex_count < 3:
        return False
    internal = _internal_edges(diagram)
    if len(internal) != diagram.vertex_count:
        return False
    adjacency = diagram.adjacency()
    return all(
        sum(1 for neighbour in adjacency[index] if neighbour >= 0) == 2
        for index in range(diagram.vertex_count)
    )


def _vertex_positions(
    diagram: Diagram,
) -> tuple[dict[int, tuple[float, float]], float, float]:
    count = diagram.vertex_count
    internal = _internal_edges(diagram)
    if _is_cycle(diagram):
        width, height = 420.0, 320.0
        center_x, center_y = width / 2, height / 2
        radius = 105.0
        positions = {
            index: (
                center_x + radius * math.cos(-math.pi / 2 + 2 * math.pi * index / count),
                center_y + radius * math.sin(-math.pi / 2 + 2 * math.pi * index / count),
            )
            for index in range(count)
        }
        return positions, width, height
    if count == 2 and len(internal) >= 2:
        return {0: (90.0, 130.0), 1: (230.0, 130.0)}, 320.0, 260.0
    width = 160.0 + 120.0 * max(count - 1, 0)
    height = 200.0
    positions = {
        index: (80.0 + 120.0 * index, 100.0)
        for index in range(count)
    }
    return positions, width, height


def _pair_counts(diagram: Diagram) -> Counter:
    counts: Counter = Counter()
    for edge in _internal_edges(diagram):
        counts[tuple(sorted((edge.left, edge.right)))] += 1
    return counts


def _external_stub(
    diagram: Diagram,
    positions: dict[int, tuple[float, float]],
    width: float,
    edge,
    external_index: int,
) -> tuple[float, float, float, float]:
    vertex = edge.left if edge.left >= 0 else edge.right
    x, y = positions[vertex]
    on_left = x <= width / 2
    stub_x = x - 55.0 if on_left else x + 55.0
    same_vertex = [
        candidate
        for candidate in diagram.edges
        if (candidate.left < 0 or candidate.right < 0)
        and (candidate.left == vertex or candidate.right == vertex)
    ]
    offset = 18.0 * (external_index - (len(same_vertex) - 1) / 2)
    return x, y, stub_x, y + offset


def to_json(diagram: Diagram) -> str:
    """把图的结构导出为 JSON。"""

    return json.dumps(
        diagram.to_dict(), ensure_ascii=False, indent=2
    ) + "\n"


def to_mermaid(diagram: Diagram) -> str:
    """把图导出为 Mermaid flowchart。"""

    lines = ["flowchart LR"]
    for index, label in enumerate(diagram.vertices):
        lines.append(f'  v{index}["{label}"]')
    for index, edge in enumerate(diagram.edges):
        if edge.left < 0 or edge.right < 0:
            lines.append(f'  ext{index}((""))')
            left = f"ext{index}" if edge.left < 0 else f"v{edge.left}"
            right = f"ext{index}" if edge.right < 0 else f"v{edge.right}"
        else:
            left, right = f"v{edge.left}", f"v{edge.right}"
        lines.append(f"  {left} -->|{edge.particle}| {right}")
    return "\n".join(lines) + "\n"


def to_latex_table(diagram: Diagram) -> str:
    """把图的顶点/边摘要导出为 LaTeX tabular。"""

    lines = [
        "\\begin{tabular}{lll}",
        "\\hline",
        "Edge & Particle & Endpoints \\\\",
        "\\hline",
    ]
    for edge in diagram.edges:
        left = "$-1$" if edge.left < 0 else str(edge.left)
        right = "$-1$" if edge.right < 0 else str(edge.right)
        lines.append(
            f"{edge.left}/{edge.right} & {edge.particle} & "
            f"({left},{right}) \\\\"
        )
    lines.extend(["\\hline", "\\end{tabular}"])
    return "\n".join(lines) + "\n"


def to_dot(diagram: Diagram) -> str:
    """把图导出为 Graphviz DOT。"""

    lines = [f'digraph "{_dot_escape(diagram.name or "feynman")}" {{']
    lines.append("  rankdir=LR;")
    lines.append("  node [shape=circle, fontsize=12];")
    for index, label in enumerate(diagram.vertices):
        lines.append(
            f'  v{index} [label="{_dot_escape(label)}"];'
        )
    for index, edge in enumerate(diagram.edges):
        if edge.left < 0 or edge.right < 0:
            lines.append(f"  ext{index} [shape=point,label=\"\"];")
            left = f"ext{index}" if edge.left < 0 else f"v{edge.left}"
            right = f"ext{index}" if edge.right < 0 else f"v{edge.right}"
        else:
            left, right = f"v{edge.left}", f"v{edge.right}"
        lines.append(
            f'  {left} -> {right} '
            f'[label="{_dot_escape(edge.particle)}"];'
        )
    lines.append("}")
    return "\n".join(lines) + "\n"


def to_tikz(diagram: Diagram) -> str:
    """把图导出为 TikZ-Feynman 代码片段。"""

    positions, _width, _height = _vertex_positions(diagram)
    scale = 60.0
    lines = [
        "% Generated by myqcd.diagram_export; requires \\usepackage{tikz-feynman}",
        "\\begin{tikzpicture}",
        "\\begin{feynman}",
    ]
    for index, label in enumerate(diagram.vertices):
        x, y = positions[index]
        lines.append(
            f"\\vertex (v{index}) at ({x / scale:.2f},{-y / scale:.2f}) "
            f"{{{label}}};"
        )
    external_indices = [
        index
        for index, edge in enumerate(diagram.edges)
        if edge.left < 0 or edge.right < 0
    ]
    external_seen: Counter = Counter()
    for index in external_indices:
        edge = diagram.edges[index]
        vertex = edge.left if edge.left >= 0 else edge.right
        seen = external_seen[vertex]
        external_seen[vertex] += 1
        x, y, stub_x, stub_y = _external_stub(
            diagram, positions, _width, edge, seen
        )
        lines.append(
            f"\\vertex (ext{index}) at ({stub_x / scale:.2f},"
            f"{-stub_y / scale:.2f}) {{}};"
        )
    if diagram.external_legs:
        comments = ", ".join(diagram.external_legs)
        lines.append(f"% external legs: {comments}")
    lines.append("\\diagram* {")
    pair_counts = _pair_counts(diagram)
    pair_seen: Counter = Counter()
    for index, edge in enumerate(diagram.edges):
        style = _TIKZ_STYLES.get(edge.particle, "plain")
        if edge.left >= 0 and edge.right >= 0:
            key = tuple(sorted((edge.left, edge.right)))
            multiplicity = pair_counts[key]
            occurrence = pair_seen[key]
            pair_seen[key] += 1
            if multiplicity == 2:
                style += (
                    ", bend left=25" if occurrence == 0
                    else ", bend right=25"
                )
            elif multiplicity >= 3:
                if occurrence == 0:
                    style += ", bend left=25"
                elif occurrence >= 2:
                    style += ", bend right=25"
            left, right = f"v{edge.left}", f"v{edge.right}"
        else:
            endpoint = f"ext{index}"
            left = endpoint if edge.left < 0 else f"v{edge.left}"
            right = endpoint if edge.right < 0 else f"v{edge.right}"
        lines.append(f"  ({left}) -- [{style}] ({right});")
    lines.append("};")
    lines.append("\\end{feynman}")
    lines.append("\\end{tikzpicture}")
    return "\n".join(lines) + "\n"


def to_svg(
    diagram: Diagram,
    *,
    radius: float = 16.0,
) -> str:
    """把图导出为独立 SVG 字符串。"""

    positions, width, height = _vertex_positions(diagram)
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        (
            f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'width="{width:.0f}" height="{height:.0f}" '
            f'viewBox="0 0 {width:.0f} {height:.0f}">'
        ),
        f"<title>{_xml_escape(diagram.name or 'feynman diagram')}</title>",
    ]
    pair_counts = _pair_counts(diagram)
    pair_seen: Counter = Counter()
    external_seen: Counter = Counter()
    for index, edge in enumerate(diagram.edges):
        color = _SVG_COLORS.get(edge.particle, "#000000")
        if edge.left >= 0 and edge.right >= 0:
            key = tuple(sorted((edge.left, edge.right)))
            multiplicity = pair_counts[key]
            occurrence = pair_seen[key]
            pair_seen[key] += 1
            x1, y1 = positions[edge.left]
            x2, y2 = positions[edge.right]
            if multiplicity > 1:
                dx, dy = x2 - x1, y2 - y1
                length = math.hypot(dx, dy) or 1.0
                normal_x, normal_y = -dy / length, dx / length
                offset = 26.0 * (occurrence - (multiplicity - 1) / 2)
                control_x = (x1 + x2) / 2 + normal_x * 2 * offset
                control_y = (y1 + y2) / 2 + normal_y * 2 * offset
                lines.append(
                    f'<path d="M {x1:.1f} {y1:.1f} Q {control_x:.1f} '
                    f'{control_y:.1f} {x2:.1f} {y2:.1f}" fill="none" '
                    f'stroke="{color}" stroke-width="2"/>'
                )
                label_x = (x1 + 2 * control_x + x2) / 4
                label_y = (y1 + 2 * control_y + y2) / 4
            else:
                lines.append(
                    f'<line x1="{x1:.1f}" y1="{y1:.1f}" '
                    f'x2="{x2:.1f}" y2="{y2:.1f}" '
                    f'stroke="{color}" stroke-width="2"/>'
                )
                label_x, label_y = (x1 + x2) / 2, (y1 + y2) / 2
            lines.append(
                f'<text x="{label_x:.1f}" y="{label_y - 6:.1f}" '
                f'font-size="11" fill="{color}" text-anchor="middle">'
                f"{_xml_escape(edge.particle)}</text>"
            )
        else:
            vertex = edge.left if edge.left >= 0 else edge.right
            seen = external_seen[vertex]
            external_seen[vertex] += 1
            x, y, stub_x, stub_y = _external_stub(
                diagram, positions, width, edge, seen
            )
            lines.append(
                f'<line x1="{x:.1f}" y1="{y:.1f}" '
                f'x2="{stub_x:.1f}" y2="{stub_y:.1f}" '
                f'stroke="{color}" stroke-width="2"/>'
            )
            label_x = (x + stub_x) / 2
            label_y = (y + stub_y) / 2
            lines.append(
                f'<text x="{label_x:.1f}" y="{label_y - 6:.1f}" '
                f'font-size="11" fill="{color}" text-anchor="middle">'
                f"{_xml_escape(edge.particle)}</text>"
            )
    for index, label in enumerate(diagram.vertices):
        x, y = positions[index]
        lines.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{radius:.1f}" '
            'fill="#ffffff" stroke="#000000" stroke-width="2"/>'
        )
        lines.append(
            f'<text x="{x:.1f}" y="{y + 4:.1f}" font-size="11" '
            f'fill="#000000" text-anchor="middle">'
            f"{_xml_escape(label)}</text>"
        )
    lines.append("</svg>")
    return "\n".join(lines) + "\n"


_EXPORTERS = {
    "dot": to_dot,
    "json": to_json,
    "latex": to_latex_table,
    "mermaid": to_mermaid,
    "svg": to_svg,
    "tikz": to_tikz,
}


def render(diagram: Diagram, output_format: str) -> str:
    """按格式名导出图；支持 ``dot``、``tikz``、``svg``。"""

    key = output_format.lower()
    if key not in _EXPORTERS:
        raise ValueError(
            f"unsupported diagram format {output_format!r}; "
            f"expected one of {sorted(_EXPORTERS)}"
        )
    return _EXPORTERS[key](diagram)


def export_audit(diagram: Diagram) -> Mapping[str, object]:
    """返回各导出器的结构性自检结果。"""

    outputs = {
        "dot": to_dot(diagram),
        "json": to_json(diagram),
        "latex": to_latex_table(diagram),
        "mermaid": to_mermaid(diagram),
        "svg": to_svg(diagram),
        "tikz": to_tikz(diagram),
    }
    return {
        "formats": sorted(outputs),
        "sizes": {name: len(text) for name, text in outputs.items()},
        "nonempty": all(text.strip() for text in outputs.values()),
        "svg_well_formed_prefix": outputs["svg"].startswith("<?xml"),
        "tikz_has_feynman_environment": "\\begin{feynman}"
        in outputs["tikz"],
        "dot_has_digraph": outputs["dot"].startswith("digraph"),
    }


__all__ = [
    "export_audit",
    "render",
    "to_dot",
    "to_json",
    "to_latex_table",
    "to_mermaid",
    "to_svg",
    "to_tikz",
]
