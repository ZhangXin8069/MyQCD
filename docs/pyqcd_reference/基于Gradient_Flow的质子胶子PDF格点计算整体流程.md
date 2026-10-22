# 基于 Gradient Flow 的格点 QCD 质子胶子 PDF 计算整体流程

## 1. 目标与文献范围

本文讨论利用 Gradient Flow, 以下简称 GF, 构造质子胶子 quasi-PDF 矩阵元, 再通过小流时间展开, 以下统一写作 SFTX, 转换到 $\overline{\mathrm{MS}}$ 方案, 最后利用大动量有效理论, 即 LaMET, 得到光锥胶子 PDF 的整体流程.

本文采用以下记号:

- $t_{\rm source}$, $t_{\rm insert}$ 和 $t_{\rm sink}$ 表示欧氏时间, 并满足 $t_{\rm source}<t_{\rm insert}<t_{\rm sink}$.
- $\tau\geq 0$ 表示流时间, 量纲为长度平方.
- $a$ 表示格距.
- $z$ 表示沿质子动量方向选取的空间分离.
- $P_z$ 表示质子沿 $z$ 方向的动量.
- $\mu$ 表示 $\overline{\mathrm{MS}}$ 重整化尺度.

需要首先说明文献覆盖范围. 文献[1]给出了 off-lightcone Wilson-line operators 从 GF 方案到 $\overline{\mathrm{MS}}$ 方案的一圈 SFTX matching, 但没有完成质子胶子三点函数的格点数值计算. 文献[2]数值实现了固定流时间取连续极限, SFTX matching 和 $\tau\to0$ 外推, 但研究对象是 pion 的局域夸克 PDF moments, 不是质子的非局域胶子 quasi-PDF. 文献[3]完成了质子非极化胶子 PDF 的二点函数, 三点函数, ratio, 重整化和 LaMET 分析, 但采用 HYP smearing 与 hybrid renormalization, 不是文献[1]的 GF-SFTX 方案. 文献[4]系统总结了 LaMET 的重整化和大动量 factorization. 文献[5]提出以 flowed 局域 twist-2 算符计算任意阶 PDF moments, 并明确给出固定物理流时间取连续极限, 再通过 SFTX 得到 $\overline{\mathrm{MS}}$ 矩阵元的次序. 该文研究的是局域 flavor-nonsinglet 夸克算符, 因而在本文中只作为 GF 连续极限, SFTX 次序和 flow-footprint 条件的方法学依据.

因此, 本文给出的不是某一篇文献已经完整实施的单一计算, 而是由上述文献分别支持的组合流程. 文献没有明确给出的格点离散细节, 极化算符 matching kernel 和数值拟合方案不作具体规定.

整体逻辑为

$$
U_\mu(x)
\xrightarrow{\mathrm{GF}}
V_\mu(x,\tau)
\xrightarrow{\mathrm{2pt/3pt}}
M_g^{\mathrm{lat,GF}}(z,P_z,\tau,a)
\xrightarrow[a\to0]{\tau\ \mathrm{fixed}}
M_g^{R,\mathrm{GF}}(z,P_z,\tau)
\xrightarrow{\mathrm{SFTX}}
M_g^{\overline{\mathrm{MS}},\mathrm{quasi}}(z,P_z,\mu)
\xrightarrow{\mathrm{LaMET}}
g^{\overline{\mathrm{MS}}}(x,\mu).
\tag{1}
$$

式(1)中的两个 matching 分别处理不同问题. SFTX matching 把 GF scheme 的等时空间型算符转换为 $\overline{\mathrm{MS}}$ scheme 的无流 quasi-operator. LaMET matching 再把有限 $P_z$ 的 quasi-PDF 转换为光锥 PDF.

## 2. 从零流时间规范场到流后规范场

### 2.1 连续 Gradient Flow 方程

文献[1]的(3.1)式给出流后规范场 $B_\mu(x,\tau)$ 的演化方程. 将原文流时间 $t$ 改写为本文的 $\tau$, 有

$$
\partial_\tau B_\mu
=
\mathcal D_\nu G_{\nu\mu}
+\kappa\mathcal D_\mu\partial_\nu B_\nu.
\tag{2}
$$

其中 $\kappa$ 是流方程中的规范参数. 文献[1]的(3.4)式和(3.5)式定义

$$
G_{\mu\nu}
=
\partial_\mu B_\nu-\partial_\nu B_\mu+[B_\mu,B_\nu],
\qquad
\mathcal D_\mu
=
\partial_\mu+[B_\mu,\,\cdot\,].
\tag{3}
$$

