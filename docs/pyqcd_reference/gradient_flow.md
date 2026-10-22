# Gradient-flow quark/gluon PDF 项目交接文档

生成日期：2026-09-08  
本次会话标题：Gradient-flow quark/gluon PDF 全链路状态、约定与继续工作清单

---

## 10. 2026-09-11 增补：当前 gluon quasi matching 结果与操作顺序

本节覆盖并更新前文关于 gluon matching 的状态；如果旧段落与本节冲突，
以本节和对应产物的 `manifest.json` 为准。

### 10.1 当前理论链

当前计算必须区分三个层次：

1. 有限流时间的 lattice OPE/C3/C2 矩阵元；
2. gradient-flow scheme 到 MSbar quasi（或同一 scheme 的 ratio/hybrid）转换；
3. quasi-to-light-cone 的 LaMET/pseudo-ITD matching。

推荐的两步链为

```text
h_GF(z,Pz,tau)
  -> GF scheme conversion
  -> h_R(z,Pz,tau)
  -> small-flow-time extrapolation tau -> 0
  -> lambda=z Pz interpolation/tail treatment
  -> Fourier transform
  -> x*g_quasi(x,Pz)
  -> gluon LaMET kernel (and singlet mixing)
  -> x*g(x,mu)
```

这里的 lambda 处理不是物理的 `lambda -> infinity` 极限。它可以表示
有限数据的 lambda 插值、最大 |lambda| 以外的尾部模型，或 pseudo-ITD 中
固定 lambda 的 zeta^2=z^2 外推；三者必须在元数据中明确区分。

对 arXiv:2510.26425v2 的 x-space gluon kernel，当前推荐先完成坐标空间的
flow conversion、tau 外推和有限 lambda 重构，再 Fourier 变换，最后应用
quasi-to-light-cone kernel。坐标空间 kernel 只有在同一 scheme、同一 Fourier
约定下才可以放到 Fourier 之前。有限 zmax、插值、尾部模型和逐 replica
归一化存在时，两条数值路线不能默认等价。

当前 even unpolarized 的 Fourier 约定为

```text
x g_quasi_tilde(x,Pz) = Pz/pi * integral_0^infinity dz
                           cos(x Pz z) h_R(z,Pz)
```

helicity 的 odd channel 使用对应的 sine transform。缺失的短距离 z 点必须
保持 mask/NaN，不能用零填补后 Fourier 或拟合。

### 10.2 当前 N406 flow-time 外推输入

输入产物：

```text
/public/group/lqcd/donghx/Gradient_Flow_GluonPDF/matching/bare_all_operators_matching_v1/flow_extrap_tau_ge1/matched_small_flow_extrap_tau_ge1.npz
```

其 manifest 明确记录：

- Nconf = 406；
- Nboot = 1000；
- a = 0.0775 fm；
- tau/a^2 = 1.0, 1.4, 1.8, 2.2, 2.6, 3.0, 3.4, 3.8；
- 小流时间模型为 `M(tau)=M0+c*tau`，采用 replica-level AIC 权重；
- 当前 operator labels 同时包含 unpolarized 的 `TU_even`、`TU+SU_even`、
  `TU-SU_even` 和 helicity 的 `TH_odd`、`TH+SH_odd`、`TH-SH_odd`；
- Pz integer = 3,4,5，z/a = 0,...,24。

外推结果和拟合图：

```text
/public/group/lqcd/donghx/Gradient_Flow_GluonPDF/matching/bare_all_operators_matching_v1/flow_extrap_tau_ge1/
```

### 10.3 quasi matching 脚本和实际产物

实现入口：

```text
/public/group/lqcd/donghx/Gradient_Flow_GluonPDF/matching/match_unpolarized_quasi_from_extrap_v2.py
```

该脚本：

- 使用 arXiv:2510.26425v2 的 gluon `C_ratio`/`C_hybrid` kernel；
- 对每个 bootstrap replica 独立做 Fourier 和一圈 inverse matching；
- 暂时关闭 quark--gluon singlet mixing；
- 使用有限 z/a=0,...,24 的 cosine transform；
- 不对缺失 z 点做零填充；
- 保存 `quasi_boot`、`matched_boot`、scheme correction、Lamet correction、
  bootstrap indices、数值敏感性检查和完整 manifest。

hybrid 结果：

```text
/public/group/lqcd/donghx/Gradient_Flow_GluonPDF/matching/bare_all_operators_matching_v1/quasi_matching_tau_ge1_v2/
```

ratio 结果：

```text
/public/group/lqcd/donghx/Gradient_Flow_GluonPDF/matching/bare_all_operators_matching_v1/quasi_matching_tau_ge1_v2_ratio/
```

主要图：

```text
.../quasi_matching_tau_ge1_v2/unpolarized_before_after_all_Pz.pdf
.../quasi_matching_tau_ge1_v2/unpolarized_zmax_sensitivity.pdf
.../quasi_matching_tau_ge1_v2_ratio/unpolarized_before_after_all_Pz.pdf
.../quasi_matching_tau_ge1_v2_ratio/unpolarized_zmax_sensitivity.pdf
```

