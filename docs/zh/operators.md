# 算符

`myqcd.operators` 在 PyQCD 的 DeGrand--Rossi 基中实现 16 个 Dirac 双线性。
双线性写作 $\bar q_u \Gamma q_d$。

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

- 宇称由 $\gamma_4 \Gamma \gamma_4 = s\,\Gamma$ 计算。
- 电荷共轭由 $C^{-1}\Gamma C = s\,\Gamma$ 计算，其中
  $C = \gamma_4\gamma_2$。
- 零导数时质量量纲为 $3$。
- PyQCD 索引是精确的 $\gamma(i)$ 索引。`T13` 没有精确项，因为
  $\gamma(7) = \gamma_3\gamma_1 = -\sigma_{13}$。

## 实例

### 非平凡分解

```python
import sympy as sp

from myqcd import gamma, operators

matrix = (
    gamma.gamma(1) * gamma.gamma(2)
    + 2 * gamma.gamma(3) * gamma.gamma5()
    + gamma.gamma5()
)
coefficients = operators.decompose_dirac_bilinear(matrix)
assert sp.simplify(coefficients["T12"] - 1) == 0
assert sp.simplify(coefficients["A3"] - 2) == 0
assert sp.simplify(coefficients["P"] - 1) == 0
assert (
    operators.reconstruct_dirac_bilinear(coefficients) - matrix
).is_zero_matrix
print(
    {
        name: value
        for name, value in coefficients.items()
        if value != 0
    }
)
```

### 介子插值算符

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
print(pion.latex(), rho.latex(), a1.latex())
```

| 算符 | 结构 | 宇称 | C | PyQCD 索引 |
|---|---|---|---|---|
| $\pi$ | `P` | $-1$ | $+1$ | 5 |
| $\rho$（时间分量） | `V4` | $+1$ | $-1$ | 4 |
| $a_1$（时间分量） | `A4` | $-1$ | $-1$ | 15 |

这些只是量子数标签；涂抹、Wilson 线和源共轭属于独立层。

### 导数算符

```python
from myqcd import operators

twist2 = operators.BilinearOperator(
    "O_twist2", "u", "u", "V3", derivatives=1
)
twist3 = operators.BilinearOperator(
    "O_twist3", "u", "u", "V3", derivatives=2
)
assert (twist2.mass_dimension, twist3.mass_dimension) == (4, 5)
print(twist2.mass_dimension, twist3.mass_dimension)
```

例如 $\mathcal{O}_{\mu\nu} = \bar q\,\gamma_\mu D_\nu q$ 的质量量纲为
$4$；两个导数给出量纲 $5$。该类型不建模对称化、无迹化和运动方程约化。

### 显式矩阵恒等式

```python
import sympy as sp

from myqcd import gamma

assert gamma.gamma5() == sp.diag(1, 1, -1, -1)
assert gamma.charge_conjugation_matrix() == gamma.gamma(4) * gamma.gamma(2)
assert (
    gamma.dirac_trace(
        gamma.gamma5()
        * gamma.gamma(1)
        * gamma.gamma(2)
        * gamma.gamma(3)
        * gamma.gamma(4)
    )
    == 4
)
```

## 与标准理论值比对

下表中的数值都是 SymPy 精确结果。“标准值”指四维欧氏空间中惯用的
SU(3)/Dirac 值，不是对某个系综的拟合。

### Dirac 代数

| 恒等式 | MyQCD | 标准值 |
|---|---|---|
| $\mathrm{Tr}[1]$ | $4$ | $4$ |
| $\mathrm{Tr}[\gamma_\mu\gamma_\nu]$ | $4\delta_{\mu\nu}$ | $4\delta_{\mu\nu}$ |
| $\mathrm{Tr}[\gamma_1\gamma_1]$ | $4$ | $4$ |
| $\mathrm{Tr}[\gamma_1\gamma_2]$ | $0$ | $0$ |
| $\mathrm{Tr}[\gamma_1\gamma_2\gamma_3\gamma_4]$ | $0$ | $0$ |
| $\mathrm{Tr}[\gamma_5\gamma_1\gamma_2\gamma_3\gamma_4]$ | $4$ | $4\epsilon_{1234}=4$ |
| $\gamma_5^2$ | $1$ | $1$ |
| $\{\gamma_5,\gamma_\mu\}$ | $0$ | $0$ |
| $C\gamma_\mu C^{-1}$ | $-\gamma_\mu^{T}$ | $-\gamma_\mu^{T}$ |
| $\mathrm{Tr}[\gamma_1\gamma_2\gamma_1\gamma_2]$ | $-4$ | $-4$ |
| $\mathrm{Tr}[\gamma_1\gamma_2\gamma_2\gamma_1]$ | $4$ | $4$ |

### SU(3) 颜色代数

| 量 | MyQCD | 标准值 |
|---|---|---|
| $C_F$ | $4/3$ | $4/3$ |
| $C_A$ | $3$ | $3$ |
| $T_F$ | $1/2$ | $1/2$ |
| $f_{123}$ | $1$ | $1$ |
| $f_{147}$ | $1/2$ | $1/2$ |
| $f_{458}$ | $\sqrt{3}/2$ | $\sqrt{3}/2$ |
| $d_{118}$ | $1/\sqrt{3}$ | $1/\sqrt{3}$ |
| $d_{146}$ | $1/2$ | $1/2$ |
| $\sum f^2$ | $24$ | $24$ |
| $\sum d^2$ | $40/3$ | $40/3$ |
| $\mathrm{Tr}[T^aT^b]$ | $\frac{1}{2}\delta^{ab}$ | $\frac{1}{2}\delta^{ab}$ |

`myqcd.derivations` 中的历史 SU(3) 推导使用反厄米归一化
$-\frac{1}{2}\delta^{ab}$；上表属于厄米的 `myqcd.color` 层，两套约定不可混用。

### 参考约定

- PyQCD DeGrand--Rossi 基：
  `refer/git-rep/PyQCD/pyqcd/lattice/_gamma.py`。
- 标准 SU(3) 迹与 $f/d$ 约定：
  `refer/git-rep/feyncalc/FeynCalc/SUN/SUNTrace.m`（只读参考）。

## 命令

```bash
python -m myqcd.operator_audit
```