这里 $\mathcal D_\mu$ 是作用在伴随表示对象上的协变导数. 文献[1]采用把规范耦合吸收到 $B_\mu$ 中的约定, 其(3.6)式给出边界条件

$$
B_\mu(x,0)=gA_\mu(x).
\tag{4}
$$

若采用不把 $g$ 吸收到流场中的约定, 可以改写为 $B_\mu(x,0)=A_\mu(x)$, 同时必须相应修改协变导数和场强中的耦合常数. 两种约定不能混用.

### 2.2 线性化和热核抑制

由文献[1]的(3.1)式至(3.5)式保留 $B_\mu$ 的线性项, 可得

$$
\partial_\tau B_\mu
=
\partial^2B_\mu
+(\kappa-1)\partial_\mu\partial_\nu B_\nu
+O(B^2).
\tag{5}
$$

文献[1]的微扰计算取 $\kappa=1$. 此时线性部分化为热方程

$$
\partial_\tau B_\mu
=
\partial^2B_\mu
+O(B^2).
\tag{6}
$$

在 Fourier 空间中, 式(6)的线性解为

$$
B_\mu(p,\tau)
=
e^{-\tau p^2}B_\mu(p,0)+O(B^2)
=
e^{-\tau p^2}gA_\mu(p)+O(A^2).
\tag{7}
$$

式(7)表明高动量模受到指数抑制. 通常以

$$
r_F=\sqrt{8\tau}
\tag{8}
$$

表示流半径. 该关系解释了为什么固定 $\tau>0$ 的 flowed composite operator 对短距离涨落不再具有普通无流算符的直接敏感性.

### 2.3 格点实现的边界

在格点上实际演化的是规范 links, 可记为 $U_\mu(x)\to V_\mu(x,\tau)$, 并满足 $V_\mu(x,0)=U_\mu(x)$. 文献[1]主要进行连续微扰分析, 没有规定质子胶子 quasi-PDF 数值计算必须使用哪一种格点 flow action, 场强离散或积分器. 因此本文不指定 Wilson flow, Symanzik flow, Zeuthen flow, clover field strength 或其他离散细节. 这些选择需要在具体数值方案中单独给出, 并进行连续极限检验.

## 3. 流后胶子 Wilson-line operator

### 3.1 文献[1]的通用胶子算符

文献[1]的(1.2)式定义无流的 off-lightcone 胶子 Wilson-line operator

$$
O_g^{\mu\nu\alpha\beta}(zv)
=
g^2F_a^{\mu\nu}(zv)
W_{\rm adj}^{ab}(zv,0)
F_b^{\alpha\beta}(0),
\tag{9}
$$

其中 $v^\mu$ 指定 Wilson line 方向, $W_{\rm adj}^{ab}$ 是伴随表示 Wilson line. 在文献[1]采用的 $B_\mu(x,0)=gA_\mu(x)$ 约定和 Hermitian generators convention 下, 流后 Wilson line 可以写成

$$
W_{\rm adj}(zv,0;\tau)
=
\mathcal P\exp\left[
 i\int_0^z ds\,v_\mu B_\mu^a(sv,\tau)T_{\rm adj}^a
\right]_{\rm adj}.
\tag{10}
$$

若采用 anti-Hermitian generators convention, 式(10)中的 $i$ 被吸收到 Lie-algebra-valued connection 中. 由同一流时间的流后场强和 Wilson line 构造

$$
O_g^{\mu\nu\alpha\beta}(zv,\tau)
=
G_a^{\mu\nu}(zv,\tau)
W_{\rm adj}^{ab}(zv,0;\tau)
G_b^{\alpha\beta}(0,\tau).
\tag{11}
$$

在其他规范场归一化约定中, 式(10)和式(11)需要恢复相应的 $g$ 因子. 算符两端的场强和中间 Wilson line 必须使用同一个流时间 $\tau$.

### 3.2 非极化与极化算符的范围

非极化胶子 quasi-PDF 使用 $GG$ 型 Lorentz 投影. 沿 $z$ 方向取 Wilson line 时, 其示意结构可写为

$$
O_g^{\rm unpol}(z,\tau)
\sim
G_a^{zi}(z\hat z,\tau)
W_{\rm adj}^{ab}(z\hat z,0;\tau)
G_b^{zi}(0,\tau),
\tag{12}
$$

其中 $i$ 是与 $z$ 不同的指标. 实际计算可以采用其他 multiplicatively renormalizable 的 Lorentz 组合. 文献[3]给出了一个具体的无流非极化胶子算符组合, 但该组合所属的 HYP-smearing 与 hybrid-renormalization 流程不能直接等同于本文的 GF-SFTX 方案.