运行命令：

```bash
cd /public/group/lqcd/donghx/Gradient_Flow_GluonPDF
python3 -m py_compile matching/match_unpolarized_quasi_from_extrap_v2.py
MPLCONFIGDIR=/tmp/mpl-gf python3 matching/match_unpolarized_quasi_from_extrap_v2.py
MPLCONFIGDIR=/tmp/mpl-gf python3 matching/match_unpolarized_quasi_from_extrap_v2.py \
  --scheme ratio \
  --out matching/bare_all_operators_matching_v1/quasi_matching_tau_ge1_v2_ratio
```

### 10.4 已确认的结果状态

- Pz=3 的 z/a = 0,1,3,5,6,7,8,9,10,11,12,13 外推点缺失，因此被记录为
  `not_computed_missing_input`，没有输出伪造的 quasi 结果；
- Pz=4 和 Pz=5 均完成 1000 个 bootstrap replica；
- Pz=5 的局域 z=0 归一化分母有 1 个 bootstrap replica 符号翻转，manifest
  已标记 `heavy_tail_risk_sign_crossing`；
- quadrature order、xi_max、输入网格和 quasi support 的扫描均已保存；
- hybrid 与 ratio 的结果都只是 exploratory NLO matched quasi diagnostic；
- 当前输出不是最终 gluon PDF。

### 10.5 不能随意修改的理论约定

1. Wilson line 沿空间 z 方向时，unpolarized 的 `Mtiti` 和 `Mijij` 都属于
   `perp-perp` endpoint sector，因此当前 GF conversion 使用共同的
   `C_perp-perp^{-1}`，再组合 `TU-SU`；不能把 temporal/spatial 标签直接
   当作 parallel/perpendicular 标签。
2. helicity 的 dual tensor 交换两个 endpoint sector；`TH` 和 `SH` 在候选
   endpoint-factorized one-loop conversion 中使用共同的
   `C_Delta_g = c_parallel-perp*c_perp-perp`，physical operator 仍是
   `(TH-SH)_odd`。`TH+SH` 和 `TH` 只能作为 diagnostics。
3. line-mass 约定为
   `delta_m = - alpha_s*C_A/(4*pi) * sqrt(2*pi/t_GeV_minus2)`，其中 t 必须
   先从 tau/a^2 转换为 GeV^-2；不能使用 `2*pi/sqrt(t)` 的旧系数。
4. 若 nonperturbative ratio/hybrid subtraction 已经包含 line mass，不能再
   乘一次 perturbative `exp(-delta_m*|z|)`。
5. 当前 `kappa_F=1` 和 helicity endpoint-factorized coefficient 是诊断/候选
   约定，不等于已经完成独立的完整 helicity partonic matching 验证。

### 10.6 当前仍未解决的问题

- 需要确定 GF-to-quasi 与 ratio/hybrid nonperturbative normalization 的
  不重叠实现；
- 需要增加 unpolarized/helicity 的 quark--gluon singlet mixing；
- 需要对 finite-z/finite-lambda tail 做模型和协方差传播；
- Pz=3 需要补齐短距离外推输入后才能 Fourier；
- 当前只有一个格距，不能做受控 continuum extrapolation；
- 需要 target-mass、higher-twist、matching scale 和 flow-window systematic；
- helicity 的完整一圈 GF-to-quasi partonic calculation 仍为“待确认”；
- 当前 quasi 输出不应被称为最终 gluon PDF。

## 11. 本文档的生成信息

更新日期：2026-09-11  
本次会话标题：N406 gluon flow extrapolation、lambda/Fourier 顺序与 quasi matching 结果交接

本文是给未来 Codex 会话使用的项目交接记录。它把理论、代码、数据
格式、已验证结果和未完成事项放在同一个地方。文中的“物理 PDF”只指
已经完成流方案转换、重整化、混合、LaMET 或 pseudo-ITD matching、极限
控制和有限坐标重构之后的结果；目前本项目的绝大多数产品仍是
finite-flow bare correlator 或 bare matrix element。

本文不包含任何 API key、bearer token、密码、auth 文件内容或其他凭据。

## 1. 项目目标和当前研究问题

### 1.1 总目标

项目的目标是从 thin-link、未做 HYP/APE/stout 预处理的格点规范场出发，
使用四维 Wilson gradient flow 构造 quark 和 gluon 的空间类非局部算符，
计算核子两点/三点函数，得到有限流时间的矩阵元，再完成：

    lattice finite-flow correlator
      -> C3/C2 ratio and state isolation
      -> bare matrix element
      -> ringed/SFTE flow-scheme conversion
      -> renormalized quasi or pseudo matrix element
      -> channel-specific LaMET or pseudo-ITD matching
      -> finite-z reconstruction and PDF

