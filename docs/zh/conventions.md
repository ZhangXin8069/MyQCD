# 约定

## Gamma 矩阵

| 索引 | 含义 |
|---|---|
| `gamma(0)` | 单位矩阵哨兵 |
| `gamma(1..4)` | DR 基中的 x、y、z、t |
| `gamma(5)` | $\gamma_5=\mathrm{diag}(1,1,-1,-1)$ |
| `gamma(6..15)` | PyQCD 使用的乘积 |
| `gamma(16,17)` | $\gamma_3\gamma_1(1\pm\gamma_4)/2$ |

Clifford：$\{\gamma_\mu,\gamma_\nu\}=2\delta_{\mu\nu}$。
电荷共轭：$C=\gamma_4\gamma_2$。

## 颜色

厄米生成元 $T^a=\lambda^a/2$，

$$
\mathrm{Tr}[T^aT^b]=\frac12\delta^{ab},
\qquad
[T^a,T^b]=if^{abc}T^c.
$$

`myqcd.derivations` 中的历史推导使用反厄米归一化
$-\frac12\delta^{ab}$；不要混用两层。

## 度规与 epsilon

Euclidean $\delta_{\mu\nu}$、$\varepsilon_{0123}=+1$、
$\sum\varepsilon^2=24$。

## 算符

$$
\dim(\bar q\Gamma q)=3,\qquad
\dim(\bar q\Gamma D^nq)=3+n.
$$

宇称为 $\gamma_4\Gamma\gamma_4=s\Gamma$；电荷共轭为
$C^{-1}\Gamma C=s\Gamma$。

## 图

$L=E_{\mathrm{int}}-V+C$；外部腿边（端点 $-1$）不计入
$E_{\mathrm{int}}$。

## 格点

动量 $p_\mu=2\pi n_\mu/L_\mu$；色散
$\hat p^2=4a^{-2}\sum\sin^2(p_\mu a/2)$。

## 证据边界

以上都是精确代数约定。圈积分、系综与连续极限属于独立任务。