对偶场强定义为

$$
\widetilde G^{\mu\nu}
=
\frac{1}{2}\epsilon^{\mu\nu\rho\sigma}G_{\rho\sigma}.
\tag{13}
$$

胶子 helicity quasi-operator 的示意结构为

$$
O_{\Delta g}(z,\tau)
\sim
G_a^{z\mu}(z\hat z,\tau)
W_{\rm adj}^{ab}(z\hat z,0;\tau)
\widetilde G_{b,\mu}^{z}(0,\tau).
\tag{14}
$$

式(12)和式(14)只用于说明非极化分布对应 $GWG$, helicity 分布对应 $GW\widetilde G$. 文献[1]没有给出一套完整的 Euclidean helicity quasi-PDF 格点算符, SFTX matching 和 LaMET kernel 的联合数值方案. 因此, 极化胶子 PDF 的 Euclidean $i$ 因子, 指标组合, mixing 和 matching 系数必须由专门文献另行核对, 不能直接把非极化结果替换一个场强后使用.

## 4. 质子二点函数和含 flowed gluon insertion 的三点函数

### 4.1 二点函数

设 $\mathcal N$ 是具有质子量子数的普通零流时间插值场. 质子二点函数可写为

$$
C_2(P_z;t_{\rm sink},t_{\rm source})
=
\sum_{\mathbf x}
e^{-i\mathbf P\cdot(\mathbf x-\mathbf x_{\rm source})}
\left\langle
0\left|
\mathcal N(\mathbf x,t_{\rm sink})
\overline{\mathcal N}(\mathbf x_{\rm source},t_{\rm source})
\right|0
\right\rangle.
\tag{15}
$$

文献[3]的(16)式和(17)式给出了实际质子二点函数及其插值场. 该论文没有采用 GF-SFTX, 但其质子二点函数和谱提取结构可以作为非局域胶子插入计算的直接参考.

### 4.2 三点函数

将 flowed gluon operator 插入欧氏时间 $t_{\rm insert}$, 得到

$$
C_{3,g}
\left(
P_z,z,\tau;
t_{\rm sink},t_{\rm insert},t_{\rm source}
\right)
=
\left\langle
0\left|
\mathcal N(P_z,t_{\rm sink})
O_g(z,\tau,t_{\rm insert})
\overline{\mathcal N}(P_z,t_{\rm source})
\right|0
\right\rangle.
\tag{16}
$$

纯胶子算符相对于质子夸克传播线是 disconnected insertion. 文献[3]的(19)式明确使用真空减除后的胶子算符与质子二点函数的协方差结构, 可概括为

$$
C_{3,g}
\propto
\left\langle
\left(O_g-\langle O_g\rangle\right)
\left(C_2-\langle C_2\rangle\right)
\right\rangle.
\tag{17}
$$

式(17)说明纯胶子 insertion 不需要在某条 valence-quark propagator 上插入一个胶子顶角. 它通过规范组态平均与质子二点函数相关联.

### 4.3 外态与流时间无关

二点函数的谱分解为

$$
C_2(P_z;T)
=
\sum_n
|Z_n(P_z)|^2e^{-E_n(P_z)T},
\qquad
T=t_{\rm sink}-t_{\rm source}.
\tag{18}
$$

三点函数的谱分解为

$$
C_{3,g}
=
\sum_{m,n}
Z_m(P_z)Z_n^*(P_z)
e^{-E_m(t_{\rm sink}-t_{\rm insert})}
e^{-E_n(t_{\rm insert}-t_{\rm source})}
\langle m,P_z|O_g(z,\tau)|n,P_z\rangle.
\tag{19}
$$

文献[2]的(A3)式对含 flowed insertion 的三点函数给出了同样的谱结构. 其外态写成普通哈密顿量本征态, 不带流时间标签. 流时间只出现在插入算符中. 对质子计算, 目标矩阵元应写为 $\langle P(P_z,S)|O_g(z,\tau)|P(P_z,S)\rangle$, 而不是 $|P(P_z,\tau)\rangle$.

文献[2]还明确要求 flow footprint 与源, 汇的欧氏时间间隔充分分离. 文献[5]在其三点函数操作流程中也要求 hadron interpolator 与 flowed operator 的物理距离远大于流半径:

$$
\sqrt{8\tau}
\ll
t_{\rm insert}-t_{\rm source},
\qquad
\sqrt{8\tau}
\ll
t_{\rm sink}-t_{\rm insert}.
\tag{20}
$$

