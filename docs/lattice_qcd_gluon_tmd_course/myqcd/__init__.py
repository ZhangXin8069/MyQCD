"""格点 QCD 长课程的可运行 SymPy 教学例题。"""

from __future__ import annotations

from typing import Tuple

from ._common import SymbolicExample


def all_examples() -> Tuple[SymbolicExample, ...]:
    """延迟构造全部例题，避免导入包时执行符号积分。"""

    from .group_qft import build_examples as build_group_qft
    from .lattice_spectroscopy import build_examples as build_spectroscopy
    from .renormalization_tmd import build_examples as build_tmd

    return (*build_group_qft(), *build_spectroscopy(), *build_tmd())


__all__ = ["SymbolicExample", "all_examples"]

