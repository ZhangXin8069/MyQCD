"""有限费曼图的拓扑不变量、同构判定与小型拓扑枚举。

本模块只处理组合图：顶点、内部边、外部腿和粒子标签。它不计算对称
因子、动量路由或圈积分。对不超过 8 个顶点的图使用显式置换判定同构；
更大的图只提供基于度序列与边标签的规范签名，不声称完整同构判定。
"""

from __future__ import annotations

import itertools
from collections import Counter
from typing import Iterable, Sequence, Tuple

from .feynman import Diagram, Edge

MAX_PERMUTATION_VERTICES = 8


def internal_edges(diagram: Diagram) -> Tuple[Edge, ...]:
    """返回两个端点都在图中的边。"""

    return tuple(
        edge
        for edge in diagram.edges
        if edge.left >= 0 and edge.right >= 0
    )


def external_leg_count(diagram: Diagram) -> int:
    """返回外部腿边数（端点为 ``-1``）。"""

    return sum(
        1
        for edge in diagram.edges
        if edge.left < 0 or edge.right < 0
    )


def degree_sequence(diagram: Diagram) -> Tuple[int, ...]:
    """返回内部边的顶点度数序列（升序）。"""

    adjacency = diagram.adjacency()
    degrees = [
        sum(1 for neighbour in adjacency[index] if neighbour >= 0)
        for index in range(diagram.vertex_count)
    ]
    return tuple(sorted(degrees))


def is_tree(diagram: Diagram) -> bool:
    """判断内部图是否为森林：``E_int = V - C``。"""

    return (
        diagram.internal_edge_count
        == diagram.vertex_count - diagram.connected_components()
    )


def is_cycle(diagram: Diagram) -> bool:
    """判断内部图是否为单环（所有顶点度数为 2）。"""

    if diagram.vertex_count < 3:
        return False
    if diagram.internal_edge_count != diagram.vertex_count:
        return False
    return all(degree == 2 for degree in degree_sequence(diagram))


def _mapped_edge_signature(
    diagram: Diagram, mapping: Sequence[int]
) -> Tuple[Tuple[int, int, str], ...]:
    entries = []
    for edge in diagram.edges:
        left = -1 if edge.left < 0 else mapping[edge.left]
        right = -1 if edge.right < 0 else mapping[edge.right]
        entries.append(
            (min(left, right), max(left, right), edge.particle)
        )
    return tuple(sorted(entries))


def canonical_signature(diagram: Diagram) -> Tuple[Tuple[int, int, str], ...]:
    """返回对顶点重标号不变的边签名。

    对小图穷举所有顶点置换取字典序最小者；对大图使用恒等映射的签名，
    并配合度序列做近似比较。
    """

    if diagram.vertex_count <= MAX_PERMUTATION_VERTICES:
        best = None
        for permutation in itertools.permutations(range(diagram.vertex_count)):
            signature = _mapped_edge_signature(diagram, permutation)
            if best is None or signature < best:
                best = signature
        return best or ()
    return _mapped_edge_signature(diagram, tuple(range(diagram.vertex_count)))


def is_isomorphic(left: Diagram, right: Diagram) -> bool:
    """判断两个图在顶点重标号下是否同构（小图精确）。"""

    if left.vertex_count != right.vertex_count:
        return False
    if left.edge_count != right.edge_count:
        return False
    if external_leg_count(left) != external_leg_count(right):
        return False
    if degree_sequence(left) != degree_sequence(right):
        return False
    if left.vertex_count > MAX_PERMUTATION_VERTICES:
        return canonical_signature(left) == canonical_signature(right)
    reference = _mapped_edge_signature(
        left, tuple(range(left.vertex_count))
    )
    for permutation in itertools.permutations(range(right.vertex_count)):
        if _mapped_edge_signature(right, permutation) == reference:
            return True
    return False


