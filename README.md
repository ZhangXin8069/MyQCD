# MyQCD

**English** | [中文](https://gitlab.itp.ac.cn/zhangxin8069/MyQCD/-/blob/main/README.zh-CN.md)

MyQCD provides executable audits for the lattice-QCD formulas used by PyQCD. It
splits a physics report into SymPy-checkable derivations, a source registry, and
independent operator-construction and Feynman-diagram layers. Reference
libraries are read-only Git submodules; GPL-3.0 or unlicensed upstream content is
never copied.

## Install

```bash
pip install myqcd
```

Requirements: Python 3.10+ and SymPy 1.12+. The complete test suite is currently
exercised on Python 3.12 with SymPy 1.14.

Check an installation without any source checkout:

```bash
python -m myqcd.operator_audit
python -m myqcd
```

`python -m myqcd` runs the core formula checks. When `refer/papers/INDEX.md` is
unavailable it skips the paper inventory and reports
`verified_core_without_inventory`; the core checks still run.

## Documentation

* English — https://myqcd.readthedocs.io/en/latest/
* 中文 — https://myqcd.readthedocs.io/zh-cn/latest/

## Repositories

| Platform | Role | URL |
|---|---|---|
| GitLab (gitlab.itp.ac.cn) | 国内开发 — primary development | https://gitlab.itp.ac.cn/zhangxin8069/MyQCD |
| Gitee | 国内发布 — China release mirror | https://gitee.com/zhangxin8069/MyQCD |
| GitHub | 国外发布 — global release mirror | https://github.com/zhangxin8069/MyQCD |

## Quick start

```python
import sympy as sp

from myqcd import color, diagram_export, feynman, gamma, operators

assert gamma.gamma_basis_rank() == 16
assert gamma.trace_gamma_product((1, 1)) == 4
assert color.casimir_fundamental() == sp.Rational(4, 3)

operator = operators.BilinearOperator(
    name="O_V4", left_flavor="u", right_flavor="d", structure="V4"
)
assert operator.pyqcd_gamma_index == 4
assert operator.mass_dimension == 3

triangle = feynman.Diagram(
    vertices=("a", "b", "c"),
    edges=(
        feynman.Edge(0, 1, "gluon"),
        feynman.Edge(1, 2, "gluon"),
        feynman.Edge(2, 0, "gluon"),
    ),
)
assert triangle.loop_count == 1
assert diagram_export.to_tikz(triangle).startswith("%")
```

## Operators and diagrams

`myqcd` exposes all 16 Dirac bilinears with exact parity/C signs, mass
dimension, and PyQCD gamma indices:

| Class | Structures | Count |
|---|---|---|
| S | `I` | 1 |
| P | `γ₅` | 1 |
| V | `γμ` | 4 |
| A | `γμγ₅` | 4 |
| T | `σμν` | 6 |

The full table and the comparison with standard Dirac/SU(3) values are in
[Operators](https://myqcd.readthedocs.io/en/latest/operators.html). The
documentation renders the same formulas with LaTeX.

![Sunset two-loop diagram](https://myqcd.readthedocs.io/en/latest/_images/sunset_two_loop.svg)

Diagram examples (two-point chain, three-gluon triangle, one-loop quark
self-energy, two-loop sunset and Wick pairing) with loop counts and
TikZ/DOT/SVG export are in
[Feynman diagrams](https://myqcd.readthedocs.io/en/latest/diagrams.html).

## What is inside

| Module | Content |
|---|---|
| `myqcd.audit` | Core formula checks, paper inventory and JSON report |
| `myqcd.pyqcd_theory_audit` | PyQCD gamma, vertex, Wilson-line, Clover, ratio and TMD boundary audits |
| `myqcd.derivations` | SymPy derivations for lattice gauge theory, flow, LaMET, PDF/TMD and statistics |
| `myqcd.formula_registry` | Formula-to-source-to-derivation registry |
| `myqcd.latex_inventory` | Display-formula inventory for paper sources |
| `myqcd.wick` | Exact flavor-respecting Wick pairings with Grassmann signs |
| `myqcd.gamma` | DeGrand--Rossi gamma basis, trace theorem and 16 Dirac structures |
| `myqcd.color` | SU(3) generators, structure constants, Casimirs and color Fierz identity |
| `myqcd.color_traces` | SU(3) trace, f/d contractions and generic Casimir formulas |
| `myqcd.gamma_traces` | gamma5 traces, epsilon correspondence and chiral projector traces |
| `myqcd.operators` | Dirac bilinear decomposition, parity/C classification and PyQCD index mapping |
| `myqcd.lorentz` | Euclidean epsilon contractions, Schouten identity, transverse and spin-2 projectors |
| `myqcd.fierz` | General 16-basis Dirac Fierz transformations with exact coefficients |
| `myqcd.operator_basis` | Derivative operators, chiral combinations, color representations and operator tables |
| `myqcd.qcd_rules` | Symbolic QCD propagators, Ward identities, vertex factors and dimensions |
| `myqcd.renormalization` | RI/MOM projectors, Z factors and mixing-matrix algebra |
| `myqcd.wilson` | Symbolic Wilson-path products and gauge-covariance checks |
| `myqcd.matching` | Tree-level matching, Fourier prefactor and hybrid switch |
| `myqcd.evolution` | Single-exponent RGE evolution and anomalous dimensions |
| `myqcd.symmetry` | Vertex automorphisms and parallel-edge exchange counts |
| `myqcd.lattice` | Lattice momenta, Fourier phases and dispersion relations |
| `myqcd.statistics` | Jackknife, bootstrap and effective-mass estimators |
| `myqcd.feynman` | Diagram structures, QCD rule catalog, Wick pairing graphs and loop counting |
| `myqcd.topology` | Graph invariants, isomorphism, topology enumeration and builders |
| `myqcd.diagram_export` | Zero-dependency JSON, Mermaid, LaTeX, TikZ, DOT and SVG export |
| `myqcd.operator_audit` | One-command audit for the operator and diagram layers |

## Entry points

```bash
python -m myqcd
python -m myqcd.operator_audit --root .
python -m myqcd.pyqcd_theory_audit --root .
```

`python -m myqcd.operator_audit` writes
`logs/data/operator_audit/operator_feynman_audit.json` under the current
directory and exits non-zero if any check fails.

## Evidence boundary

- `verified` covers only the algebra, dimensions, finite-dimensional proxies and
  combinatorial identities that are actually checked.
- No claim is made for loop integrals, nonperturbative matrix elements, real
  ensembles, GPU numerics, soft/rapidity closure or the continuum limit.
- `myqcd.color` uses the Hermitian normalization `Tr[T^aT^b] = +delta^{ab}/2`;
  the historical SU(3) derivations in `myqcd.derivations` use the anti-Hermitian
  `-delta^{ab}/2`. The two conventions must not be mixed.
- Diagram export guarantees combinatorial structure and string format only; it
  does not prove symmetry factors or loop-integral results.

## License

MIT. See `LICENSE`.
