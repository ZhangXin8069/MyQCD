"""Operator/diagram audit covers the complex diagram samples."""

from pathlib import Path

from myqcd import operator_audit

ROOT = Path(__file__).resolve().parents[3]


def test_complex_diagram_checks_are_present():
    report = operator_audit.build_report(ROOT)
    assert report["status"] == "verified"
    assert report["check_count"] >= 46
    for name in (
        "image_self_energy_loop_one",
        "sunset_loop_count_two",
        "external_legs_not_counted",
        "parallel_edges_are_curved",
        "lorentz_epsilon_double_contract",
        "fierz_scalar_scalar",
        "operator_basis_count",
        "qcd_quark_propagator",
    ):
        assert report["checks"][name]
    assert report["diagram_samples"]["sunset"]["loop_count"] == 2
    assert report["diagram_samples"]["self_energy"]["internal_edge_count"] == 2