quark 和 gluon 必须分别使用适合各自算符的 matching；不能把 quark 的
ringed-fermion 系数套给 gluon，也不能把 HYP 或 hybrid-renormalization
的常数直接套给 thin-link 4D flow。

### 1.2 当前 ensemble

- ensemble：beta6.41_mu-0.2295_ms-0.2050_L32x96；
- lattice：32^3 x 96；
- 目前主要格距：a 约为 0.0775 fm；
- 初始规范场：thin link / Nosmear；
- quark 原始数据根目录：
  /public/group/lqcd/donghx/Gradient_Flow/Result/beta6.41_mu-0.2295_ms-0.2050_L32x96/thin_link；
- gluon 原始配置目录：
  /public/group/lqcd/configurations/CLOVER/beta6.41_mu-0.2295_ms-0.2050_L32x96。

### 1.3 当前最重要的研究问题

1. quark：普通 flowed fermion endpoint 尚未完成独立的 ringed-field
   normalization Z_chi；因此现有 quark 结果不能直接叫 MSbar quasi-PDF。
2. quark：四维 flow 的多 flow-time 结果需要通过完整的状态隔离、固定物理
   flow radius 的连续极限、SFTE 和 channel-specific LaMET matching。
3. gluon：OPE 和 C3/C2 已经有大量数据，但 physical unpolarized/helicity
   gluon PDF 仍需要 flow-to-quasi conversion、gluon-quark singlet mixing、
   LaMET/pseudo-ITD kernel、有限 z 重构和极限控制。
4. gluon：最新统计产品是 Nconf=406；较早的 Nconf=231 产品仍有图和拟合，
   但只能作为历史/诊断产品。未来分析应默认使用 N406。
5. quark 的 t/a^2=0.8 和 1.1 任务曾提交，但当前日志在 projection 阶段
   找不到 t/a^2=0.8 的 corr_projected 输入；这两个 flow time 尚未完成。

## 2. 已确认结论、依据和不能改变的边界

### 2.1 [已确认] 四维 flow 和三维 flow 不是同一个 scheme

四维 gauge flow 使用所有四个方向的场：

    d B_mu(t,x) / d t = D_nu G_nu,mu(t,x)

quark flow 使用同一个 flowed gauge field 的四维 covariant heat kernel：

    d chi(t,x) / d t = Delta[B(t)] chi(t,x).

三维 flow 只阻尼空间动量，不能自动继承四维 flow 的 finiteness theorem、
ringed-field normalization 或 published 4D matching coefficient。任何 3D
结果必须有独立的 scheme 和 matching 推导。这个结论来自
gradient-flow-quark-pdf skill 的 theory-and-matching contract 和
Note/Gradient_Flow/main.tex 的 3D/4D 专节。

### 2.2 [已确认] thin-link flow 和 HYP-pre-smeared flow 不可混用

当前 production 从 thin link 开始，没有 HYP/APE/stout 预 smear。HYP 旧笔记
DeltaG_Note.pdf 只用于理解历史算符和图形，不能把其中的 HYP/hybrid
renormalization 常数直接用于当前 thin-link flow。

### 2.3 [已确认] gluon unpolarized 算符

代码坐标顺序是 (x,y,z,t)=(0,1,2,3)，Wilson line 沿 z_dir=2。
Euclidean primitive 定义为

    U_{mu nu}(z) =
      sum_x Tr[F_{mu nu}(x+z zhat) W F_{mu nu}(x) W].

保存的两个独立项是

    T_U = M_titi = M_30;30 + M_31;31
    S_U = M_ijij = 2 M_01;01

Euclidean/Minkowski Wick rotation 和场强反对称性给出 production combination

    O_U = T_U - S_U

物理方向投影是

    O_U,even(z) = O_U(+z) + O_U(-z).

数组中的 even_sum 没有除以 2。这个相对负号不能按图形好看程度修改；
它由 Minkowski 0i/ij 结构和 Euclidean Wick phase 固定。依据：
arXiv:2510.26425v2、Note/Gradient_Flow/main.tex、gluon OPE README 和
flowed_gluon_ope.cpp。

### 2.4 [已确认] gluon helicity 算符

Euclidean dual tensor 是

    Fdual_mu,nu = 1/2 epsilon_mu,nu,rho,sigma F_rho,sigma,
    epsilon_xyzt = +1.

当前 primitive 为

    H_ti = F_ti W Fdual_ti
    H_xy = F_xy W Fdual_xy
    T_H = H_tx + H_ty
    S_H = 2 H_xy

Wick rotation 后的 physical target 是

    O_H = T_H - S_H
    O_H,odd(z) = O_H(+z) - O_H(-z).

生产 OPE 文件中的 helicity combined 历史上保存了 T_H+S_H；原始
Mtiti/Mijij 仍然保留，因此不需要重新做 gauge flow/OPE 就可以构造
T_H-S_H。当前分析同时保留：

    (T_H-S_H)_odd       production target
    (T_H+S_H)_odd       legacy/sign diagnostic
    (T_H)_odd           temporal-only diagnostic

