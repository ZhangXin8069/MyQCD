# Tutorial: from gamma algebra to diagrams

This tutorial walks through the operator and diagram layers in one session.
Every code block is executed by the documentation contract tests.

## 1. Environment and algebra

```python
import sympy as sp

from myqcd import (
    color,
    diagram_export,
    feynman,
    fierz,
    gamma,
    lorentz,
    operator_basis,
    operators,
    qcd_rules,
    topology,
)

assert gamma.gamma_basis_rank() == 16
assert gamma.trace_gamma_product((1, 1)) == 4
assert color.casimir_fundamental() == sp.Rational(4, 3)
```

## 2. A pion interpolating operator

```python
pion = operators.BilinearOperator("O_pi", "u", "d", "P")
assert pion.parity_sign == -1
assert pion.charge_conjugation_sign == 1
assert pion.pyqcd_gamma_index == 5
print(pion.latex())
```

## 3. Decompose a matrix into Dirac bilinears

```python
matrix = gamma.gamma(1) * gamma.gamma(2) + gamma.gamma5()
coefficients = operators.decompose_dirac_bilinear(matrix)
assert sp.simplify(coefficients["T12"] - 1) == 0
assert sp.simplify(coefficients["P"] - 1) == 0
assert (
    operators.reconstruct_dirac_bilinear(coefficients) - matrix
).is_zero_matrix
```

## 4. Fierz rearrangement

```python
scalar = fierz.fierz_transform("S", "S")
assert scalar[("S", "S")] == sp.Rational(1, 4)
assert scalar[("A1", "A1")] == -sp.Rational(1, 4)
mixed = fierz.fierz_transform("S", "V1")
assert mixed[("S", "V1")] == sp.Rational(1, 4)
```

## 5. Propagators and Ward identity

```python
p = lorentz.vector_components("p")
m = sp.Symbol("m", positive=True)
assert qcd_rules.quark_propagator_residual(p, m).is_zero_matrix
assert qcd_rules.ward_identity_residual(p).is_zero_matrix
assert all(
    qcd_rules.gluon_transversality(p, nu, gauge_parameter=0) == 0
    for nu in range(4)
)
```

## 6. Build and export a diagram

```python
triangle = feynman.Diagram(
    vertices=("a", "b", "c"),
    edges=(
        feynman.Edge(0, 1, "gluon"),
        feynman.Edge(1, 2, "gluon"),
        feynman.Edge(2, 0, "gluon"),
    ),
)
assert triangle.loop_count == 1
assert topology.is_cycle(triangle)
assert diagram_export.to_mermaid(triangle).startswith("flowchart LR")
assert "\\begin{tabular}" in diagram_export.to_latex_table(triangle)
```

## 7. Derivative operator and audit

```python
twist = operator_basis.DerivativeOperator(
    "O_twist2", "V3", derivatives=2, color="octet"
)
assert twist.mass_dimension == 5
assert twist.pyqcd_gamma_index == 3
assert operator_basis.enumerate_derivative_operators(
    ("u",), max_derivatives=1, colors=("singlet",)
)
```

Run the full structural audit:

```bash
python -m myqcd.operator_audit
```

The command reports 48 checks covering Clifford algebra, color traces,
Fierz transformations, QCD rules, operator counting, topology and exports.
