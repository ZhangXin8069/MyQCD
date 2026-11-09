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

from . import color, diagram_export, feynman, gamma, operators, wick


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
        "triangle_connected": _diagram_triangle().is_connected,
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
        default=Path(__file__).resolve().parents[1],
        help="MyQCD 工作区根目录",
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
