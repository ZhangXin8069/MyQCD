# Summary

`myqcd` is an exact algebraic audit layer for lattice QCD. The current
checkpoint adds operator construction, Feynman-diagram structure, Lorentz
and color algebra, QCD rules, lattice kinematics and statistics, with
bilingual documentation and PyPI/RTD delivery.

## Module map

| Layer | Modules |
|---|---|
| Representation | `gamma`, `gamma_traces`, `color`, `color_traces`, `lorentz` |
| Operator | `operators`, `operator_basis`, `fierz` |
| Diagram | `feynman`, `topology`, `diagram_export`, `qcd_rules` |
| Lattice | `lattice`, `statistics`, `wick` |
| Audit | `operator_audit`, `pyqcd_theory_audit` |
| Core audit | `audit`, `derivations`, `formula_registry`, `latex_inventory` |

## Documentation map

| Goal | Pages |
|---|---|
| Learn by running | `tutorial`, `worked-examples`, `case-studies` |
| Operator basis | `operators`, `operator-basis`, `operator-catalog`, `lattice-operators` |
| Algebra | `lorentz`, `fierz`, `gamma-traces`, `gamma-catalog`, `color-algebra`, `color-catalog` |
| Rules and diagrams | `qcd-rules`, `vertex-catalog`, `diagrams`, `diagram-catalog`, `diagram-formats`, `topology` |
| Lattice and statistics | `lattice-geometry`, `statistics` |
| Reference | `api-reference`, `glossary`, `notation`, `conventions`, `reference-values` |
| Operations | `validation`, `release-checklist`, `troubleshooting`, `migration`, `comparison`, `limitations`, `roadmap` |

## Evidence levels

- `verified`: exact SymPy algebra or combinatorics executed in this session.
- `structural`: algebraic closure with stated assumptions.
- `inferred`: derived from an explicit convention.
- `unverified`: requires loops, ensembles or the continuum limit.

## Metrics

| Scope | Lines |
|---|---|
| Baseline operator/diagram subsystem | 2,443 |
| Current code (16 modules) | 3,835 |
| Current tests (16 files) | 1,450 |
| Current bilingual docs (42 pages) | 5,491 |
| Documentation relative to the 546-line baseline | 10.06× |
| Code + tests + docs total | 10,776 (4.41× baseline) |

The line counts are physical `wc -l` counts. They measure coverage, not
correctness; correctness is guarded by the test suite and the 48-check
operator audit.

## Commands

```bash
python -m myqcd.operator_audit
python -m myqcd.pyqcd_theory_audit --root .
python -m pytest
python -m sphinx -b html -W docs/en <output>
python -m sphinx -b html -W docs/zh <output>
```

## Boundaries

The package does not evaluate loop integrals, fit ensembles, assign symmetry
factors or perform a continuum extrapolation. Those are separate numerical
and phenomenological tasks.

## Next steps

Continue with renormalization projectors, Wilson-path algebra, explicit
symmetry-factor conventions, matching kernels and randomized differential
tests. The content ledger tracks the target.