式(20)是文献[2]对局域 flowed operator 的明确条件. 将其用于非局域质子胶子算符时, 还需要确保该算符在空间方向的 flow footprint 与所选 $z$ 相容.

### 4.4 Ratio 和基态矩阵元

通过三点函数与二点函数的 ratio, 或通过二点函数和三点函数的联合多态拟合, 在大欧氏时间分离下提取基态矩阵元. 一般可写为

$$
R_g
=
\frac{C_{3,g}}{C_2}
\xrightarrow[
t_{\rm sink}-t_{\rm insert}\to\infty
]{
t_{\rm insert}-t_{\rm source}\to\infty
}
\mathcal M_g^{\rm lat,GF}(z,P_z,\tau,a),
\tag{21}
$$

## 5. 固定流时间下的连续极限与 GF 方案

### 5.1 Ratio 提取的 flowed 格点矩阵元

将 ratio 或谱拟合得到的有限格距结果记为

$$
M_g^{\rm lat,GF}(z,P_z,\tau,a)
=
\langle P(P_z)|O_g^{\rm lat,GF}(z,\tau,a)|P(P_z)\rangle.
\tag{22}
$$

式(22)是有限格距下由 ratio 或谱拟合提取的 flowed 格点矩阵元. 该阶段完成外态 overlap, 欧氏传播因子和激发态效应的处理, 并保留 $a$ 和 $\tau$ 依赖.

### 5.2 固定正流时间下的连续 GF 矩阵元

GF 以正流时间作为短距离调节尺度. 在底层 QCD 参数已经重整化的条件下, 由 flowed gauge fields 构成的纯胶子算符在固定物理 $\tau>0$ 时具有有限连续极限, 这是文献[1]建立 GF matching scheme 的基础. 文献[2]和文献[5]针对局域 flowed twist-2 算符进一步明确采用了固定物理流时间取连续极限的次序. 因此, 对式(22)在多个格距上保持同一物理 $\tau$, 并定义

$$
M_g^{R,\rm GF}(z,P_z,\tau)
=
\lim_{a\to0}
M_g^{\rm lat,GF}(z,P_z,\tau,a),
\qquad
\tau>0\ \mathrm{fixed}.
\tag{23}
$$

式(23)中的上标 $R$ 表示底层 QCD 已完成参数重整化, 且该 flowed 矩阵元已经取连续极限. 对本文的纯胶子 insertion, 算符内部只含 flowed gauge fields 和伴随 Wilson line, 因而这一阶段不另设普通无流格点算符的独立重整化因子 $Z_{O_g}(a)$. 若算符含有 flowed fermion fields, 则还需要与 SFTX coefficient 定义一致的 flowed-fermion renormalization; 文献[5]的(6)式至(9)式使用 ringed fields 处理这一点.

$M_g^{R,\rm GF}(z,P_z,\tau)$ 仍属于 GF scheme 并依赖 $\tau$. 下一阶段通过包含 Wilson-line 质量修正和端点系数的 SFTX, 将其转换为无流的 $\overline{\mathrm{MS}}$ quasi 矩阵元.

## 6. SFTX 和第一次 matching

### 6.1 局域 current 的 SFTX

文献[1]的(3.13)式给出 renormalized flowed current 与 $\overline{\mathrm{MS}}$ renormalized unflowed current 之间的 SFTX:

$$
O^{R,\rm GF}(\tau)
=
c_O(\tau,\mu)
O^{\overline{\rm MS}}(\mu)
+O(\tau).
\tag{24}
$$

式(24)连接有限的 GF-scheme flowed operator 与 $\overline{\mathrm{MS}}$ renormalized unflowed operator, 其中 $c_O$ 是两个方案之间的 matching coefficient. 文献[5]的(11)式对 ringed 局域 twist-2 算符给出了相同结构, 其(16)式通过 $c_n^{-1}$ 得到 $\overline{\mathrm{MS}}$ 矩阵元. 文献[1]的式(3.13)忽略了 operator mixing; 若具体算符存在 mixing, $c_O$ 应推广为矩阵并进行矩阵求逆.

### 6.2 Wilson line 的质量修正

文献[1]的(4.15)式给出一圈质量修正. 对胶子算符的伴随表示 Wilson line, $C_R=C_A$, 因而

$$
\delta m_A(\tau)
=
-\frac{\alpha_s(\mu)C_A}{4\pi}
\frac{\sqrt{2\pi}}{\sqrt{\tau}}
+O(\alpha_s^2).
\tag{25}
$$

