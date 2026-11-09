# 快速开始

## 安装

```bash
pip install myqcd
```

Python 3.10+ 与 SymPy 1.12+；完整套件在 Python 3.12 上执行。

## 第一次审计

```bash
python -m myqcd.operator_audit
```

命令打印 JSON 摘要，并在当前目录写出
`logs/data/operator_audit/operator_feynman_audit.json`。

## 第一个算符

```python
import sympy as sp

from myqcd import gamma, operators

pion = operators.BilinearOperator("O_pi", "u", "d", "P")
assert pion.mass_dimension == 3
assert pion.parity_sign == -1
assert pion.charge_conjugation_sign == 1
assert pion.pyqcd_gamma_index == 5
assert gamma.trace_gamma_product((1, 1)) == 4
print(pion.latex())
```

## 第一次 Fierz 检查

```python
import sympy as sp

from myqcd import fierz

coefficients = fierz.fierz_transform("S", "S")
assert coefficients[("S", "S")] == sp.Rational(1, 4)
assert coefficients[("A1", "A1")] == -sp.Rational(1, 4)
print(len(coefficients))
```

## 第一张图

```python
from myqcd import diagram_export, topology

triangle = topology.build_cycle(3)
assert triangle.loop_count == 1
assert diagram_export.to_mermaid(triangle).startswith("flowchart LR")
print(diagram_export.export_audit(triangle)["formats"])
```

## 下一步

| 目标 | 页面 |
|---|---|
| 学习完整流程 | `tutorial` |
| 查看可执行检查 | `worked-examples` |
| 查某个量 | `reference-values` |
| 理解约定 | `conventions` |
| 查 API 名称 | `api-reference` |

## 边界

快速开始检查精确代数与结构。它不安装或读取格点系综、不计算圈积分、
不做连续极限外推。
