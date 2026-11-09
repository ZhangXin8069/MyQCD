# Worked examples

Each block is a self-contained, executable check. The documentation contract
runs them in order.

## 1. Gamma and trace values

```python
from myqcd import gamma

assert gamma.gamma_basis_rank() == 16
assert gamma.trace_gamma_product((1, 1)) == 4
assert gamma.trace_gamma_product((1, 2)) == 0
assert gamma.trace_gamma_product((1, 2, 1, 2)) == -4
assert gamma.trace_gamma_product((1, 2, 2, 1)) == 4
```

## 2. SU(3) constants

```python
import sympy as sp

from myqcd import color

assert color.casimir_fundamental() == sp.Rational(4, 3)
assert color.casimir_adjoint() == 3
assert color.structure_constants()[0][1][2] == 1
assert color.structure_constants()[0][3][6] == sp.Rational(1, 2)
assert color.symmetric_constants()[0][0][7] == sp.sqrt(3) / 3
assert color.color_fierz_residual() == 0
```

## 3. Operator quantum numbers

```python
from myqcd import operators

pion = operators.BilinearOperator("O_pi", "u", "d", "P")
rho = operators.BilinearOperator("O_rho", "u", "d", "V4")
a1 = operators.BilinearOperator("O_a1", "u", "d", "A4")
assert [pion.parity_sign, rho.parity_sign, a1.parity_sign] == [-1, 1, -1]
assert [
    pion.charge_conjugation_sign,
    rho.charge_conjugation_sign,
    a1.charge_conjugation_sign,
] == [1, -1, -1]
assert [pion.pyqcd_gamma_index, rho.pyqcd_gamma_index, a1.pyqcd_gamma_index] == [5, 4, 15]
```

## 4. Non-trivial decomposition

```python
import sympy as sp

from myqcd import gamma, operators

matrix = gamma.gamma(1) * gamma.gamma(2) + 2 * gamma.gamma(3) * gamma.gamma5()
coefficients = operators.decompose_dirac_bilinear(matrix)
assert sp.simplify(coefficients["T12"] - 1) == 0
assert sp.simplify(coefficients["A3"] - 2) == 0
assert (operators.reconstruct_dirac_bilinear(coefficients) - matrix).is_zero_matrix
```

## 5. Fierz coefficients

```python
import sympy as sp

from myqcd import fierz

scalar = fierz.fierz_transform("S", "S")
assert scalar[("S", "S")] == sp.Rational(1, 4)
assert scalar[("V1", "V1")] == sp.Rational(1, 4)
assert scalar[("A1", "A1")] == -sp.Rational(1, 4)
mixed = fierz.fierz_transform("S", "V1")
assert mixed[("S", "V1")] == sp.Rational(1, 4)
assert len(mixed) == 16
```

## 6. QCD propagator and Ward identity

```python
import sympy as sp

from myqcd import lorentz, qcd_rules

p = lorentz.vector_components("p")
m = sp.Symbol("m", positive=True)
assert qcd_rules.quark_propagator_residual(p, m).is_zero_matrix
assert qcd_rules.ward_identity_residual(p).is_zero_matrix
assert all(
    qcd_rules.gluon_transversality(p, nu, gauge_parameter=0) == 0
    for nu in range(4)
)
```

## 7. Loop counts

```python
from myqcd import topology

assert topology.build_chain(3).loop_count == 0
assert topology.build_cycle(3).loop_count == 1
assert topology.build_self_energy().loop_count == 1
assert topology.build_sunset().loop_count == 2
```

## 8. Small topology enumeration

```python
from myqcd import topology

assert len(topology.enumerate_connected_topologies(3, 3)) == 1
trees = topology.enumerate_connected_topologies(4, 3)
assert len(trees) == 2
assert all(topology.is_tree(tree) for tree in trees)
```

## 9. Export formats

```python
from myqcd import diagram_export, feynman, topology

triangle = topology.build_cycle(3)
formats = diagram_export.export_audit(triangle)["formats"]
assert formats == ["dot", "json", "latex", "mermaid", "svg", "tikz"]
assert diagram_export.to_mermaid(triangle).startswith("flowchart LR")
assert diagram_export.to_json(triangle).startswith("{")
assert "\\begin{tabular}" in diagram_export.to_latex_table(triangle)
```

## 10. Lattice and statistics

```python
import math

from myqcd import lattice, statistics

p = lattice.momentum_from_indices((1, 0, 0, 0), (4, 4, 4, 8))
assert p[0] == math.pi / 2
assert lattice.lattice_dispersion((0.0, 0.0)) == 0
samples = [(1.0, 2.0), (2.0, 4.0), (3.0, 6.0)]
assert statistics.jackknife_mean(samples) == (2.0, 4.0)
assert statistics.bootstrap_indices(3, 4, seed=1) == statistics.bootstrap_indices(3, 4, seed=1)
```