该量在固定 $\tau>0$ 时有限, 但在 $\tau\to0$ 时具有 $1/\sqrt{\tau}$ 奇异性. 文献[1]将其指数化并写入完整 Wilson-line operator 的 matching 关系. 其他文献可能采用相反符号定义正的质量 counterterm, 因而指数符号必须与 $\delta m$ 的定义成套使用.

### 6.3 完整胶子 Wilson-line operator 的 SFTX

相对于 Wilson line 方向 $v^\mu$, 文献[1]把场强分为 $\parallel\perp$ 和 $\perp\perp$ 两类. 其(4.69)式和(4.70)式给出

$$
O_{\parallel\perp}^{R,\rm GF}(zv,\tau)
=
C_{\parallel\perp}(\tau,\mu)
e^{\delta m_A(\tau)z}
O_{\parallel\perp}^{\overline{\rm MS}}(zv,\mu)
+O(\tau),
\tag{26}
$$

$$
O_{\perp\perp}^{R,\rm GF}(zv,\tau)
=
C_{\perp\perp}(\tau,\mu)
e^{\delta m_A(\tau)z}
O_{\perp\perp}^{\overline{\rm MS}}(zv,\mu)
+O(\tau).
\tag{27}
$$

文献[1]取 $z>0$. 对允许正负分离的格点数据, 应将指数写成依赖 Wilson line 物理长度 $|z|$ 的形式. 两个 endpoint current 分别贡献一个局域 matching coefficient, 因而文献[1]的(4.72)式和(4.73)式为

$$
C_{\parallel\perp}(\tau,\mu)
=
c_{\parallel\perp}^2(\tau,\mu),
\qquad
C_{\perp\perp}(\tau,\mu)
=
c_{\perp\perp}^2(\tau,\mu).
\tag{28}
$$

一圈结果由文献[1]的(4.65)式和(4.66)式给出:

$$
c_{\parallel\perp}(\tau,\mu)
=
1+O(\alpha_s^2),
\tag{29}
$$

$$
c_{\perp\perp}(\tau,\mu)
=
1+
\frac{\alpha_s(\mu)C_A}{4\pi}
\ln\left(2\mu^2\tau e^{\gamma_E}\right)
+O(\alpha_s^2).
\tag{30}
$$

保持一圈精度, 完整双端点算符的系数为

$$
C_{\parallel\perp}(\tau,\mu)
=
1+O(\alpha_s^2),
\tag{31}
$$

$$
C_{\perp\perp}(\tau,\mu)
=
1+
\frac{\alpha_s(\mu)C_A}{2\pi}
\ln\left(2\mu^2\tau e^{\gamma_E}\right)
+O(\alpha_s^2).
\tag{32}
$$

这些系数只适用于文献[1]明确分析的 tensor projections. 对式(14)一类 helicity operator, 两个 endpoint 可能属于不同投影. 文献[1]没有把相应的 polarized-gluon SFTX matching 作为完整 quasi-PDF 公式列出, 因而本文不提供可直接用于数值计算的 helicity matching coefficient.

### 6.4 从 GF 矩阵元反解 $\overline{\mathrm{MS}}$ quasi 矩阵元

对文献[1]明确处理的投影 $i\in\{\parallel\perp,\perp\perp\}$, 在忽略 mixing 的条件下, 对质子矩阵元反解式(26)或式(27)可得

$$
M_{g,i}^{\overline{\rm MS},\rm quasi}(z,P_z,\mu)
=
e^{-\delta m_A(\tau)|z|}
C_{g,i}^{-1}(\tau,\mu)
M_{g,i}^{R,\rm GF}(z,P_z,\tau)
+O(\tau).
\tag{33}
$$

这里 $C_{g,i}$ 表示对应 tensor projection 的完整双端点系数. 文献[1]说明这些 Wilson-line matching coefficients 与外部态及 $z$ 无关, $z$ 依赖仅通过线性质量修正的指数和原算符矩阵元出现.

定义有限 $a$ 和有限 $\tau$ 下的匹配估计量

$$
\widehat M_{g,i}^{\overline{\rm MS}}
(z,P_z,\mu;\tau,a)
=
e^{-\delta m_A(\tau)|z|}
C_{g,i}^{-1}(\tau,\mu)
M_{g,i}^{\rm lat,GF}(z,P_z,\tau,a).
\tag{34}
$$

GF-SFTX 方案要求先在固定物理 $\tau$ 下处理连续极限, 再分析匹配后结果的流时间依赖. 理想的全阶关系为