matching 不能把 plus-sign diagnostic 变成 physical helicity。依据：
arXiv:2207.08733v2、Note/Gradient_Flow/main.tex、analysis/helicity_operator_comparison.py
和 tests/test_helicity_operator_comparison.py。

### 2.5 [已确认] helicity 的复数和两点函数约定

gluon disconnected estimator 必须为

    C3_U = <O_U C2_nopol> - <O_U><C2_nopol>
    C3_H = <O_H C2_pol35> - <O_H><C2_pol35>

helicity numerator 使用完整复数 pol35。两种 channel 的 denominator 都是
nopol。只有最终 Euclidean phase projection 才取

    Im(R_H) = Re[-i R_H].

当前 bootstrap estimator 直接实现为

    R_U = Re(C3_U) / Re(C2_nopol)
    R_H = Im(C3_H) / Re(C2_nopol).

不能提前把 pol35 或 C3 取虚部，也不能用 pol35 代替 denominator。

### 2.6 [已确认] quark operator/flow 约定

- proton diquark operator：C gamma5 gamma4；
- C2 source/sink：未 flow；
- C3 中的 quasi-PDF current：flow；
- quark flavor：connected u、d，并可构造 u-d；connected u/d 不是完整
  singlet PDF；
- flow：四维同步 gauge/fermion flow；
- temporal boundary：flowed fermion 使用 anti-periodic；
- distillation：NEV_CURRENT=400，NEV_SRC=NEV_VVV=200；
- displacement：delta_z=0..20；
- pilot momenta：Pz=+3,+4,+5；
- pilot source-sink separations：tsep=6..10；
- production step：FLOW_EPSILON=0.01；
- basis/flowed vertex 常用 complex64，contraction/final correlator 用
  complex128；
- 当前 ordinary flowed fermion endpoint 没有已验证 Z_chi。

### 2.7 [不能随意修改] matching 层次

必须区分：

1. finite-flow bare C3/C2；
2. flowed scheme 到 MSbar quasi/pseudo 的 SFTE 或 GF conversion；
3. quasi/pseudo 到 light-cone PDF 的 LaMET/pseudo-ITD kernel。

完成第 1 层不能称为 physical PDF；完成第 2 层也仍不能称为 physical
PDF。singlet unpolarized/helicity 还需要 quark-gluon mixing。transversity
在本 quark workflow 中保持 pending_external_physics_confirmation，直到
相对算符符号经过外部定义确认。

## 3. 符号、坐标、归一化和尺度窗口

### 3.1 坐标和 flow time

- Euclidean coordinate order：x=0, y=1, z=2, t=3；
- gluon Wilson line：z_dir=2；
- lattice flow time：widehat{t}=t/a^2；
- flow radius：

      r_flow = sqrt(8 t) = a sqrt(8 widehat{t});

- 当前 gluon flow times：

      0.1, 0.2, 0.3, 0.4, 0.5, 0.6,
      1.0, 1.4, 1.8, 2.2, 2.6, 3.0, 3.4, 3.8.

- quark 早期 multi-flow pilot：

      0.10:2, 0.20:3, 0.30:3, 0.40:4, 0.50:4, 0.60:5

  冒号后是 temporal-window half width。新提交的 quark 测试使用
  0.80:6 和 1.10:8。

### 3.2 gluon Clover/OPE schema

flowed Clover：

    F_mu,nu = -i (Q_mu,nu - Q_mu,nu^dagger) / 8

production 使用 color-traceless projection。一个 v5 OPE 数组轴为

    (field_projection, channel, z_orientation, component, z, t)
    = (2, 2, 4, 6, 25, 96)

labels：

    field_projection: legacy_untraced, traceless
    channel: unpolarized, helicity
    z_orientation: plus_z_raw, minus_z_raw, even_sum, odd_difference
    component: combined, Mtiti, Mijij, ti, tj, ij_single

raw plus/minus 和全部 components 必须保留，因为它们可以做 exact linear
identity、Hermiticity、parity 和 helicity sign checks。

### 3.3 quark ringed-field SFTE

流 quark bilocal 需要 ringed fields：

    chi_ringed = Z_chi(t)^(1/2) chi(t)

两个 flowed fermion endpoint 合并成 bilocal 的一个总体 Z_chi。非微扰
定义模板在

    /public/home/donghx/Gradient_Flow/Blending_L32x96/small_flow_time/ringed_z_chi.template.json

模板不是实测数据，不能直接拿来生产。Z_chi 必须在每个 ensemble/flow
time 通过明确的 derivative、mass/chiral prescription 独立测量。

四维 4D ringed bilocal 的 corrected one-loop coefficient（Brambilla--Wang
2024 convention）为

    C_psi(t,mu) =
      1 - alpha_s C_F/(4 pi)
          [3 log(2 mu^2 t exp(gamma_E)) + 2 + log(432)]

    delta_m(t) =
      - alpha_s C_F/(4 pi) sqrt(2 pi) / sqrt(t)

