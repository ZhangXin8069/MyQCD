"""Exact flavor-respecting Wick pairing enumeration.

The original fermion-field order is part of the definition of the
correlator.  Reordering that input changes the Grassmann sign even when the
set of pairings is unchanged, so callers must pass fields in the order in
which they appear in the operator product.
"""

from __future__ import annotations

import itertools
import math
from collections import defaultdict
from dataclasses import dataclass
from typing import DefaultDict, Iterable, Tuple


@dataclass(frozen=True)
class FermionField:
    """One quark or antiquark field in an ordered fermion product."""

    flavor: str
    antiquark: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.flavor, str) or not self.flavor.strip():
            raise ValueError("fermion flavor must be a nonempty string")
        if self.flavor != self.flavor.strip():
            raise ValueError("fermion flavor must not contain outer whitespace")
        if not isinstance(self.antiquark, bool):
            raise TypeError("antiquark must be a bool")

    @classmethod
    def quark(cls, flavor: str) -> "FermionField":
        return cls(flavor=flavor, antiquark=False)

    @classmethod
    def anti(cls, flavor: str) -> "FermionField":
        return cls(flavor=flavor, antiquark=True)


@dataclass(frozen=True)
class WickPairing:
    """A quark-to-antiquark matching and its Grassmann reordering sign."""

    quark_to_antiquark: Tuple[int, ...]
    sign: int

    def __post_init__(self) -> None:
        if self.sign not in (-1, 1):
            raise ValueError("Wick sign must be +1 or -1")
        if any(
            not isinstance(index, int) or isinstance(index, bool) or index < 0
            for index in self.quark_to_antiquark
        ):
            raise ValueError("Wick pairing indices must be nonnegative integers")
        if tuple(sorted(self.quark_to_antiquark)) != tuple(
            range(len(self.quark_to_antiquark))
        ):
            raise ValueError("Wick pairing indices must form a permutation from zero")


def fermion_fields(
    quarks: Iterable[str], antiquarks: Iterable[str]
) -> Tuple[FermionField, ...]:
    """Build an all-quarks-then-all-antiquarks field order.

    This convenience function is suitable for explicitly spinor-ordered
    blocks.  For an interleaved operator product, construct ``FermionField``
    values directly in the physical order.
    """

    return tuple(FermionField.quark(flavor) for flavor in quarks) + tuple(
        FermionField.anti(flavor) for flavor in antiquarks
    )


def _field_partition(
    fields: Iterable[FermionField],
) -> Tuple[
    Tuple[FermionField, ...],
    Tuple[int, ...],
    Tuple[int, ...],
    DefaultDict[str, list[int]],
    DefaultDict[str, list[int]],
]:
    ordered = tuple(fields)
    if any(not isinstance(field, FermionField) for field in ordered):
        raise TypeError("fields must contain only FermionField values")

    quark_positions = tuple(
        index for index, field in enumerate(ordered) if not field.antiquark
    )
    antiquark_positions = tuple(
        index for index, field in enumerate(ordered) if field.antiquark
    )
    if len(quark_positions) != len(antiquark_positions):
        raise ValueError(
            "unbalanced quark/antiquark count: "
            f"{len(quark_positions)} != {len(antiquark_positions)}"
        )

    quarks_by_flavor: DefaultDict[str, list[int]] = defaultdict(list)
    antiquarks_by_flavor: DefaultDict[str, list[int]] = defaultdict(list)
    for quark_index, field_index in enumerate(quark_positions):
        quarks_by_flavor[ordered[field_index].flavor].append(quark_index)
    for antiquark_index, field_index in enumerate(antiquark_positions):
        antiquarks_by_flavor[ordered[field_index].flavor].append(antiquark_index)

    if {
        flavor: len(indices) for flavor, indices in quarks_by_flavor.items()
    } != {
        flavor: len(indices)
        for flavor, indices in antiquarks_by_flavor.items()
    }:
        raise ValueError("quark and antiquark flavor content must match exactly")

    return (
        ordered,
        quark_positions,
        antiquark_positions,
        quarks_by_flavor,
        antiquarks_by_flavor,
    )


def _permutation_sign(positions: Iterable[int]) -> int:
    ordered = tuple(positions)
    inversions = sum(
        left > right
        for left_index, left in enumerate(ordered)
        for right in ordered[left_index + 1 :]
    )
    return -1 if inversions % 2 else 1


def count_wick_pairings(fields: Iterable[FermionField]) -> int:
    """Count exact-flavor pairings without materializing them."""

    _, _, _, quarks_by_flavor, _ = _field_partition(fields)
    return math.prod(
        math.factorial(len(indices)) for indices in quarks_by_flavor.values()
    )


def enumerate_wick_pairings(
    fields: Iterable[FermionField],
) -> Tuple[WickPairing, ...]:
    """Enumerate all exact-flavor pairings in deterministic order.

    ``quark_to_antiquark[q]`` is the position of the antiquark in original
    antiquark order paired with the ``q``-th quark.  The sign is the parity
    of moving the original fields into
    ``q_0 ... q_n bar_pi(0) ... bar_pi(n)``.  Gamma matrices, color tensors,
    source conjugation, and any correlator-wide Berezin convention are outside
    this combinatorial layer and must be supplied by the caller.
    """

    (
        _,
        quark_positions,
        antiquark_positions,
        quarks_by_flavor,
        antiquarks_by_flavor,
    ) = _field_partition(fields)

    flavors = sorted(quarks_by_flavor)
    choices = tuple(
        tuple(itertools.permutations(antiquarks_by_flavor[flavor]))
        for flavor in flavors
    )

    pairings = []
    for selected in itertools.product(*choices):
        mapping = [-1] * len(quark_positions)
        for flavor, antiquark_order in zip(flavors, selected):
            for quark_index, antiquark_index in zip(
                quarks_by_flavor[flavor], antiquark_order
            ):
                mapping[quark_index] = antiquark_index
        ordered_positions = quark_positions + tuple(
            antiquark_positions[index] for index in mapping
        )
        pairings.append(
            WickPairing(
                quark_to_antiquark=tuple(mapping),
                sign=_permutation_sign(ordered_positions),
            )
        )
    return tuple(pairings)


__all__ = [
    "FermionField",
    "WickPairing",
    "count_wick_pairings",
    "enumerate_wick_pairings",
    "fermion_fields",
]