$$
M_{g,i}^{\overline{\rm MS},\rm quasi}(z,P_z,\mu)
=
\lim_{\tau\to0}
\left[
e^{-\delta m_A(\tau)|z|}
C_{g,i}^{-1}(\tau,\mu)
\lim_{a\to0}
M_{g,i}^{\rm lat,GF}(z,P_z,\tau,a)
\right].
\tag{35}
$$

文献[2]的数值策略是: 在固定物理流时间取连续极限, 进行 matching, 再检查匹配后结果的残余流时间依赖, 必要时外推到零流时间. 该顺序在文献[2]中针对局域 pion PDF moments 得到实际验证. 文献[5]的(16)式也明确采用固定流时间连续极限后的矩阵元 $A_n(\tau)$, 再乘 $c_n^{-1}(\tau,\mu)$ 得到 $\overline{\mathrm{MS}}$ 矩阵元. 将这一顺序用于非局域质子胶子 operator 时, Wilson-line 的专门 SFTX 系数来自文献[1]; 当前所引文献尚未给出这一组合流程的完整格点数值结果.

## 7. 流时间窗口和连续极限

综合文献[1]与文献[2]中明确出现的层级, 可使用以下条件组织数据选择:

$$
a
\ll
\sqrt{8\tau}
\ll
\min\left(
|z|,
t_{\rm insert}-t_{\rm source},
t_{\rm sink}-t_{\rm insert}
\right).
\tag{36}
$$

式(36)不是文献中针对质子非局域胶子 quasi-PDF 给出的单一已证明窗口. 其左侧层级来自固定物理流时间取连续极限的要求和文献[2]讨论的 $a^2/\tau$ enhanced cutoff effects. 两个欧氏时间层级来自文献[2]的(A3)式及其相邻讨论, 文献[5]也明确要求 hadron interpolator 与 flowed operator 的物理距离远大于 $\sqrt{8\tau}$. $\sqrt{8\tau}\ll|z|$ 来自文献[1]附录中对 quark quasi-PDF 一圈有限流时间效应的分析, 文献[1]只在零外部动量的夸克例子中明确验证了该判断, 因而不能把它当成质子胶子 operator 的已完成数值误差估计.

对实际数据, 应在多个 $a$ 和多个 $\tau$ 上检查匹配后结果. 文献[2]表明 flowed ratios 的 cutoff effects 可以包含 $a^2/\tau$ enhanced 项, 而 SFTX 自身包含高维算符贡献. 对非局域胶子 operator, 可将以下形式作为诊断而不是已经由所引文献完整推导的误差公式:

$$
\widehat M_g^{\overline{\rm MS}}(\tau,a)
=
M_g^{\overline{\rm MS},\rm quasi}
+O\left(\frac{a^2}{\tau}\right)
+O(\tau)
+O(\alpha_s^{N+1}).
\tag{37}
$$

其中 $N$ 是 SFTX matching coefficient 已知的最高微扰阶数. 文献[1]给出的 off-lightcone Wilson-line matching 为一圈结果. 因此, 匹配后的残余 $\tau$ 依赖既可能来自 SFTX 的高维算符, 也可能来自微扰截断和有限格距效应. 不能仅使用最小的一个 $\tau$ 数据点来代替窗口和外推分析.

## 8. 从 $\overline{\mathrm{MS}}$ quasi 矩阵元到 quasi-PDF

得到 $M_g^{\overline{\rm MS},\rm quasi}(z,P_z,\mu)$ 后, 可以按照文献[3]的(14)式所示结构进行 Fourier 变换:

$$
\widetilde g(x,P_z,\mu)
=
\mathcal N_g(P_z)
\int_{-\infty}^{+\infty}
\frac{dz}{2\pi}
e^{-ixP_zz}
M_g^{\overline{\rm MS},\rm quasi}(z,P_z,\mu).
\tag{38}
$$

$\mathcal N_g(P_z)$ 取决于具体胶子 operator 和运动学归一化. 文献[3]还对有限 $z$ 数据进行大 Ioffe-time 外推, 但该外推 ansatz 属于其具体分析选择, 不是 GF-SFTX 框架本身的必然组成. 因此本文只保留 Fourier 变换的结构, 不规定大 $|z|$ 外推模型.

也可以在坐标空间直接进行短距离 factorization. 文献[4]讨论了 momentum-space LaMET 和 coordinate-space factorization 的等价极限, 但有限格点数据下两种分析路线具有不同的数值系统误差.

## 9. 第二次 matching: LaMET 到光锥 PDF

