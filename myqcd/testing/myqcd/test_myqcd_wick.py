from __future__ import annotations

import pytest

from myqcd import derive_wick_pairing_enumeration
from myqcd.formula_registry import CORE_FORMULAS
from myqcd.wick import (
    FermionField,
    WickPairing,
    count_wick_pairings,
    enumerate_wick_pairings,
    fermion_fields,
)


def test_grassmann_sign_depends_on_interleaved_field_order() -> None:
    interleaved = (FermionField.anti("u"), FermionField.quark("u"))
    blocked = fermion_fields(("u",), ("u",))

    assert enumerate_wick_pairings(interleaved) == (WickPairing((0,), -1),)
    assert enumerate_wick_pairings(blocked) == (WickPairing((0,), 1),)


def test_two_meson_pairings_include_both_signs() -> None:
    fields = (
        FermionField.anti("u"),
        FermionField.quark("u"),
        FermionField.anti("u"),
        FermionField.quark("u"),
    )

    pairings = enumerate_wick_pairings(fields)

    assert {(item.quark_to_antiquark, item.sign) for item in pairings} == {
        ((0, 1), -1),
        ((1, 0), 1),
    }


@pytest.mark.parametrize(
    ("quarks", "antiquarks", "expected"),
    [
        (("u",), ("u",), 1),
        (
            ("u", "d", "u", "d", "u", "d"),
            ("u", "d", "u", "d", "u", "d"),
            36,
        ),
        (
            ("u", "d", "u", "u", "d", "u", "d", "u", "d"),
            ("u", "d", "u", "u", "d", "u", "d", "u", "d"),
            2880,
        ),
        (
            ("u", "u", "u", "d", "d", "d"),
            ("u", "u", "u", "d", "d", "d"),
            36,
        ),
    ],
)
def test_reference_fixture_counts(
    quarks: tuple[str, ...],
    antiquarks: tuple[str, ...],
    expected: int,
) -> None:
    fields = fermion_fields(quarks, antiquarks)

    assert count_wick_pairings(fields) == expected
    assert len(enumerate_wick_pairings(fields)) == expected


def test_invalid_flavor_content_and_field_types_are_rejected() -> None:
    with pytest.raises(ValueError, match="unbalanced quark/antiquark count"):
        enumerate_wick_pairings((FermionField.quark("u"),))

    with pytest.raises(ValueError, match="flavor content must match exactly"):
        enumerate_wick_pairings(
            (FermionField.quark("u"), FermionField.anti("d"))
        )

    with pytest.raises(TypeError, match="FermionField"):
        enumerate_wick_pairings(("u", "u"))  # type: ignore[arg-type]

    with pytest.raises(ValueError, match="permutation"):
        WickPairing((1,), 1)


def test_wick_pairing_derivation_is_registered_in_core_audit_result() -> None:
    result = derive_wick_pairing_enumeration()

    assert result.status == "verified"
    assert all(result.checks.values())
    assert result.equations["fixture_counts"] == {
        "pn": 36,
        "ppn": 2880,
        "delta++delta-": 36,
    }
    assert result.equations["pipi_sign_distribution"] == {-1: 1, 1: 1}
    assert CORE_FORMULAS["wick_pairing_enumeration"].status == "verified"
