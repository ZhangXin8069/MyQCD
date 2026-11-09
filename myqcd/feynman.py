"""费曼图数据结构、QCD 顶点/传播子规则与 Wick 配对图构建。

本模块只处理图的组合结构、规则清单和可审计不变量（顶点数、边数、连通
分量、圈数、Fermi 符号）。它不执行圈积分、不推导对称因子，也不把规则
清单升级为完整微扰计算。颜色因子与 Lorentz 结构以字符串登记，精确代数
由 :mod:`myqcd.gamma` 与 :mod:`myqcd.color` 提供。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence, Tuple

from . import wick as wick_module

PARTICLE_STYLES = {
    "quark": "fermion",
    "antiquark": "anti fermion",
    "gluon": "gluon",
    "ghost": "ghost",
    "scalar": "scalar",
    "photon": "photon",
}


@dataclass(frozen=True)
class VertexRule:
    """一个 QCD 顶点的粒子内容与因子结构（不做数值求值）。"""

    name: str
    particles: Tuple[str, ...]
    color_factor: str
    lorentz_factor: str
    coupling_power: int = 1
    notes: str = ""

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("vertex name must be nonempty")
        if not self.particles:
            raise ValueError("vertex must contain at least one particle")
        if self.coupling_power < 0:
            raise ValueError("coupling power must be nonnegative")
        if not self.color_factor.strip() or not self.lorentz_factor.strip():
            raise ValueError("vertex factors must be nonempty strings")

    def to_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "particles": list(self.particles),
            "color_factor": self.color_factor,
            "lorentz_factor": self.lorentz_factor,
            "coupling_power": self.coupling_power,
            "notes": self.notes,
        }


@dataclass(frozen=True)
class PropagatorRule:
    """一个传播子的粒子与因子结构。"""

    name: str
    particle: str
    expression: str
    color_factor: str = ""
    notes: str = ""

    def __post_init__(self) -> None:
        if not self.name.strip() or not self.particle.strip():
            raise ValueError("propagator name and particle must be nonempty")
        if not self.expression.strip():
            raise ValueError("propagator expression must be nonempty")

    def to_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "particle": self.particle,
            "expression": self.expression,
            "color_factor": self.color_factor,
            "notes": self.notes,
        }


def qcd_vertex_rules() -> Tuple[VertexRule, ...]:
    """返回 QCD 顶点规则清单（结构式，符号约定见 notes）。"""

    return (
        VertexRule(
            name="quark-antiquark-gluon",
            particles=("quark", "antiquark", "gluon"),
            color_factor="T^a_{ij}",
            lorentz_factor="gamma_mu",
            coupling_power=1,
            notes="QCD 三线性耦合；色因子取基本表示生成元。",
        ),
        VertexRule(
            name="three-gluon",
            particles=("gluon", "gluon", "gluon"),
            color_factor="f^{abc}",
            lorentz_factor=(
                "(k1-k2)_rho delta_{mu nu} + (k2-k3)_mu delta_{nu rho} "
                "+ (k3-k1)_nu delta_{rho mu}"
            ),
            coupling_power=1,
            notes="全反对称颜色结构；动量约定全部入流。",
        ),
        VertexRule(
            name="four-gluon",
            particles=("gluon", "gluon", "gluon", "gluon"),
            color_factor="f^{abe}f^{cde}",
            lorentz_factor="delta_{mu nu}delta_{rho sigma} permutations",
            coupling_power=2,
            notes="四胶子接触项；完整张量结构需展开三组颜色收缩。",
        ),
        VertexRule(
            name="ghost-antighost-gluon",
            particles=("ghost", "antighost", "gluon"),
            color_factor="f^{abc}",
            lorentz_factor="k_mu",
            coupling_power=1,
            notes="Faddeev--Popov 鬼场顶点；仅适用于协变规范。",
        ),
    )


def qcd_propagator_rules() -> Tuple[PropagatorRule, ...]:
    """返回 QCD 传播子规则清单（Euclidean 约定）。"""

    return (
        PropagatorRule(
            name="quark",
            particle="quark",
            expression="(m - i p_slash) / (p^2 + m^2)",
            color_factor="delta_{ij}",
            notes="Euclidean Dirac 传播子；i p_slash 与质量项符号按本库约定。",
        ),
        PropagatorRule(
            name="gluon",
            particle="gluon",
            expression="delta_{mu nu} / p^2",
            color_factor="delta^{ab}",
            notes="Feynman 规范；其它规范需补规范参数项。",
        ),
        PropagatorRule(
            name="ghost",
            particle="ghost",
            expression="1 / p^2",
            color_factor="delta^{ab}",
            notes="协变规范中的鬼场传播子。",
        ),
    )


@dataclass(frozen=True)
class Edge:
    """连接两个顶点索引的有向边；外部腿用 ``-1`` 表示。"""

    left: int
    right: int
    particle: str

    def __post_init__(self) -> None:
        for endpoint in (self.left, self.right):
            if not isinstance(endpoint, int) or isinstance(endpoint, bool):
                raise TypeError("edge endpoints must be ints")
            if endpoint < -1:
                raise ValueError("edge endpoints must be -1 or nonnegative")
        if self.left == self.right:
            raise ValueError("self-loops are not supported")
        if self.particle not in PARTICLE_STYLES:
            raise ValueError(f"unknown particle {self.particle!r}")

    def to_dict(self) -> dict[str, object]:
        return {
            "left": self.left,
            "right": self.right,
            "particle": self.particle,
        }


@dataclass(frozen=True)
class Diagram:
    """有限费曼图的组合结构。"""

    vertices: Tuple[str, ...]
    edges: Tuple[Edge, ...]
    external_legs: Tuple[str, ...] = ()
    sign: int = 1
    name: str = ""

    def __post_init__(self) -> None:
        if not self.vertices:
            raise ValueError("diagram must contain at least one vertex")
        if self.sign not in (-1, 1):
            raise ValueError("diagram sign must be +1 or -1")
        for edge in self.edges:
            for endpoint in (edge.left, edge.right):
                if endpoint >= len(self.vertices):
                    raise ValueError(
                        f"edge endpoint {endpoint} exceeds vertex count"
                    )

    @property
    def vertex_count(self) -> int:
        return len(self.vertices)

    @property
    def edge_count(self) -> int:
        return len(self.edges)

    @property
    def internal_edge_count(self) -> int:
        """返回两个端点都在图中的内部边数；外部腿不计入。"""

        return sum(
            1
            for edge in self.edges
            if edge.left >= 0 and edge.right >= 0
        )

    def adjacency(self) -> Tuple[Tuple[int, ...], ...]:
        neighbours: list[list[int]] = [[] for _ in self.vertices]
        for edge in self.edges:
            if edge.left >= 0 and edge.right >= 0:
                neighbours[edge.left].append(edge.right)
                neighbours[edge.right].append(edge.left)
            elif edge.left >= 0:
                neighbours[edge.left].append(-1)
            elif edge.right >= 0:
                neighbours[edge.right].append(-1)
        return tuple(tuple(sorted(set(items))) for items in neighbours)

    def connected_components(self) -> int:
        """返回忽略外部腿后的连通分量数。"""

        seen = [False] * self.vertex_count
        components = 0
        neighbours = self.adjacency()
        for start in range(self.vertex_count):
            if seen[start]:
                continue
            components += 1
            stack = [start]
            seen[start] = True
            while stack:
                current = stack.pop()
                for neighbour in neighbours[current]:
                    if neighbour >= 0 and not seen[neighbour]:
                        seen[neighbour] = True
                        stack.append(neighbour)
        return components

    @property
    def is_connected(self) -> bool:
        return self.connected_components() == 1

    @property
    def loop_count(self) -> int:
        """返回圈数 ``E_int - V + C``；外部腿边不计入 ``E_int``。"""

        return (
            self.internal_edge_count
            - self.vertex_count
            + self.connected_components()
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "vertices": list(self.vertices),
            "edges": [edge.to_dict() for edge in self.edges],
            "external_legs": list(self.external_legs),
            "sign": self.sign,
            "vertex_count": self.vertex_count,
            "edge_count": self.edge_count,
            "internal_edge_count": self.internal_edge_count,
            "connected_components": self.connected_components(),
            "loop_count": self.loop_count,
        }


def diagram_from_edges(
    vertex_labels: Sequence[str],
    edges: Iterable[Edge],
    *,
    external_legs: Sequence[str] = (),
    sign: int = 1,
    name: str = "",
) -> Diagram:
    """从顶点标签与边构造图，并校验端点。"""

    return Diagram(
        vertices=tuple(vertex_labels),
        edges=tuple(edges),
        external_legs=tuple(external_legs),
        sign=sign,
        name=name,
    )


def wick_pairing_diagram(
    fields: Iterable[wick_module.FermionField],
    pairing: wick_module.WickPairing,
    *,
    name: str = "",
) -> Diagram:
    """把一条 Wick 配对表示为二分配对图。

    每个场位置是一个顶点，每条夸克-反夸克配对是一条 ``fermion`` 边。
    图中不含算符插入顶点，因此圈数恒为零；它用于检查配对覆盖与 Fermi
    符号，而不是替代完整的关联函数图。
    """

    ordered = tuple(fields)
    quark_positions = [
        index for index, field in enumerate(ordered) if not field.antiquark
    ]
    antiquark_positions = [
        index for index, field in enumerate(ordered) if field.antiquark
    ]
    if len(pairing.quark_to_antiquark) != len(quark_positions):
        raise ValueError("pairing does not match the quark count")
    edges = []
    for quark_index, antiquark_index in enumerate(
        pairing.quark_to_antiquark
    ):
        edges.append(
            Edge(
                left=quark_positions[quark_index],
                right=antiquark_positions[antiquark_index],
                particle="quark",
            )
        )
    labels = tuple(
        f"{field.flavor}{'bar' if field.antiquark else ''}"
        for field in ordered
    )
    return Diagram(
        vertices=labels,
        edges=tuple(edges),
        sign=pairing.sign,
        name=name or "wick-pairing",
    )


def rule_audit() -> dict[str, object]:
    """返回规则清单的结构自检结果。"""

    vertices = qcd_vertex_rules()
    propagators = qcd_propagator_rules()
    return {
        "vertex_count": len(vertices),
        "propagator_count": len(propagators),
        "vertex_names": [rule.name for rule in vertices],
        "propagator_names": [rule.name for rule in propagators],
        "all_colors_nonempty": all(
            rule.color_factor.strip() for rule in vertices
        ),
        "all_lorentz_nonempty": all(
            rule.lorentz_factor.strip() for rule in vertices
        ),
        "coupling_powers": {
            rule.name: rule.coupling_power for rule in vertices
        },
    }


__all__ = [
    "Diagram",
    "Edge",
    "PARTICLE_STYLES",
    "PropagatorRule",
    "VertexRule",
    "diagram_from_edges",
    "qcd_propagator_rules",
    "qcd_vertex_rules",
    "rule_audit",
    "wick_pairing_diagram",
]