SFTX 后得到的对象仍然是有限 $P_z$ 的空间型等时 quasi-PDF, 不是光锥 PDF. 文献[4]的(33)式给出 quasi-PDF 与 light-cone PDF 之间的大动量 factorization. 对胶子和 flavor-singlet quark sector, 文献[4]的(77)式和(78)式说明必须允许 quark-gluon mixing. 可概括为

$$
\begin{pmatrix}
\Sigma^{\overline{\rm MS}}(x,\mu)\\
g^{\overline{\rm MS}}(x,\mu)
\end{pmatrix}
=
\mathbf C^{\rm LaMET}
\left(\frac{\mu}{P_z}\right)
\otimes
\begin{pmatrix}
\widetilde\Sigma^{\overline{\rm MS}}(x,P_z,\mu)\\
\widetilde g^{\overline{\rm MS}}(x,P_z,\mu)
\end{pmatrix}
+\mathrm{power\ corrections}.
\tag{39}
$$

其中 $\Sigma=\sum_f(q_f+\bar q_f)$ 是 flavor-singlet quark PDF, $\otimes$ 表示动量分数卷积. $\mathbf C^{\rm LaMET}$ 的方向取决于采用"quasi 表示 light-cone"还是"light-cone 表示 quasi"的 convention, 使用时必须与所引用 kernel 的定义一致.

文献[4]的(33)式表明, 中等 $x$ 区间的典型大动量修正具有

$$
O\left(
\frac{\Lambda_{\rm QCD}^2}{(xP_z)^2},
\frac{\Lambda_{\rm QCD}^2}{[(1-x)P_z]^2}
\right)
\tag{40}
$$

的结构. 因此需要多个较大 $P_z$ 来检查有限动量效应. 文献[3]实际进行了质子非极化胶子 PDF 的有限动量和连续极限分析, 但其输入是 hybrid-renormalized 无流 quasi matrix elements. 该论文的数值外推形式不能未经验证地直接视为 GF-SFTX 方案的唯一选择.

对于非极化胶子 PDF, 式(39)中的 $g$ 与 $\Sigma$ 使用非极化 matching matrix. 对 helicity PDF, 必须改用 $\Delta g$ 和 $\Delta\Sigma$ 以及相应 polarized matching matrix. 文献[1]没有给出从 flowed helicity gluon Wilson-line operator 一直到 light-cone $\Delta g$ 的完整两阶段 kernel, 因而不能使用式(29)至式(32)之外的未核实替换规则.

## 10. 文献支持下的操作顺序

以下顺序总结了文献明确支持的部分及其边界.

1. 从零流时间规范 links $U_\mu(x)$ 出发, 按选定的格点 Gradient Flow 离散得到 $V_\mu(x,\tau)$. 连续极限所对应的流方程由式(2)至式(4)给出. 具体格点 flow action 和积分器需要另行规定.

2. 在同一流时间 $\tau$ 上构造流后场强和伴随 Wilson line, 得到式(11)的 $O_g(z,\tau)$. 非极化 operator 的具体 Lorentz 组合必须选定并与 matching projection 对应.

3. 使用普通零流时间质子 source 和 sink 计算式(15)和式(16)的二点函数与三点函数. 外部质子态不进行流时间演化. 纯胶子 insertion 采用类似式(17)的 vacuum-subtracted disconnected correlation.

4. 使用 ratio 或多态谱拟合提取式(22)的有限格距 flowed 矩阵元. Ratio 用于消除外态 overlap 和欧氏传播因子, 并通过时间分离或多态拟合控制激发态污染.

5. 在底层 QCD 参数已重整化的前提下, 保持物理 $\tau>0$ 固定, 对多个格距按式(23)取连续极限. 对纯胶子 flowed insertion, 该 GF 路线在此阶段不引入普通无流算符的独立 $Z_{O_g}(a)$; 若算符含 flowed fermion fields, 则按所采用的 SFTX convention 完成相应 flowed-fermion renormalization.

6. 对连续 GF matrix element 使用文献[1]的 SFTX. 对其明确处理的 tensor projections, 使用式(25)的 $\delta m_A$ 和式(31)或式(32)的 $C_g$, 按式(33)转换到 $\overline{\mathrm{MS}}$ quasi matrix element.

7. 使用多个 $\tau$ 检查 SFTX 后结果的流时间稳定性. 参考文献[2]的实际数值策略, 在必要时对匹配后的连续结果作 $\tau\to0$ 外推. 对非局域质子胶子 operator 的具体 fit ansatz 需要由数据和进一步文献确定.

8. 根据式(38)构造 quasi-PDF, 或采用坐标空间 factorization. 有限 $z$ 区间和 Fourier inversion 的处理属于独立数值系统误差.

