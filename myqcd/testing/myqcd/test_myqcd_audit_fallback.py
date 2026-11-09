"""CLI fallback and top-level discoverability tests without refer/papers."""

import pytest

from myqcd import audit


def _core_ok():
    return {
        "status": "verified",
        "derivation_count": 0,
        "failed_checks": [],
        "checks": {},
    }


def _missing_index(*args, **kwargs):
    raise FileNotFoundError(
        2, "No such file or directory", "refer/papers/INDEX.md"
    )


def test_missing_inventory_is_skipped(monkeypatch, tmp_path):
    monkeypatch.setattr(audit, "run_core_checks", _core_ok)
    monkeypatch.setattr(audit, "scan_refer_papers", _missing_index)

    report, inventory = audit._build_audit_bundle(tmp_path)

    assert report["status"] == "verified_core_without_inventory"
    assert report["inventory"]["skipped"] is True
    assert "INDEX.md" in report["inventory"]["reason"]
    assert inventory is None


def test_requested_paper_ids_require_inventory(monkeypatch, tmp_path):
    monkeypatch.setattr(audit, "run_core_checks", _core_ok)
    monkeypatch.setattr(audit, "scan_refer_papers", _missing_index)

    with pytest.raises(ValueError, match="论文公式清单不可用"):
        audit._build_audit_bundle(tmp_path, paper_ids=("P01",))


def test_top_level_submodules_are_available():
    import myqcd

    assert myqcd.gamma.gamma_basis_rank() == 16
    assert myqcd.color.N_COLORS == 3
    assert myqcd.operators.DIRAC_STRUCTURE_LABELS
    assert myqcd.feynman.PARTICLE_STYLES
    assert callable(myqcd.diagram_export.render)
