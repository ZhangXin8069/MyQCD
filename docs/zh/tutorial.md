# 教程：从 gamma 代数到费曼图

本教程用一次会话走完算符层与图层。每个代码块都由文档契约测试实际执行。

## 1. 环境与代数

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

## 2. 一个 π 介子插值算符

```python
pion = operators.BilinearOperator("O_pi", "u", "d", "P")
assert pion.parity_sign == -1
assert pion.charge_conjugation_sign == 1
assert pion.pyqcd_gamma_index == 5
print(pion.latex())
```

## 3. 把矩阵分解到 Dirac 双线性

```python
matrix = gamma.gamma(1) * gamma.gamma(2) + gamma.gamma5()
coefficients = operators.decompose_dirac_bilinear(matrix)
assert sp.simplify(coefficients["T12"] - 1) == 0
assert sp.simplify(coefficients["P"] - 1) == 0
assert (
    operators.reconstruct_dirac_bilinear(coefficients) - matrix
).is_zero_matrix
```

## 4. Fierz 重排

```python
scalar = fierz.fierz_transform("S", "S")
assert scalar[("S", "S")] == sp.Rational(1, 4)
assert scalar[("A1", "A1")] == -sp.Rational(1, 4)
mixed = fierz.fierz_transform("S", "V1")
assert mixed[("S", "V1")] == sp.Rational(1, 4)
```

## 5. 传播子与 Ward 恒等式

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

## 6. 构建并导出费曼图

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

## 7. 导数算符与审计

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

运行完整结构审计：

```bash
python -m myqcd.operator_audit
```

该命令报告 48 项检查，覆盖 Clifford 代数、颜色迹、Fierz 变换、QCD 规则、
算符计数、拓扑与导出。