其逆转换形式为

    h_quasi_MSbar =
      Z_chi(t) C_psi(t,mu)^(-1)
      exp[-delta_m(t)|z|] h_GF
      + flow-power corrections.

### 3.4 gluon GF-to-quasi matching

四维 gluon auxiliary-field convention使用

    c_parallel_perp = 1 + O(alpha_s^2)
    c_perp_perp =
      1 + alpha_s C_A/(4 pi) log(2 mu^2 t exp(gamma_E))

    delta_m_A =
      - alpha_s C_A/(4 pi) sqrt(2 pi/t)

相对于 z Wilson line：

    Z_U = kappa_F^2 exp[-delta_m_A |z|] / c_perp_perp^2
    Z_H = kappa_F^2 exp[-delta_m_A |z|]
          / (c_parallel_perp c_perp_perp)

当前代码/图诊断取 kappa_F=1；这不是已经完成的 tree-level normalization
证明，标记为待确认。系数中的 t 必须用 GeV^{-2}，不能把无量纲 t/a^2
直接放进 logarithm。matching 因子对 +z/-z 使用相同的 |z|。

当前推荐在逐组态 OPE、vacuum subtraction、C3/C2 和 bootstrap 之前施加
Z_U/Z_H；因为该因子是确定性 scalar，乘在 fit-level shared bootstrap
replica 上可以作为诊断，但不是最终 production substitute。

### 3.5 window 和极限

必须全局选择而不是逐点挑误差最小的数据：

    a^2/t << 1
    sqrt(t) Pz << 1
    t Lambda_QCD^2 << 1
    r_flow << |z|       (非零 z)
    Pz^2 >> M_N^2

quark/gluon 共同需要：

- fixed physical flow time/radius，而不是跨格距直接固定 t/a^2；
- continuum at fixed physical t,z,Pz；
- flow-time window、finite-z、finite-volume、Pz、fit-window 和
  perturbative-order systematic；
- t=0.5 时 r_flow/a=2；z/a<=2 不满足干净的 r_flow << |z|；
- quark skill 给出的 t=0.5 估计 sqrt(t)Pz 对 Pz=3,4,5 约为
  0.42, 0.56, 0.69，最高动量 marginal。

## 4. 代码入口、数据路径和运行命令

### 4.1 gluon OPE production

代码根：

    /public/group/lqcd/donghx/Gradient_Flow_GluonPDF

重要入口：

    src/flowed_gluon_ope.cpp
    scripts/build_v5.sh
    scripts/run_one_v5.py
    scripts/validate_output_v5.py
    slurm/v5/flowed_ope_cpu_v5.slurm
    slurm/v5/flowed_ope_chain_cpu_v5.slurm
    slurm/v5/submit_all_tau_v5.sh

构建和提交：

    cd /public/group/lqcd/donghx/Gradient_Flow_GluonPDF
    ./scripts/build_v5.sh
    ./slurm/v5/submit_all_tau_v5.sh

v5 提交约定：

    partitions = a192c1t,cpu6248R,cpueicc,i72c512g
    cpus_per_task = 48
    epsilon = 0.01
    fine epsilon gate = 0.005 on conf1000
    z_count = 25
    z_dir = 2

提交记录：

    runs/submission_all_tau_v5_20260903_002048.txt

它记录了 887 个 manifest entries、14 个 tau、依赖 gate 和 chain heads。

### 4.2 gluon latest ratio/bootstrap

代码：

    ratio_bootstrap_latest_v1/construct_bootstrap.py
    ratio_bootstrap_latest_v1/validate_collection.py
    ratio_bootstrap_latest_v1/audit_statistics.py
    ratio_bootstrap_latest_v1/slurm/submit_all.sh

