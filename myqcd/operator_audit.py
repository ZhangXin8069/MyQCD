"""算符构建与费曼图层的一键审计。

用法::

    python -m myqcd.operator_audit --root .
    python -m myqcd.operator_audit --output logs/data/operator_audit/report.json

审计只覆盖可在精确代数或有限图上闭合的不变量：Clifford 代数、Dirac
基完备性、迹定理、颜色代数、双线性分解、Wick 配对图、圈数公式和导出器
结构。它不读取真实系综，也不执行圈积分或数值张量收缩。
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Sequence

import sympy as sp

from . import (
    color,
    color_traces,
    diagram_export,
    feynman,
    fierz,
    gamma,
    gamma_traces,
    lattice,
    lorentz,
    operator_basis,
    operators,
    qcd_rules,
    statistics,
    topology,
    wick,
)


def _matrix_zero(matrix: sp.MatrixBase) -> bool:
    return bool(sp.Matrix(matrix).is_zero_matrix)


def _diagram_chain() -> feynman.Diagram:
    return feynman.Diagram(
        vertices=("src", "op", "sink"),
        edges=(
            feynman.Edge(0, 1, "quark"),
            feynman.Edge(1, 2, "quark"),
        ),
        external_legs=("src", "sink"),
        name="two-point-chain",
    )


def _diagram_triangle() -> feynman.Diagram:
    return feynman.Diagram(
        vertices=("a", "b", "c"),
        edges=(
            feynman.Edge(0, 1, "gluon"),
            feynman.Edge(1, 2, "gluon"),
            feynman.Edge(2, 0, "gluon"),
        ),
        name="three-gluon-loop",
    )


def _diagram_self_energy() -> feynman.Diagram:
    return feynman.Diagram(
        vertices=("q_in", "q_out"),
        edges=(
            feynman.Edge(0, 1, "quark"),
            feynman.Edge(0, 1, "gluon"),
            feynman.Edge(0, -1, "quark"),
            feynman.Edge(1, -1, "quark"),
        ),
        external_legs=("q_in", "q_out"),
        name="quark-self-energy",
    )


def _diagram_sunset() -> feynman.Diagram:
    return feynman.Diagram(
        vertices=("a", "b"),
        edges=(
            feynman.Edge(0, 1, "gluon"),
            feynman.Edge(0, 1, "gluon"),
            feynman.Edge(0, 1, "gluon"),
            feynman.Edge(0, -1, "quark"),
            feynman.Edge(1, -1, "quark"),
        ),
        external_legs=("q_in", "q_out"),
        name="sunset-two-loop",
    )


def run_checks() -> dict[str, bool]:
    """运行全部代数、算符、图和导出检查。"""

    identity = gamma.identity()
    gamma5 = gamma.gamma5()
    four_gammas = gamma.gamma_matrices()

    checks: dict[str, bool] = {
        "gamma_clifford": all(
            _matrix_zero(gamma.clifford_residual(mu, nu))
            for mu in range(1, 5)
            for nu in range(1, 5)
        ),
        "gamma5_square": _matrix_zero(gamma5 * gamma5 - identity),
        "gamma5_anticommutator": all(
            _matrix_zero(gamma5 * matrix + matrix * gamma5)
            for matrix in four_gammas
        ),
        "gamma_basis_rank_16": gamma.gamma_basis_rank() == 16,
        "gamma_basis_gram_offdiagonal": all(
            sp.simplify(gamma.gamma_basis_gram()[left, right]) == 0
            for left in range(16)
            for right in range(16)
            if left != right
        ),
        "charge_conjugation_transpose": all(
            _matrix_zero(
                gamma.charge_conjugation_matrix()
                * gamma.gamma(mu)
                * gamma.charge_conjugation_matrix().H
                + gamma.gamma(mu).T
            )
            for mu in range(1, 5)
        ),
        "parity_projector_complete": _matrix_zero(
            sum(gamma.parity_projectors(), sp.zeros(4)) - identity
        ),
        "parity_projector_idempotent": all(
            _matrix_zero(projector * projector - projector)
            for projector in gamma.parity_projectors()
        ),
        "color_casimir_fundamental": color.casimir_fundamental()
        == sp.Rational(4, 3),
        "color_casimir_adjoint": color.casimir_adjoint() == 3,
        "color_fierz": color.color_fierz_residual() == 0,
        "bilinear_structure_count": len(
            operators.dirac_bilinear_structures()
        )
        == 16,
        "bilinear_roundtrip": all(
            _matrix_zero(
                operators.reconstruct_dirac_bilinear(
                    operators.decompose_dirac_bilinear(matrix)
                )
                - matrix
            )
            for matrix in operators.dirac_bilinear_structures().values()
        ),
        "pyqcd_index_identity": operators.pyqcd_gamma_index(identity) == 0,
        "pyqcd_index_gamma5": operators.pyqcd_gamma_index(gamma5) == 5,
        "operator_dimension": operators.operator_mass_dimension(2) == 5,
        "wick_diagram_edges": (
            feynman.wick_pairing_diagram(
                wick.fermion_fields(["u"], ["u"]),
                wick.enumerate_wick_pairings(
                    wick.fermion_fields(["u"], ["u"])
                )[0],
            ).edge_count
            == 1
        ),
        "chain_loop_count_zero": _diagram_chain().loop_count == 0,
        "triangle_loop_count_one": _diagram_triangle().loop_count == 1,
        "image_self_energy_loop_one": _diagram_self_energy().loop_count == 1,
        "sunset_loop_count_two": _diagram_sunset().loop_count == 2,
        "external_legs_not_counted": (
            _diagram_self_energy().edge_count == 4
            and _diagram_self_energy().internal_edge_count == 2
        ),
        "parallel_edges_are_curved": (
            diagram_export.to_svg(_diagram_self_energy()).count("<path") == 2
        ),
        "triangle_connected": _diagram_triangle().is_connected,
        "lorentz_epsilon_double_contract": (
            lorentz.epsilon_two_contract_residual() == 0
        ),
        "lorentz_schouten": lorentz.schouten_residual(
            lorentz.vector_components("p")
        )
        == 0,
        "lorentz_projector_idempotent": (
            sp.simplify(
                sum(
                    lorentz.transverse_projector(
                        lorentz.vector_components("p"), 0, nu
                    )
                    * lorentz.transverse_projector(
                        lorentz.vector_components("p"), nu, 2
                    )
                    for nu in range(4)
                )
                - lorentz.transverse_projector(
                    lorentz.vector_components("p"), 0, 2
                )
            )
            == 0
        ),
        "fierz_scalar_scalar": len(fierz.fierz_transform("S", "S")) == 16,
        "fierz_mixed_nonempty": bool(fierz.fierz_transform("S", "V1")),
        "operator_basis_count": len(
            operator_basis.enumerate_derivative_operators(
                ("u",), max_derivatives=1, colors=("singlet",)
            )
        )
        == 32,
        "chiral_projectors": all(
            operator_basis.chiral_projector_identities().values()
        ),
        "qcd_quark_propagator": qcd_rules.quark_propagator_residual(
            lorentz.vector_components("p"), sp.Symbol("m", positive=True)
        ).is_zero_matrix,
        "qcd_ward_identity": qcd_rules.ward_identity_residual(
            lorentz.vector_components("p")
        ).is_zero_matrix,
        "qcd_landau_transverse": all(
            qcd_rules.gluon_transversality(
                lorentz.vector_components("p"), nu, gauge_parameter=0
            )
            == 0
            for nu in range(4)
        ),
        "color_trace_three": color_traces.trace_three(1, 2, 3)
        == sp.I / 4,
        "color_jacobi": color_traces.jacobi_residual(1, 2, 3, 4) == 0,
        "gamma5_four_trace": gamma_traces.trace_gamma5_four_residual() == 0,
        "gamma5_projectors": gamma_traces.trace_projector_orthogonality()[
            "Tr[P_L]"
        ]
        == 2,
        "topology_tree": topology.is_tree(topology.build_chain(3)),
        "topology_cycle": topology.is_cycle(topology.build_cycle(3)),
        "lattice_dispersion": lattice.lattice_dispersion((0.1, 0.2)) > 0,
        "statistics_jackknife": statistics.jackknife_mean(
            [(1.0, 2.0), (2.0, 4.0), (3.0, 6.0)]
        )
        == (2.0, 4.0),
        "rule_audit_vertices": feynman.rule_audit()["vertex_count"] >= 4,
        "diagram_export_all_formats": bool(
            diagram_export.export_audit(_diagram_triangle())["nonempty"]
        ),
    }

    for indices in ((1, 1, 1, 1), (1, 2, 1, 2), (1, 2, 2, 1), (1, 2, 3, 4)):
        theorem = gamma.trace_gamma_product(indices)
        explicit = gamma.dirac_trace(
            sp.prod([gamma.gamma(index) for index in indices])
        )
        checks[f"trace_theorem_{''.join(map(str, indices))}"] = (
            sp.simplify(theorem - explicit) == 0
        )

    return checks


def build_report(root: Path | str) -> dict[str, object]:
    """组装机器可读报告。"""

    checks = run_checks()
    failed = [name for name, passed in checks.items() if not passed]
    return {
        "schema": "myqcd-operator-feynman-audit-v1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "root": str(Path(root).resolve()),
        "status": "verified" if not failed else "failed",
        "failed_checks": failed,
        "check_count": len(checks),
        "checks": checks,
        "operator_structures": operators.structure_summary(),
        "diagram_rules": feynman.rule_audit(),
        "diagram_samples": {
            "chain": _diagram_chain().to_dict(),
            "triangle": _diagram_triangle().to_dict(),
            "self_energy": _diagram_self_energy().to_dict(),
            "sunset": _diagram_sunset().to_dict(),
        },
        "trusted_scope": (
            "精确 Clifford/颜色代数、Dirac 双线性分解、Wick 配对图、"
            "圈数公式与导出字符串结构；不含圈积分、真实系综或数值收缩"
        ),
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="MyQCD 工作区根目录（默认当前目录）",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="JSON 输出路径；默认 logs/data/operator_audit/operator_feynman_audit.json",
    )
    args = parser.parse_args(argv)
    root = args.root.resolve()
    output = (
        args.output
        or root / "logs/data/operator_audit/operator_feynman_audit.json"
    )
    report = build_report(root)
    output = output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    summary = {
        "status": report["status"],
        "check_count": report["check_count"],
        "failed_checks": len(report["failed_checks"]),
        "output": str(output),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "verified" else 1


if __name__ == "__main__":
    raise SystemExit(main())
