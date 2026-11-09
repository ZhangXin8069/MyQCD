# Design

`myqcd` is an exact algebraic audit layer. The design keeps four boundaries
explicit: representation, operator structure, diagram combinatorics and
numerical ensembles.

## Layers

| Layer | Modules | Responsibility |
|---|---|---|
| Representation | `gamma`, `gamma_traces`, `color`, `color_traces`, `lorentz` | exact matrices, traces and tensor identities |
| Operator | `operators`, `operator_basis`, `fierz` | bilinears, derivatives, chiral/color structures and Fierz |
| Diagram | `feynman`, `topology`, `diagram_export`, `qcd_rules` | graph invariants, rules and export |
| Lattice | `lattice`, `statistics`, `wick` | kinematics, resampling and pairings |
| Audit | `operator_audit`, `pyqcd_theory_audit` | machine-readable checks |

## Invariants

1. **Exactness:** every algebraic result is a SymPy expression, not a float
   approximation.
2. **Convention pinning:** DR gamma indices, Euclidean metric, $+1/2$ color
   normalization and $C=\gamma_4\gamma_2$ are stated in public docstrings.
3. **Evidence boundaries:** a `verified` status covers the checks actually
   executed; loops, ensembles and continuum limits are separate.
4. **No hidden dependency:** the operator/diagram layer uses SymPy plus the
   standard library; export formats are strings.

## Data flow

```
operator definition
  -> Dirac/color/Lorentz algebra
  -> Wick pairing or diagram
  -> loop/topology invariants
  -> JSON/Mermaid/LaTeX/TikZ/DOT/SVG
```

The audit entry `python -m myqcd.operator_audit` exercises all four stages
and writes a JSON report. It does not run external code or read an ensemble.

## Non-goals

The package is not a numerical contraction engine, a Mathematica replacement,
a loop-integral library or a fit framework. Those responsibilities belong
to PyQCD, FeynCalc or dedicated numerical packages.
