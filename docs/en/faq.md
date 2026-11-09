# FAQ

## Is `myqcd` a replacement for PyQCD?

No. PyQCD is the lattice-QCD numerical package; `myqcd` is an exact
algebraic audit and operator/diagram layer that references PyQCD as its
source of conventions.

## Does it compute loop integrals?

No. It provides propagators, vertices, projectors and algebraic identities;
loop integrals and ensemble fits are outside the package.

## Why Euclidean conventions?

The target is lattice QCD: $\delta_{\mu\nu}$, Hermitian gamma matrices and
$\varepsilon_{0123}=+1$. Minkowski signs differ and must be converted
explicitly.

## Why do some Fierz coefficients have minus signs?

The 16-basis Gram matrix is not uniformly positive in Euclidean space; the
dual basis $\Gamma^A=\Gamma_A/g_A$ is used. The signs are checked against
the component matrix identity and random spinors.

## Why is `gamma(0)` the identity?

PyQCD's DeGrand–Rossi API uses index 0 as an identity sentinel; the temporal
matrix is `gamma(4)`, not `gamma(0)`.

## Why is `T13` missing a PyQCD index?

PyQCD stores `gamma(7)=gamma3 gamma1=-sigma13`; there is no exact
`sigma13` entry. The mapping returns `None` rather than silently changing
the sign.

## Why does the CLI skip the paper inventory?

`python -m myqcd` needs `refer/papers/INDEX.md`. When it is absent, the core
checks still run and the report says `verified_core_without_inventory`.
Requesting specific paper IDs or an inventory JSON exits with code 2.

## Why is no symmetry factor assigned?

A symmetry factor depends on identical-particle content and vertex-exchange
conventions. `myqcd.topology` deliberately exposes graph invariants only.

## How do I add an operator?

Use `operators.BilinearOperator` or
`operator_basis.DerivativeOperator`; validate `structure`, `derivatives`,
`color` and flavors.

## How do I export a diagram?

Use `diagram_export` for JSON, Mermaid, LaTeX, TikZ, DOT or SVG. The formats
are structural; no external process is invoked.

## What is not covered?

Loop integrals, nonperturbative matrix elements, real ensembles, GPU
numerics, soft/rapidity resummation, continuum extrapolation and full
renormalization fits.
