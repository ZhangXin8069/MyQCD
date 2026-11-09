# 用法

## 审计算符层与图层

```bash
python -m myqcd.operator_audit --root .
```

命令写出 `logs/data/operator_audit/operator_feynman_audit.json`；任一检查失败
时返回非零退出码。

它验证 Clifford 代数、16 个 Dirac 结构的秩、迹定理与显式矩阵的一致性、
SU(3) Fierz 恒等式、双线性分解往返、Wick 配对图、圈数与导出器。

## 使用代数层

```python
import sympy as sp

from myqcd import color, gamma, operators

assert gamma.gamma_basis_rank() == 16
assert gamma.trace_gamma_product((1, 1)) == 4
assert color.casimir_fundamental() == sp.Rational(4, 3)

operator = operators.BilinearOperator(
    name="O_V4", left_flavor="u", right_flavor="d", structure="V4"
)
assert operator.pyqcd_gamma_index == 4
assert operator.mass_dimension == 3
```

## 构建并导出费曼图

```python
from myqcd import diagram_export, feynman

triangle = feynman.Diagram(
    vertices=("a", "b", "c"),
    edges=(
        feynman.Edge(0, 1, "gluon"),
        feynman.Edge(1, 2, "gluon"),
        feynman.Edge(2, 0, "gluon"),
    ),
)
assert triangle.loop_count == 1
assert diagram_export.to_tikz(triangle).startswith("%")
assert diagram_export.to_dot(triangle).startswith("digraph")
assert diagram_export.to_svg(triangle).startswith("<?xml")
```

## Wick 配对

```python
from myqcd import wick

fields = wick.fermion_fields(["u"], ["u"])
pairings = wick.enumerate_wick_pairings(fields)
assert len(pairings) == 1
assert pairings[0].sign in (-1, 1)
```