9. 在与输入 quasi matrix element 相同的 $\overline{\mathrm{MS}}$ convention 下使用 LaMET kernel, 并按照式(39)考虑 gluon-singlet mixing, 得到光锥 $g^{\overline{\rm MS}}(x,\mu)$. 极化分布必须使用独立核对的 polarized operator 和 matching matrix.

整个方案可以最终概括为

$$
\boxed{
\text{flowed 3pt/2pt}
\xrightarrow[
\tau\ \mathrm{fixed}
]{a\to0}
\text{GF-scheme matrix element}
\xrightarrow{\mathrm{SFTX}}
\overline{\mathrm{MS}}\text{ quasi matrix element}
\xrightarrow{\mathrm{LaMET}}
\overline{\mathrm{MS}}\text{ light-cone PDF}
}.
\tag{41}
$$

## 11. 关键术语的严格区分

| 对象 | 主要依赖 | 是否需要额外说明 |
|---|---|---|
| $M_g^{\rm lat,GF}(z,P_z,\tau,a)$ | $a$, $\tau$, $z$, $P_z$ | ratio 或谱拟合提取的有限格距 flowed 矩阵元 |
| $M_g^{R,\rm GF}(z,P_z,\tau)$ | $\tau$, $z$, $P_z$ | 固定物理 $\tau$ 的连续 GF-scheme 矩阵元 |
| $M_g^{\overline{\rm MS},\rm quasi}(z,P_z,\mu)$ | $z$, $P_z$, $\mu$ | 经 SFTX 转换后的无流 quasi 矩阵元 |
| $\widetilde g(x,P_z,\mu)$ | $x$, $P_z$, $\mu$ | 有限动量 quasi-PDF |
| $g^{\overline{\rm MS}}(x,\mu)$ | $x$, $\mu$ | 经 LaMET matching 得到的光锥 PDF |

固定正流时间下的连续 GF 矩阵元依赖 $\tau$, 正如 $\overline{\mathrm{MS}}$ renormalized quantity 依赖 $\mu$. $\tau$ 在 GF scheme 中承担短距离尺度的作用. 未匹配的 GF Wilson-line operator 在 $\tau\to0$ 时一般没有有限非零极限; 式(35)中的 matched combination 在全阶和受控极限下趋向有限的 $\overline{\mathrm{MS}}$ quasi matrix element.

## 12. 结论与限制

质子胶子 PDF 的 GF-SFTX-LaMET 流程包含两个不同 matching. 第一次 matching 使用 SFTX, 将固定正流时间下连续且有限的 GF-scheme Wilson-line matrix element 转换为 $\overline{\mathrm{MS}}$ quasi matrix element. 第二次 matching 使用 LaMET, 将有限动量 quasi-PDF 转换为 light-cone PDF, 并在胶子 sector 中处理 flavor-singlet mixing.

对纯胶子 flowed operator, 3pt/2pt ratio 或谱拟合首先给出有限格距 flowed 矩阵元. 在固定物理 $\tau>0$ 下取连续极限后得到 GF-scheme 矩阵元, 随后使用包含 $\delta m_A$ 和 $C_g$ 的 SFTX matching 得到 $\overline{\mathrm{MS}}$ quasi 矩阵元. 这一 GF 路线在连续极限之前不另设普通无流算符的独立 $Z_{O_g}(a)$.

当前引用文献没有单独完成"质子非局域胶子算符的 GF 演化, flowed 3pt/2pt, Brambilla-Wang SFTX, $\overline{\mathrm{MS}}$ quasi-PDF, 含 mixing 的 LaMET"这一完整数值链. 因此, 具体格点 flow action, 非极化 operator 最优组合, helicity operator 的 Euclidean 定义, polarized SFTX coefficients, quark-gluon mixing kernel 和联合外推形式仍需要针对最终计算方案逐项补充文献依据.

## 13. Reference

[1] Nora Brambilla and Xiang-Peng Wang, *Off-lightcone Wilson-line operators in gradient flow*, [arXiv: 2312.05032]

[2] Anthony Francis et al., *Gradient Flow for Parton Distribution Functions: First Application to the Pion*, [arXiv: 2509.02472]

[3] Chen Chen et al., *Unpolarized gluon PDF of the nucleon from lattice QCD in the continuum limit*, [arXiv: 2510.26425]

[4] Xiangdong Ji et al., *Large-Momentum Effective Theory*, [arXiv: 2004.03543]

[5] Andrea Shindler, *Moments of parton distribution functions of any order from lattice QCD*, [arXiv: 2311.18704]