运行：

    cd /public/group/lqcd/donghx/Gradient_Flow_GluonPDF
    python -m py_compile ratio_bootstrap_latest_v1/*.py
    python -m pytest ratio_bootstrap_latest_v1/tests -q
    bash ratio_bootstrap_latest_v1/slurm/submit_all.sh
    python ratio_bootstrap_latest_v1/validate_collection.py

latest frozen manifest：

    ratio_bootstrap_latest_v1/manifests/common_all14_plusz_P345.tsv
    SHA256 = 1a2161d754493f03a4c5e26d5fe20a0a83446f762f3a8bc159cc282f866b53e4

authoritative latest ratios：

    ratio_bootstrap_latest_v1/results_v1/

### 4.3 gluon latest bare fits

代码：

    fit_latest_v1/fit_bare_latest.py

运行一个 flow time 或全部：

    cd /public/group/lqcd/donghx/Gradient_Flow_GluonPDF
    python fit_latest_v1/fit_bare_latest.py --tau 0.5
    python fit_latest_v1/fit_bare_latest.py

结果：

    fit_latest_v1/results_v1/
    fit_latest_v1/fit_collection_validation.json

拟合约定：

    Tmin = floor(0.6 fm / 0.0775 fm) + 1 = 8
    Tmin physical label approximately 0.62 fm
    Tmax = 9,...,15
    symmetric cuts c = 1,2,3
    forward Sumratio-difference plateau
    Schaefer-Strimmer covariance
    central Q >= 0.01
    central chi2/dof <= 3
    bootstrap success >= 0.90
    replica-wise AIC fit-range weights
    equal-weight mixing of usable cuts
    Nboot=1500, std(ddof=1)

### 4.4 gluon matching and plots

代码：

    matching/gluon_flow_to_quasi.py
    matching/calc_ratio_matched.py
    matching/plot_matched_bare_matrix.py
    matching/plot_pz3_results.py
    matching/test_gluon_flow_to_quasi.py

测试：

    cd /public/group/lqcd/donghx/Gradient_Flow_GluonPDF/matching
    python -m pytest test_gluon_flow_to_quasi.py -q

matching 代码的 per-configuration 使用方式：

    python matching/gluon_flow_to_quasi.py \
      --input output_v5/conf8300/tau0p500 \
      --output matched_quasi_v1/conf8300/tau0p500 \
      --tau 0.5 --mu 2.0 --alpha-s 0.25

注意：这是 GF-to-quasi/operator conversion，不是 light-cone PDF matching。

### 4.5 quark 4D flow

active successor：

    /public/home/donghx/Gradient_Flow/Blending_L32x96

核心代码：

    flow_common_l32x96.py
    generate_flowed_vertex_l32x96.py
    calc_flowed_c2c3_factorized_l32x96.py
    calc_flowed_c2c3_l32x96.py
    project_flowed_channels_l32x96.py
    validate_multiflow_conf_l32x96.py
    verify_multiflow_restart_l32x96.py
    cleanup_flow_cache_l32x96.py

driver：

    run_multiflow_channels_l32x96_4gpu_a800.slurm

历史/当前提交脚本：

    /public/group/lqcd/donghx/Gradient_Flow_GluonPDF/submit_quark_flow_02_08_all10.sh
    /public/group/lqcd/donghx/Gradient_Flow_GluonPDF/submit_quark_flow_0811_all10.sh

这些脚本使用 pilot_z、Pz=+3,+4,+5、tsep=6..10。不要在已经排队的
job 直接改 driver；应复制成版本化 successor 后测试再提交。

### 4.6 旧/一般 quark bare-matrix workflow

connected quark bare-matrix 的一般工作流位于：

    /public/group/lqcd/donghx/Diagram_GluonPDF/Fit_SKILL/C3_Ratio_Bootstrap
    /public/group/lqcd/donghx/Diagram_GluonPDF/Fit_SKILL/Bare_Matrix_Fit

主要命令：

    python3 run.py show-config --ensemble L32x64
    python3 run.py validate-conventions --ensemble L32x64
    python3 run.py audit-inputs --ensemble L32x64
    python3 run.py bootstrap --ensemble L32x64 \
      --channels unpolarized,helicity \
      --flavors u,d,u_minus_d --nboot 1500 --seed 1115 --c2-mode complex
    python3 -m unittest discover -s tests -v

当前 connected-quark 一般 workflow 的权威产品契约是
c3_ratio_v3、ratio_v4、bare_matrix_fit_v3；旧 ratio v2/bare-fit v1
不能恢复为 physics product。它和 local flowed-gluon N406 产品不要混淆。

## 5. 已完成的计算、检查和验证

### 5.1 gluon OPE v5

[已确认] output_v5 已覆盖：

    887 个组态目录
    14 个 flow time
    887 x 14 = 12418 个 epsilon=0.01 OPE npy/json pairs
    另有 conf1000 的 14 个 epsilon=0.005 fine-gate pairs

数组 schema、atomic output、finite check、orientation/component identity
由 validate_output_v5.py 检查。epsilon gate 的全部 14 个 flow time 均
status=passed；代表性最大值仍远低于阈值：

    max_relative_l2 threshold = 0.005
    max_plaquette_diff threshold = 5e-5

提交日志中的 kernel/source/run/validator SHA256 已记录，未来若修改
源码必须生成新的 versioned output，不要覆盖 v5。

### 5.2 gluon latest N406 ratio/bootstrap

[已确认] ratio_bootstrap_latest_v1：

    Nsource = 887
    frozen common Nconf = 406
    Nboot = 1500
    seed = 1115
    flow times = 14
    job array 3565822: 14 tasks, exit code 0:0
    shared configuration order = true
    shared bootstrap indices = true
    collection status = complete_and_shared_indices_validated

当前 frozen manifest 是为了避免 flow-time 之间配置列表漂移。每个 tau
的完整 bootstrap npz 和 SHA256 记录在 collection_validation.json。

### 5.3 gluon latest N406 bare fits

[已确认] fit_latest_v1：

    fit_total = 225 points per flow time
    filled_count = 219 per flow time
    accepted fit counts:
      tau 0.1--0.5: 219
      tau 0.6: 216
      tau 1.0: 210
      tau 1.4: 208
      tau 1.8: 203
      tau 2.2: 197
      tau 2.6: 195
      tau 3.0: 193
      tau 3.4: 191
      tau 3.8: 190

这些是 finite-flow bare matrix elements，不是 renormalized/matched PDFs。

### 5.4 gluon N231 historical products and figures

此前使用 Nconf=231 的产品生成了：

    /public/group/lqcd/donghx/Diagram_GluonPDF/Gradient_flow_gluon/results_v2
    /public/group/lqcd/donghx/Diagram_GluonPDF/Gradient_flow_gluon/results_v3
    /public/group/lqcd/donghx/Diagram_GluonPDF/Gradient_flow_gluon/bare_fit_sumdiff_aic_v1/products
    /public/group/lqcd/donghx/Gradient_Flow_GluonPDF/matching/pz3_comparison_v1

Pz=3 的裸矩阵元和 matching 前后图已画出；每个 tau 的 z/a=0..15
单独 PDF 位于 matching/pz3_comparison_v1/bare_by_tau_z0to15。它们
对于检查算符和图形很有用，但不应覆盖或替代当前 N406 分析。

### 5.5 quark 计算和检查

[已确认] 流动/投影代码已通过多项局部检查：

- zero-flow identity、basis/vertex axis、gauge covariance、flowed-link
  checks 和 factorized contraction smoke tests 已实现；
- test job 3569237 的五个 gauge-index 检查通过：
  t/a^2 = 0.1, 0.2, 0.3, 0.4, 0.6；
- direct-versus-restart equivalence 的 preflight 阶段通过；
- quark ordinary-flow correlators 尚未有 validated Z_chi。

[待确认/未完成] 新的 gf0811 job 3571893..3571902：

- preflight 和 direct-vs-restart 阶段通过；
- driver 计划 pending flow specs=0.8:6,1.1:8；
- projection 失败，错误为找不到
  thin_tf0p80000000_eps0p01000000_tw6_Nv400_dz21/Nev_200/<conf>/
  corr_projected_tsep6_dz0-20_Nev200.npz；
- 因此 0.8/1.1 不能标记为 complete；
- 目前也不能仅凭这些 job 的 stdout 宣称 quark C3/C2 已完成。

当前环境中 squeue 查询返回 Slurm stream socket Operation not permitted；
queue 状态应在能访问 Slurm controller 的登录环境重新查询。

### 5.6 theory notes and documents

主要理论文档：

    /public/home/donghx/Note/Gradient_Flow/main.tex
    /public/home/donghx/Note/Gradient_Flow/main.pdf
    /public/home/donghx/Note/Gradient_Flow/DeltaG_Note.pdf
    /public/home/donghx/.codex/Markdown/gluon_gradient_flow_matching.md

main.tex 是当前整理后的 quark+gluon note；DeltaG_Note.pdf 是旧 HYP5
helicity/gluon note；gluon_gradient_flow_matching.md 专门记录 gluon
GF-to-quasi 推导、端点系数、T/S 组合和实现状态。

## 6. 尚未解决的问题和下一步最具体的操作

### 6.1 最高优先级：修复 quark 0.8/1.1

不要先重跑 fit。先在可访问 GPU 的环境做：

1. 检查每个 0.8/1.1 conf 是否存在 flowed basis、flowed gauge、
   flowed vertex 和 Nev_200 projected input；
2. 检查 driver 是否在 projection 之前正确调用
   generate_flowed_vertex_l32x96.py 和 calc_flowed_c2c3_factorized_l32x96.py；
3. 对 conf=10000 做一个 isolated successor smoke run，确认
   t/a^2=0.8 的 source path 被生成；
4. 运行 validate_multiflow_conf_l32x96.py --raw；
5. 只有 raw C3/C2、metadata、completion guard 全部通过后，才恢复
   10100..10900 和 1.1；
6. 重新记录 job IDs、output/error 路径和 completion receipts。

不要把“preflight passed”写成“flow output complete”。

### 6.2 quark ringed normalization

需要为 L32x96 的每个 flow time 测量 Z_chi(t)：

1. 明确定义 massless/chiral 和 derivative discretization；
2. 使用与 4D flowed fermion 相同的 thin-link gauge flow；
3. 对每个 tau 生成带统计误差的 ringed_z_chi JSON；
4. 运行 small_flow_time/apply_sfte.py 的 tests；
5. 形成 Z_chi uncertainty 和 SFTE coefficient uncertainty；
6. 先得到 MSbar bilocal diagnostic，再继续 LaMET。

禁止直接复制 template JSON 或把 C3/C2 的 nucleon overlap cancellation
当成 Z_chi cancellation。

### 6.3 gluon N406 的匹配和 flow-time 分析

建议顺序：

1. 使用 ratio_bootstrap_latest_v1/results_v1 和 fit_latest_v1/results_v1；
2. 在逐组态 OPE 上应用 Z_U/Z_H，或者明确标记 fit-level conversion
   为 diagnostic；
3. 重新做 N406 的 TH-SH、TH+SH、TH 三种 helicity 对比；
4. 对每个 tau 重新做 bare-versus-matched Pz=3/4/5 图；
5. 只在通过 global SFTE window mask 的 tau,z,Pz 上做小 flow extrapolation；
6. 记录 flow-time fit window、AIC 权重、相关性和所有 failed points；
7. 加入 gluon-singlet/quark mixing 后才讨论 gluon PDF。

旧 N231 的 tau>1 AIC extrapolation 和 z/a=0..15 图不能直接当作 N406
结论，应以 N406 重新运行。

### 6.4 continuum、LaMET 和 PDF reconstruction

目前只有一个 lattice spacing 的 gluon 主结果，因此不能做可信的
continuum extrapolation。quark 也必须在固定物理 flow radius、z、Pz
上合并多个格距。之后：

- 选择与 operator scheme 一致的 unpolarized/helicity quasi 或 pseudo-ITD
  kernel；
- singlet 保留 quark-gluon mixing matrix；
- 检查 target-mass、higher-twist、finite-volume、finite-z；
- 对 Fourier/reconstruction 的 truncation 和 covariance 做稳定性扫描；
- 只在所有层都完成后报告 g(x,mu) 或 Delta g(x,mu)。

## 7. 不确定内容标记

以下事项明确是“待确认”，不能在后续会话中被写成已完成：

- gluon Clover tree-level normalization kappa_F；当前 matching 诊断使用
  kappa_F=1；
- gluon GF-to-quasi 一圈系数在当前 lattice normalization、color
  projection 和所有 finite-a terms 下的完整适用范围；
- quark 的非扰动 Z_chi；
- quark 0.8/1.1 的 raw output completion；
- gluon channel-specific singlet GF-to-quasi mixing 的完整高阶结果；
- physical continuum/flow-time window；
- finite-z reconstruction 到 x-space 的稳定性；
- transversity 的外部相对符号确认。

以下内容是“历史/诊断”，不要升级为物理结论：

- DeltaG_Note.pdf 中的 HYP5/Wilson3 结果；
- gluon N231 results_v2/results_v3 和 bare_fit_sumdiff_aic_v1；
- fit-level matching 图；
- 单一 tau、单一格距、单一 Pz 的漂亮 plateau；
- ordinary flowed quark C3/C2 在没有 Z_chi 时的 MSbar/PDF 解释。

## 8. 不可随意修改的约定

1. 不能把 HYP-pre-smeared 输入和 thin-link GF matching 混在一起。
2. 不能改变坐标顺序 (x,y,z,t)=(0,1,2,3) 而不重新验证所有 epsilon、
   Clover、dual 和 component labels。
3. gluon unpolarized physical operator 固定为
   (T_U-S_U)_even。
4. gluon helicity physical target 固定为
   (T_H-S_H)_odd；plus 和 temporal-only 只能作为 diagnostics。
5. even_sum/odd_difference 当前没有 1/2。
6. helicity 的完整 complex pol35 必须在 vacuum subtraction 和 covariance
   构造前保留；denominator 是 nopol。
7. 每个 bootstrap replica 先做 ratio，再做最后的 Re/Im projection；
   不能用 mean(C3)/mean(C2) 或 mean(C3/C2) 替换声明的 estimator。
8. 所有 tau、channel、flavor、direction、fit method 必须共享明确对齐的
   configuration order 和 bootstrap index array。
9. NaN padding 和 invalid masks 不是零数据，不能填零后拟合。
10. flow-time、fit window、z cut 必须全局预注册，不能按点挑最小误差。
11. finite-flow bare correlator、MSbar bilocal 和 physical PDF 必须使用
   不同 status 名称。
12. 不要删除旧 products；如需修复，生成 versioned successor 并保存
   code/config/manifest/output SHA256。

## 9. 参考文献和交接入口

核心论文：

- M. Luscher, arXiv:1006.4518；
- M. Luscher, arXiv:1302.5246；
- Monahan and Orginos, arXiv:1612.01584；
- Brambilla and Wang, arXiv:2312.05032；
- Khan et al., arXiv:2107.08960；
- Egerer et al., arXiv:2207.08733v2；
- Balitsky, Morris and Radyushkin, arXiv:2112.02011；
- Chen et al., arXiv:2510.26425v2。

未来 Codex 开始工作时，建议先读：

1. 本文；
2. /public/home/donghx/.codex/skills/gradient-flow-quark-pdf/SKILL.md；
3. /public/home/donghx/.codex/skills/quark-pdf-bare-matrix/SKILL.md；
4. /public/home/donghx/Note/Gradient_Flow/main.tex；
5. 当前任务对应的 collection_validation.json、fit_collection_validation.json
   和 Slurm completion/validation receipts。

最后重新查询 Slurm 和文件 completion markers；不要仅依赖本文中记录的
历史 job state。

---

文档生成日期：2026-09-08  
本次会话标题：Gradient-flow quark/gluon PDF 全链路状态、约定与继续工作清单
