# Fierz 变换

`myqcd.fierz` 在 16 个双线性基上实现通用 Dirac Fierz 重排。取
`myqcd.operators` 中的 $\Gamma_A$，

$$
\left(\bar\psi_1\Gamma_A\psi_2\right)
\left(\bar\psi_3\Gamma_B\psi_4\right)
=
\sum_{C,D}F_{AB}^{CD}
\left(\bar\psi_1\Gamma_C\psi_4\right)
\left(\bar\psi_3\Gamma_D\psi_2\right).
$$

系数通过投影到对偶基 $\Gamma^A=\Gamma_A/g_A$ 精确计算，其中
$g_A=\mathrm{Tr}[\Gamma_A\Gamma_A]/4\in\{+1,-1\}$（Euclidean 基）。
引擎同时用分量矩阵恒等式和随机复旋量验证。

## 标量–标量示例

当 $A=B=S$ 时只有 $C=D$ 项：

| $C=D$ | 系数 |
|---|---|
| `S`、`P`、`V1`–`V4` | $+1/4$ |
| `A1`–`A4`、`T12`–`T34` | $-1/4$ |

符号来自 Euclidean 基，不是任意约定。混合结构（如 $A=S$、$B=V_1$）的
非零伙伴包括 $(C,D)=(S,V_1),(P,A_1),(V_1,S)$ 以及张量/轴矢组合。

## 复现

```python
import sympy as sp

from myqcd import fierz

scalar = fierz.fierz_transform("S", "S")
assert scalar[("S", "S")] == sp.Rational(1, 4)
assert scalar[("A1", "A1")] == -sp.Rational(1, 4)

mixed = fierz.fierz_transform("S", "V1")
assert mixed[("S", "V1")] == sp.Rational(1, 4)
assert mixed[("V1", "S")] == sp.Rational(1, 4)
assert len(mixed) == 16

spinors = [
    [1.0 + 0.5j, 0.0, 0.0, 0.0],
    [0.0, 1.0 - 0.5j, 0.0, 0.0],
    [0.0, 0.0, 1.0 + 0.5j, 0.0],
    [0.0, 0.0, 0.0, 1.0 - 0.5j],
]
assert abs(fierz.fierz_residual("S", "V1", spinors)) < 1e-9
print(len(fierz.common_identities()))
```

## 与标准恒等式比对

| 检查 | 结果 |
|---|---|
| 对偶完备性 $\sum_A\Gamma_A^{ij}\Gamma^{A,kl}=4\delta^{il}\delta^{kj}$ | 精确 |
| 已测试 $(A,B)$ 的矩阵恒等式 | 精确 |
| 随机旋量残差 | $<10^{-9}$ |
| $S$–$S$ 非零项数 | 16 |
| $S$–$V_1$ 非零项数 | 16 |

Fierz 重排的整体符号取决于把 $\psi_2$ 移过 $\bar\psi_3$ 时采用的
Grassmann 约定；本包检查可交换分量的矩阵恒等式，并显式声明约定。