def enumerate_connected_topologies(
    vertex_count: int,
    internal_edge_count: int,
    *,
    particle: str = "gluon",
) -> Tuple[Diagram, ...]:
    """枚举给定顶点/内部边数的连通简单图，按同构去重。

    只支持小规模组合；``vertex_count`` 建议不超过 6。
    """

    if vertex_count < 1:
        raise ValueError("vertex_count must be positive")
    possible = list(
        itertools.combinations(range(vertex_count), 2)
    )
    if internal_edge_count > len(possible):
        return ()
    unique: list[Diagram] = []
    for selected in itertools.combinations(possible, internal_edge_count):
        diagram = Diagram(
            vertices=tuple(f"v{index}" for index in range(vertex_count)),
            edges=tuple(
                Edge(left, right, particle)
                for left, right in selected
            ),
            name="enumerated",
        )
        if not diagram.is_connected:
            continue
        if any(is_isomorphic(diagram, existing) for existing in unique):
            continue
        unique.append(diagram)
    return tuple(unique)


def build_chain(vertex_count: int, *, particle: str = "quark") -> Diagram:
    """构造 ``v0 - v1 - ...`` 的链图。"""

    if vertex_count < 2:
        raise ValueError("chain requires at least two vertices")
    return Diagram(
        vertices=tuple(f"v{index}" for index in range(vertex_count)),
        edges=tuple(
            Edge(index, index + 1, particle)
            for index in range(vertex_count - 1)
        ),
        name="chain",
    )


def build_cycle(vertex_count: int, *, particle: str = "gluon") -> Diagram:
    """构造单环图。"""

    if vertex_count < 3:
        raise ValueError("cycle requires at least three vertices")
    edges = [
        Edge(index, (index + 1) % vertex_count, particle)
        for index in range(vertex_count)
    ]
    return Diagram(
        vertices=tuple(f"v{index}" for index in range(vertex_count)),
        edges=tuple(edges),
        name="cycle",
    )


def build_self_energy(
    *, quark: str = "quark", gluon: str = "gluon"
) -> Diagram:
    """构造一条夸克线加一条胶子线的单圈自能。"""

    return Diagram(
        vertices=("q_in", "q_out"),
        edges=(
            Edge(0, 1, quark),
            Edge(0, 1, gluon),
            Edge(0, -1, quark),
            Edge(1, -1, quark),
        ),
        external_legs=("q_in", "q_out"),
        name="self-energy",
    )


def build_sunset(*, particle: str = "gluon") -> Diagram:
    """构造三条内部线连接两个顶点的两圈 sunset。"""

    return Diagram(
        vertices=("a", "b"),
        edges=(
            Edge(0, 1, particle),
            Edge(0, 1, particle),
            Edge(0, 1, particle),
            Edge(0, -1, "quark"),
            Edge(1, -1, "quark"),
        ),
        external_legs=("q_in", "q_out"),
        name="sunset",
    )


def topology_table(diagram: Diagram) -> dict[str, object]:
    """返回图的组合不变量摘要。"""

    return {
        "name": diagram.name,
        "vertex_count": diagram.vertex_count,
        "edge_count": diagram.edge_count,
        "internal_edge_count": diagram.internal_edge_count,
        "external_leg_count": external_leg_count(diagram),
        "connected_components": diagram.connected_components(),
        "loop_count": diagram.loop_count,
        "degree_sequence": degree_sequence(diagram),
        "is_tree": is_tree(diagram),
        "is_cycle": is_cycle(diagram),
        "canonical_signature": canonical_signature(diagram),
    }


__all__ = [
    "MAX_PERMUTATION_VERTICES",
    "build_chain",
    "build_cycle",
    "build_self_energy",
    "build_sunset",
    "canonical_signature",
    "degree_sequence",
    "enumerate_connected_topologies",
    "external_leg_count",
    "internal_edges",
    "is_cycle",
    "is_isomorphic",
    "is_tree",
    "topology_table",
]
