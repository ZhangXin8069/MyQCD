# Reading guide

Choose a path by goal.

| Goal | Pages |
|---|---|
| Build a bilinear operator | `operators`, `operator-basis`, `lattice-operators` |
| Understand gamma/color conventions | `gamma-traces`, `color-algebra`, `lorentz` |
| Reproduce a Fierz identity | `fierz`, `worked-examples` |
| Write QCD Feynman rules | `qcd-rules`, `qcd-rules` + `diagrams` |
| Draw or export a diagram | `diagrams`, `diagram-formats`, `topology` |
| Check lattice kinematics | `lattice-geometry`, `statistics` |
| Learn by running code | `tutorial`, `worked-examples` |
| Check API names | `api-reference`, `glossary` |

## Three reading orders

1. **Physics first:** `overview` → `operators` → `operator-basis` → `fierz`
   → `qcd-rules` → `diagrams`.
2. **Code first:** `tutorial` → `worked-examples` → `api-reference`.
3. **Audit first:** `usage` → `operator-audit` command → `topology` →
   `diagram-formats`.

## Notation

- Euclidean metric $\delta_{\mu\nu}$; $\varepsilon_{0123}=+1$.
- DR gamma indices: $0=I$, $1$–$4$ spatial/temporal, $5=\gamma_5$.
- $V=3$ mass dimension of a bilinear; each derivative adds $1$.
- $L=E_{\mathrm{int}}-V+C$ is the loop number.

## Where the boundaries are

The library is an **exact algebraic audit layer**, not a numerical lattice
ensemble, loop-integral package or continuum extrapolation tool. Pages
state their own evidence boundaries; the glossary defines the shared terms.
