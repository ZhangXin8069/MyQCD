# Validation

`myqcd` separates exact algebra, structural checks, publication metadata and
numerical-lattice evidence.

## Evidence levels

| Level | Meaning | Example |
|---|---|---|
| `verified` | exact algebra/combinatorics executed | Clifford, Fierz, color traces |
| `structural` | algebraic closure with declared assumptions | hybrid matching, Fourier prefactor |
| `inferred` | derived from an external convention | limit proxies |
| `unverified` | requires loops, ensembles or continuum | TMD soft factor |

## Commands

```bash
python -m myqcd.operator_audit
python -m myqcd.pyqcd_theory_audit --root .
python -m pytest
```

The audit writes machine-readable JSON. The test suite currently has 298
passing tests; 11 remaining failures are the missing `refer/papers`
environment data, not algebra regressions.

## Release gates

- sdist only; `twine check` PASSED.
- `myqcd/py.typed`, both READMEs and `pyproject.toml` tracked.
- Clean-venv install from PyPI; `python -m myqcd` must degrade gracefully
  when `refer/papers/INDEX.md` is absent.
- Sphinx `-W` both languages; bilingual code blocks identical.
- Double push to GitLab and Gitee; GitHub follows the Gitee mirror.

## Not claimed

Loop integrals, nonperturbative matrix elements, real ensembles, GPU
numerics, soft/rapidity closure, continuum extrapolation and complete
renormalization fits.
