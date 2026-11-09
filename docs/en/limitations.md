# Limitations

This page lists what the operator/diagram layer deliberately does not do.

## Physics

- **No loop integrals.** The package checks propagators, vertices and
  algebraic identities; it does not evaluate Feynman integrals.
- **No ensembles.** Matrix elements, fits, continuum extrapolation and
  physical predictions require lattice data.
- **No symmetry factors.** `myqcd.topology` exposes graph invariants only;
  symmetry factors depend on particle content and exchange conventions.
- **No complete renormalization.** RI/MOM projectors and Z-factor algebra are
  available; loop coefficients and nonperturbative fits are not.
- **No gamma5 scheme machine.** The Euclidean DR basis is fixed; NDR, Larin
  and BMHV are not implemented.

## Conventions

- Color normalization differs between `myqcd.color` ($+\delta^{ab}/2$) and
  historical `myqcd.derivations` ($-\delta^{ab}/2$).
- Minkowski and Euclidean signs differ; a basis conversion is required before
  comparing numerical coefficients.
- The PyQCD `gamma_mu` representative in historical tables is temporal; use
  explicit components.

## Engineering

- Export formats are structural strings; no external renderer is invoked.
- Topology isomorphism is exact only up to eight vertices.
- The CLI degrades gracefully when `refer/papers/INDEX.md` is missing; it
  does not synthesize the missing inventory.

## Evidence rule

A `verified` result covers only the checks actually executed. Unverified
boundaries are reported explicitly rather than hidden behind a global status.
