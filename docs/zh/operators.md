# 算符

`myqcd.operators` 在 PyQCD 的 DeGrand--Rossi 基中实现 16 个 Dirac 双线性。
双线性写作 `bar q_u Gamma q_d`。

## Dirac 基

| 结构 | 类别 | 宇称 | C | 量纲 | PyQCD 索引 |
|---|---|---|---|---|---|
| `S` | S | +1 | +1 | 3 | 0 |
| `P` | P | -1 | +1 | 3 | 5 |
| `V1` | V | -1 | +1 | 3 | 1 |
| `V2` | V | -1 | -1 | 3 | 2 |
| `V3` | V | -1 | +1 | 3 | 3 |
| `V4` | V | +1 | -1 | 3 | 4 |
| `A1` | A | +1 | +1 | 3 | 12 |
| `A2` | A | +1 | -1 | 3 | 13 |
| `A3` | A | +1 | +1 | 3 | 14 |
| `A4` | A | -1 | -1 | 3 | 15 |
| `T12` | T | +1 | -1 | 3 | 8 |
| `T13` | T | +1 | +1 | 3 | — |
| `T14` | T | -1 | -1 | 3 | 9 |
| `T23` | T | +1 | -1 | 3 | 6 |
| `T24` | T | -1 | +1 | 3 | 10 |
| `T34` | T | -1 | -1 | 3 | 11 |

说明：

- 宇称由 `gamma4 Gamma gamma4 = s Gamma` 计算。
- 电荷共轭由 `C^-1 Gamma C = s Gamma` 计算，其中 `C = gamma4 gamma2`。
- 零导数时质量量纲为 3。
- PyQCD 索引是精确的 `gamma(i)` 索引。`T13` 没有精确项，因为
  `gamma(7) = gamma3 gamma1 = -sigma13`。

## 复现分解

```python
import sympy as sp
from myqcd import operators

matrix = operators.structure_matrix("V4")
coefficients = operators.decompose_dirac_bilinear(matrix)
assert sp.simplify(coefficients["V4"] - 1) == 0
assert all(
    sp.simplify(value) == 0
    for name, value in coefficients.items()
    if name != "V4"
)
print(coefficients["V4"])
```

## 与标准理论值比对

下表中的数值都是 SymPy 精确结果。“标准值”指四维欧氏空间中惯用的
SU(3)/Dirac 值，不是对某个系综的拟合。

### Dirac 代数

| 恒等式 | MyQCD | 标准值 |
|---|---|---|
| `Tr[1]` | 4 | 4 |
| `Tr[gamma_mu gamma_nu]` | `4 delta_mu_nu` | `4 delta_mu_nu` |
| `Tr[gamma1 gamma1]` | 4 | 4 |
| `Tr[gamma1 gamma2]` | 0 | 0 |
| `Tr[gamma1 gamma2 gamma3 gamma4]` | 0 | 0 |
| `Tr[gamma5 gamma1 gamma2 gamma3 gamma4]` | 4 | `4 epsilon_1234 = 4` |
| `gamma5^2` | 1 | 1 |
| `{gamma5, gamma_mu}` | 0 | 0 |
| `C gamma_mu C^-1` | `-gamma_mu^T` | `-gamma_mu^T` |

### SU(3) 颜色代数

| 量 | MyQCD | 标准值 |
|---|---|---|
| `C_F` | `4/3` | `4/3` |
| `C_A` | `3` | `3` |
| `f_123` | `1` | `1` |
| `f_147` | `1/2` | `1/2` |
| `f_458` | `sqrt(3)/2` | `sqrt(3)/2` |
| `d_118` | `1/sqrt(3)` | `1/sqrt(3)` |
| `d_146` | `1/2` | `1/2` |
| `sum f^2` | `24` | `24` |
| `sum d^2` | `40/3` | `40/3` |
| `Tr[T^a T^b]` | `delta_ab/2` | `delta_ab/2` |

`myqcd.derivations` 中的历史 SU(3) 推导使用反厄米归一化 `-delta_ab/2`；
上表属于厄米的 `myqcd.color` 层，两套约定不可混用。

## 命令

```bash
python -m myqcd.operator_audit
```
