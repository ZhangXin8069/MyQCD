# Migration notes

## From PyQCD conventions

- Use `gamma(0)` as the identity sentinel, `gamma(4)` as temporal.
- The DR basis has `gamma5 = diag(1,1,-1,-1)`; do not substitute a chiral
  basis without a transformation.
- PyQCD's `gamma_mu` representative is the temporal component in historical
  `_baroperator` tables; `myqcd.operators` uses explicit component names
  (`V1`–`V4`).

## Color normalization

The historical `myqcd.derivations` SU(3) code uses the anti-Hermitian
normalization `tr(T^aT^b) = -delta^{ab}/2`. `myqcd.color` and
`myqcd.color_traces` use `+delta^{ab}/2`. Convert signs before comparing
Casimirs or f/d contractions.

## Fierz signs

The Fierz engine uses the dual basis and Euclidean Gram signs. A Minkowski
or different gamma representation requires a basis conversion; do not
transplant coefficients blindly.

## CLI behavior

`python -m myqcd` skips the paper inventory when `refer/papers/INDEX.md` is
absent (`verified_core_without_inventory`). Requesting paper IDs or an
inventory JSON exits with code 2.

## Packaging

Only sdist is published. `pyproject.toml`, `MANIFEST.in`, `README.zh-CN.md`
and `myqcd/py.typed` must stay tracked; the whitelist `.gitignore` can hide
extensionless files if an exception is missing.
