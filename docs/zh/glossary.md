# 术语表

**双线性。** 夸克-反夸克结构 $\bar q\,\Gamma q$，其中 $\Gamma$ 是 16 个
Dirac 矩阵之一。

**Clover。** 四叶 plaquette 对称平均的格点场强
$F_{\mu\nu}=-i/8\sum(P-P^\dagger)$。

**DeGrand–Rossi（DR）基。** PyQCD 使用的 Euclidean gamma 表示：
$\gamma(0)=I$、$\gamma(4)$ 为时间方向、
$\gamma_5=\mathrm{diag}(1,1,-1,-1)$。

**Dirac 结构。** 16 个双线性基中的 $S,P,V_\mu,A_\mu,T_{\mu\nu}$。

**有效质量。** $m_{\mathrm{eff}}(t)=\log[C(t)/C(t+1)]$。

**Epsilon 张量。** 全反对称 $\varepsilon_{\mu\nu\rho\sigma}$，且
$\varepsilon_{0123}=+1$。

**Fierz 变换。** 把
$(\bar\psi_1\Gamma_A\psi_2)(\bar\psi_3\Gamma_B\psi_4)$ 重排为
$(\bar\psi_1\Gamma_C\psi_4)(\bar\psi_3\Gamma_D\psi_2)$ 的和。

**Fermi 符号。** 重排费米子场时的 Grassmann 奇偶性。

**梯度流。** 在流时间 $t$ 对规范链接进行微分涂抹；平滑半径为
$\sqrt{8t}$。

**内部边。** 两个端点都是顶点的图边；外部腿边端点为 $-1$，不计入
$E_{\mathrm{int}}$。

**Jackknife。** leave-one-out 重采样，用于估计均值的协方差。

**圈数。** 对含 $C$ 个连通分量的图，$L=E_{\mathrm{int}}-V+C$。

**混合矩阵。** $\mathcal{O}_i^R=\sum_j Z_{ij}\mathcal{O}_j$ 中的
$Z_{ij}$。

**动量涂抹。** 对夸克源施加规范协变相位，以到达更大的空间动量。

**宇称符号。** $\gamma_4\Gamma\gamma_4=s\Gamma$ 中的 $s$。

**RI/MOM。** 在 $p^2=\mu^2$ 定义的动量减除重正化方案。

**Staple。** 胶子 TMD 算符中使用的三段 Wilson 路径。

**拓扑。** 顶点与边构成的组合图，不依赖粒子标签与动量。

**Twist。** 质量量纲与自旋投影之差；领头 twist 双线性的量纲为
$3+n$（$n$ 个导数）。

**Wick 收缩。** 夸克与反夸克场的配对及相应 Grassmann 符号。

**Wilson 线。** 规范链接的路径排序乘积 $W(x,y)=\prod U_\mu$。

**Z 因子。** 乘在算符或场上的重正化常数。

**对称因子。** 图自同构数的倒数。`myqcd.topology` **不自动**分配它；
必须显式提供粒子内容与顶点交换约定。
