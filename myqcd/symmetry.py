"""有限图的顶点自同构与边交换计数。"""

from __future__ import annotations

import itertools
import math
from typing import Sequence, Tuple

from .feynman import Diagram

MAX_AUTOMORPHISM_VERTICES = 8


def _edge_signature(diagram: Diagram, permutation: Sequence[int]) -> Tuple[Tuple[int, int, str], ...]:
    entries = []
    for edge in diagram.edges:
        left = -1 if edge.left < 0 else permutation[edge.left]
        right = -1 if edge.right < 0 else permutation[edge.right]
        entries.append((min(left, right), max(left, right), edge.particle))
    return tuple(sorted(entries))


def automorphisms(diagram: Diagram) -> Tuple[Tuple[int, ...], ...]:
    """返回保持边多重集的顶点置换。"""

    if diagram.vertex_count > MAX_AUTOMORPHISM_VERTICES:
        raise ValueError("automorphism enumeration supports at most eight vertices")
    reference = _edge_signature(diagram, tuple(range(diagram.vertex_count)))
    return tuple(
        permutation
        for permutation in itertools.permutations(range(diagram.vertex_count))
        if _edge_signature(diagram, permutation) == reference
    )


def automorphism_count(diagram: Diagram) -> int:
    """返回顶点自同构数。"""

    return len(automorphisms(diagram))


def edge_exchange_count(diagram: Diagram) -> int:
    """返回同粒子平行边的交换数 ``prod_k m_k!``。"""

    counts: dict[tuple[int, int, str], int] = {}
    for edge in diagram.edges:
        key = (min(edge.left, edge.right), max(edge.left, edge.right), edge.particle)
        counts[key] = counts.get(key, 0) + 1
    return math.prod(math.factorial(value) for value in counts.values())


def symmetry_table(diagram: Diagram) -> dict[str, object]:
    """返回顶点自同构与边交换摘要（不声明物理对称因子）。"""

    return {
        "vertices": diagram.vertex_count,
        "edges": diagram.edge_count,
        "automorphism_count": automorphism_count(diagram),
        "edge_exchange_count": edge_exchange_count(diagram),
        "note": "physics symmetry factors require particle-content conventions",
    }


__all__ = [
    "MAX_AUTOMORPHISM_VERTICES",
    "automorphism_count",
    "automorphisms",
    "edge_exchange_count",
    "symmetry_table",
]
