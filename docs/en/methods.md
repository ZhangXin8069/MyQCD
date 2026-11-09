# Methods

This page records how the package's claims are produced and checked.

## Exact algebra first

Every matrix, trace and contraction is a SymPy expression. The package does
not use floating-point tolerances for algebraic identities; `is_zero_matrix`
and `simplify` are used only after explicit symbolic construction.

## Dual basis and signs

The Euclidean 16-bilinear basis has Gram eigenvalues $+1$ or $-1$. Fierz
projection therefore uses the dual basis
$\Gamma^A=\Gamma_A/g_A$. The implementation is checked twice:

1. the component matrix identity
   $\Gamma_A^{ij}\Gamma_B^{kl}
   =\sum_{C,D}F_{AB}^{CD}\Gamma_C^{il}\Gamma_D^{kj}$;
2. a random complex-spinor residual below $10^{-9}$.

## Random differential tests

Trace identities, Fierz coefficients and SU(3) traces are compared against
explicit matrix products with seeded random indices. The seed makes failures
reproducible; the explicit matrices are independent of the tested shortcut.

## Diagram invariants

Topology functions use only vertices, edges and particle labels. Loop number
is $E_{\mathrm{int}}-V+C$; external-leg edges are excluded. Isomorphism is
exact by vertex permutations up to eight vertices; larger graphs use a
canonical signature and state the limitation.

## Documentation contract

The test suite parses the bilingual Markdown pages and checks:

- identical fenced code blocks in English and Chinese;
- toctree entries equal to the pages on disk;
- every Python block executes;
- the operator table matches `myqcd.operators`;
- SVG assets exist and are well-formed;
- MathJax/dollarmath is enabled;
- packaging files are tracked.

## Audit report

`python -m myqcd.operator_audit` runs 48 checks and writes JSON. A `verified`
status is local to those checks; it is not a claim about loops, ensembles or
the continuum.

## Release reproducibility

Only sdist is published. The sdist contains both READMEs, `py.typed` and
the package modules; tests and `AGENTS.md` are pruned. A fresh clone build
is verified with `git archive` when the environment cannot hold a full
clone.

## Limits of the method

The methods validate exact algebra and structure. They do not replace
numerical lattice data, loop integrals, nonperturbative renormalization or
continuum extrapolation.
