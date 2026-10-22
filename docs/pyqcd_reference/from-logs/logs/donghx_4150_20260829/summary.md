# donghx / PyQCD 组态 4150 对照证据

本目录记录本轮可提交的轻量证据索引；原始规范场、本征矢量、perambulator、HYP
场和参考产物均只读于用户明确给出的 `/public/group/lqcd/...` 路径，未复制到仓库。
大型 VVV/2pt 数组保留在本机生成目录或 `data/cmp1_4150/`，不进入 Git。

## 资产盘点

盘点命令：

```text
python examples/pyqcd/cmp1/manifest_4150.py --output examples/pyqcd/cmp1/v202608291424/manifest.json
python examples/pyqcd/cmp1/verify_manifest_4150.py
```

| 资产 | 当前事实 |
|---|---|
| Clover 规范场 | 存在，573439152 bytes |
| eigenvectors/4150 | 存在，72 个文件，4777574400 bytes |
| light perambulators/4150 | 存在，288 个文件，13271040000 bytes |
| HYP 3D 1/3/5 次、4D 10 次 | 均存在，各 7 个记录文件，约 573 MB；4D10 已完成三方向 OPE 对照 |
| 2pt_Result 系综目录 | 存在，322 个文件；本轮选定 7 个 4150 根目录；另有 `effmass` 聚合数组 7 项、25 个动量行已逐数组检查 |
| TMD OPE x/y/z 结果 | 存在，58 个文件；含横向位移参数，未与本轮直线 OPE 混合比较 |
| `Result_hpy_4D_10times` | 当前路径不存在 |
| `Peram_code_2505`、`Peram_mpi`、`Peram_result` | 当前用户给定路径不存在 |

## 低层真实对照

结果：`examples/pyqcd/cmp1/v202608291500_lowlevel/results.json`。

| 对象 | 形状 | 相对差 | 状态 |
|---|---|---:|---|
| eigvec | `(8, 13824, 3)` | 0 | pass |
| phase | `(13824,)` | 0 | pass |
| VdV | `(1, 4, 4)` | 1.31e-15 | pass |
| VVV | `(4, 4, 4)` | 4.75e-16 | pass |
| Clover | `(4, 4, 2, 24, 24, 24, 3, 3)` | 2.45e-16 | pass |
| dual | `(4, 4, 2, 24, 24, 24, 3, 3)` | 1.89e-16 | pass |
| OPE | `(2, 2)` | 1.36e-15 | pass |

比较基准是同一 4150 规范场上独立重写的 donghx 参考公式；这七项不等同于
“外部逐时间 VVV 文件”对照。

## HYP 规范场与非极化 OPE 真实对照

运行入口：

```text
python examples/pyqcd/cmp1/run_4150_hyp_ope.py --smear 4d10 --directions x,y,z --outdir examples/pyqcd/cmp1/v20260829_hyp_ope_xyz
python examples/pyqcd/cmp1/run_4150_hyp_ope.py --smear 3d1 --directions z --outdir examples/pyqcd/cmp1/v20260829_hyp_ope_3d1_z
python examples/pyqcd/cmp1/run_4150_hyp_ope.py --smear 3d3 --directions z --outdir examples/pyqcd/cmp1/v20260829_hyp_ope_3d3_z
python examples/pyqcd/cmp1/run_4150_hyp_ope.py --smear 3d5 --directions z --outdir examples/pyqcd/cmp1/v20260829_hyp_ope_3d5_z
```

输入是各 `.lime.contents/msg02.rec04.ildg-binary-data`，读取后为
`(Nt,Nz,Ny,Nx,4,3,3)=(72,24,24,24,4,3,3)` 的 `complex128` 规范场；
`4d10` 的最大链接幺正性偏差为 `1.11e-15`。比较调用
`gluon_ope_operator_z0(..., second_insert="F")`，即 donghx 非极化
`F\,W\,F\,W` 通道；参考 TMD 成品只取横向位移为零的直线截面，不能据此宣称
非零横向 staple 已验证。

### 4D HYP 10 次：三方向 9 个通道

结果：`examples/pyqcd/cmp1/v20260829_hyp_ope_xyz/results.json`，摘要：
`examples/pyqcd/cmp1/v20260829_hyp_ope_xyz/summary.md`。

| 方向 | 通道数 | 输出形状 | 最大相对 L2 | 最大绝对差 | 状态 |
|---|---:|---|---:|---:|---|
| x | 3 | `(72,9)` | `3.30e-15` | `5.69e-13` | pass |
| y | 3 | `(72,9)` | `3.31e-15` | `5.69e-13` | pass |
| z | 3 | `(72,12)` | `7.50e-17` | `5.69e-14` | pass |

9/9 通道均为 `pass`，整体 runner 退出码为 0。

### 3D HYP 1/3/5 次：真实运行但无可配对参考成品

三次 z 向运行均成功构造并计算 3 个通道，输出形状均为 `(72,12)`，规范场均为
`complex128` 且最大幺正性偏差为 `1.11e-15`；由于用户给出的参考 OPE 成品只属于
`4d10`，三个结果按设计记为 `unverified`，runner 退出码均为 2。结果目录分别为：

```text
examples/pyqcd/cmp1/v20260829_hyp_ope_3d1_z/
examples/pyqcd/cmp1/v20260829_hyp_ope_3d3_z/
examples/pyqcd/cmp1/v20260829_hyp_ope_3d5_z/
```

## 费米子 2pt 真实对照

主结果：`examples/pyqcd/cmp1/v202608300145_cg5g4/`；
`Cg5` 结果：`examples/pyqcd/cmp1/v202608300146_cg5/`。
主结果为 `Nev=100`、`t_source=0`、`Delta t=2..36` 的 35 个时间对；其余动量
配置取 `Delta t=2`，且均复用经过形状/dtype 校验的本地 VVV 缓存。

| 通道/动量 | contract 相对差 | nopol 相对差 | 参考精度 |
|---|---:|---:|---|
| `Cg5g4`, `(Pz,Py,Px)=(0,0,0)` | 3.50e-15 | 1.27e-15 | complex128 |
| `Cg5`, `(0,0,0)` | 2.29e-15 | 1.53e-15 | complex128 |
| `Cg5g4`, `Pz=1`（单时间对） | 2.53e-15 | 8.56e-16 | complex128 |
| `Cg5g4`, `Pz=2`（单时间对） | 2.31e-15 | 8.26e-16 | complex128 |
| `Cg5g4`, `Pz=5`（单时间对） | 1.66e-15 | 1.42e-16 | complex128 |
| `Cg5g4`, `Px=1`（单时间对） | 2.64e-06 | 1.42e-06 | complex64，tol=1e-5 |
| `Cg5g4`, `Py=1`（单时间对） | 2.59e-06 | 5.94e-07 | complex64，tol=1e-5 |

每个 runner 的第三项 `vvv` 均为 `unverified(reference_output_missing)`：用户给定
参考结果目录没有可直接读取的逐时间 `VVV.t*.Px*Py*Pz*` 中间文件。因此整体状态
必须是 `unverified`，但已有 contract/nopol 数值比较仍为 `pass`。

### 无 momentum smear 的方向/大小矩阵

在同一组态、同一标准 light perambulator 上，按 `P=(Pz,Py,Px)` 分别覆盖
`Pz=0..5`、`Py=1..5`、`Px=1..5`。每个非零动量取 `Delta t=2`；`Cg5g4` 的
`P=0` 另取 `Delta t=2..36` 的 35 对。结果由各版本目录的 `results.json` 汇总：

| 变体 | 动量配置数 | 选定时间对 | contract/nopol | 参考 dtype | 最大 contract 相对差 | 最大 nopol 相对差 |
|---|---:|---:|---|---|---:|---:|
| `Cg5g4` | 16 | 50 | 16/16 pass | c128 12，c64 4 | 2.6388e-6 | 1.5445e-6 |
| `Cg5` | 16 | 16 | 16/16 pass | c128 16 | 3.0761e-15 | 1.7189e-15 |

其中每个 `contract` 输出形状为 `(72,72,4,4)`，每个 `nopol_pp` 输出形状为
`(72,72)`；`Cg5g4` 的 c64 参考采用 `tol=1e-5`，最大误差仍在容差内。上述
矩阵只证明无 momentum smear 的 2pt 中间/投影对象；`momsmear±2{x,y,z}` 仍需
独立 smeared perambulator，不能由标准 perambulator 推断。对已有 momentum-smear
最终成品，另有独立的输出级投影检查，见下节。

## momentum-smear 最终输出级检查

检查入口：`examples/pyqcd/cmp1/inspect_4150_momsmear.py`；结果：
`examples/pyqcd/cmp1/v20260830123306_4150_2pt_polar/results.json`；本次检查器因发现
标准极化差异而按约定退出 `2`，不是读取或运行错误。

参考可见的计算顺序是：固定 $q=\pm2\hat d$ 相位乘到低模 → 以输出动量 $P$ 逐时间构造
VVV → 读取四个 source-Dirac 文件组成 peram → 两项质子颜色 epsilon 缩并 →
$P_+=\frac12(\gamma_0+\gamma_4)$ 投影 → 对反周期边界应用 $t_s<t_0$ 的负号，最后
保存 `contract` 与 `nopol_ss`。本检查只复算最后两步的输出关系，不把普通 light
perambulator 代替独立 momentum-smeared perambulator。

| 根目录 | 相位 | 动量覆盖 | 文件数 | 动量组 | projection pass | 最大 rel L2 |
|---|---|---|---:|---:|---:|---:|
| `momsmear-2x` | $-2\hat x$ | $P_x=-2\ldots-6$ | 25 | 5 | 5/5 | 5.20e-8 |
| `momsmear-2y` | $-2\hat y$ | $P_y=-2\ldots-6$ | 25 | 5 | 5/5 | 5.28e-8 |
| `momsmear-2z` | $-2\hat z$ | $P_z=-2\ldots-6$ | 25 | 5 | 5/5 | 5.85e-8 |
| `momsmear2x` | $+2\hat x$ | $P_x=2\ldots6$ | 25 | 5 | 5/5 | 4.63e-8 |
| `momsmear2z` | $+2\hat z$ | $P_z=0,2\ldots6$ | 27 | 6 | 6/6 | 5.01e-8 |

合计 127 个文件、26 个动量组，26/26 通过；所有 `contract`/`nopol_ss` 为
`(72,72,4,4)`/`(72,72)`，最大相对 L2 为 `5.86e-8`，最大绝对差为
`7.57e-10`，c64 容差为 `5e-6`。这证明输出文件的投影和边界实现自洽，不能升级
为 PyQCD 使用独立 smeared peram 重算并与参考 raw VVV/peram 一致。

本轮又纳入两个 `momsmear0` 根目录（其文件名无算符后缀，检查器以
`variant=implicit` 保留事实，不从目录名猜测物理变体）：

| 根目录 | 相位 | 动量覆盖 | 文件数 | 动量组 | projection pass | 最大 rel L2 |
|---|---|---|---:|---:|---:|---:|
| `momsmear0_Cg5` | 0 | $P_z=0\ldots5$、$P_y/P_x=1\ldots5$ | 47 | 16 | 16/16 | 0 |
| `momsmear0_Cg5g4` | 0 | $P_z=0\ldots5$、$P_y/P_x=1\ldots5$ | 58 | 16 | 16/16 | 8.29e-7 |

七个根目录合计 232 个已解析数组、58 个动量组，`contract → P+ → 反周期边界 →
nopol` 为 58/58；全体最大相对 L2 为 `8.29e-7`，最大绝对差为 `1.98e-9`，仍在
complex64 的 `5e-6` 容差内。`momsmear0` 只表示输出配置；三个独立 momentum-smeared
perambulator 候选目录仍不存在。

### 极化输出级检查：标准 `li` 与参考旧 `il` 变体分开记账

参考极化矩阵由 `P_+ (i gamma_d gamma5)` 构造，其中
`d=1,2,3` 分别对应 `pol15/pol25/pol35`。标准收缩是：

```text
einsum("li,yxil->yx", projector, contract)
```

然后沿用 `t_sink < t_source` 的反周期负号。参考
`refer/donghx/2pt_diffpol/L24x72_diffpol.py:121-129` 的极化输出使用
`einsum("il,yxil->yx", ...)`；它是转置轴变体，不能替代标准 `li`。

本次对 7 个根目录的 174 个极化槽位逐项检查：

| 标准 `li` 状态 | 数量 | 解释 |
|---|---:|---|
| `pass` | 74 | 116 个实际存在的极化数组中，标准投影相符 |
| `diff` 且旧 `il` `pass` | 41 | 与参考旧转置实现相符，只作为诊断，不升级为标准通过 |
| `diff` 且旧 `il` 也 `diff` | 1 | `momsmear2x`，`P=(Pz,Py,Px)=(0,0,6)`，`Cg5g4/pol15` |
| `unverified` | 58 | 极化文件缺失，不能当作失败或通过 |

异常槽位的 `pol15` 输出范数约为 `3.30e-9`；标准 `li` 与旧 `il` 均给出
`max_abs=1.25e-4` 的不符，故相对 L2（以成品范数作分母）达到约 `1.51e5`，
该相对数值受近零分母支配。对应 `contract → nopol` 仍通过，异常只归属于该
极化成品槽位。各根目录的极化计数如下：

| 根目录 | 动量组 | `li`: pass/diff/unverified |
|---|---:|---:|
| `momsmear-2x` | 5 | 10/5/0 |
| `momsmear-2y` | 5 | 10/5/0 |
| `momsmear-2z` | 5 | 10/5/0 |
| `momsmear2x` | 5 | 9/6/0 |
| `momsmear2z` | 6 | 10/5/3 |
| `momsmear0_Cg5` | 16 | 15/0/33 |
| `momsmear0_Cg5g4` | 16 | 10/16/22 |

这一步闭合了参考成品的极化/边界输出级事实，并暴露了参考实现的轴序分支；
它不等同于 PyQCD 已用独立 momentum-smeared perambulator 重算 raw VVV。

## effmass 聚合 2pt：4150 样本索引与逐数组对应

本轮新增检查器：`examples/pyqcd/cmp1/inspect_4150_effmass.py`，受控测试为
`examples/pyqcd/cmp1/verify_4150_effmass.py`。参考聚合脚本的组态序列是
`4050 + 50*k`，所以组态 4150 对应聚合索引 `k=2`。检查器不只比较形状：对 raw
`Res_2pt*.npy` 逐矩阵定位 4150 行；对 `twoptall*.npy` 先按
`(t_sink - t_source) mod 72` 汇总可见 4150 的 `(72,72)` 矩阵，再比较聚合行。
complex64 输入的时间汇总先升宽为 complex128，避免累加精度造成假差异。

结果：`examples/pyqcd/cmp1/v202608301600_4150_effmass_aggregate/results.json`，
摘要：`examples/pyqcd/cmp1/v202608301600_4150_effmass_aggregate/summary.md`。

| 聚合资产 | 形状 | 动量行 | 最大相对差 | 4150 索引（命中/行数） | 状态 |
|---|---|---:|---:|---:|---|
| raw `+2z` momentum-smear | `(5,879,72,72)` | 5 | `0` | `2`（5/5） | pass |
| raw `-2z` momentum-smear | `(5,879,72,72)` | 5 | `0` | `2`（5/5） | pass |
| raw `momsmear0 Cg5g4` | `(4,878,72,72)` | 4 | `0` | `2`（4/4） | pass |
| `twoptall +2z` | `(5,879,72)` | 5 | `2.58e-16` | `2`（5/5） | pass |
| `twoptall momsmear0 Cg5g4` | `(4,878,72)` | 4 | `7.12e-18` | `2`（4/4） | pass |
| `twoptall Pz0 Cg5` | `(1,879,72)` | 1 | `3.94e-17` | `2`（1/1） | pass |
| `twoptall Pz0 Cg5g4` | `(1,876,72)` | 1 | `1.87e-17` | `2`（1/1） | pass |

受控测试 `verify_4150_effmass: PASS 3/3`，真实检查
`inspect_4150_effmass: assets=7 pass=7 diff=0 unverified=0 rows=25`。
raw 矩阵行均为逐位相等；`twoptall` 最大相对差为 `2.58e-16`。这闭合了可见
effmass 聚合数组与 4150 单组态 2pt 成品的样本对应关系，但仍不等同于独立
momentum-smeared perambulator、逐时间 VVV 或 3pt/ratio/barematrix 的输入级复现。

## 3pt、ratio、barematrix 配对盘点

在用户明确给出的对照根目录中，`2pt_Result/.../4150` 的匹配文件是
`twopt_slice_*` 2pt 数组；`Contraction` 目录是 `Wick_contraction.py` 与 Wick 图
PDF；TMD OPE 目录是 x/y/z 方向的 `ops_*` 数组。没有发现同时具备组态 4150、同一
动量/方向、同一 OPE 几何和插入时间元数据的 raw 3pt 数组，也没有可一一配对的
ratio/barematrix 数值成品；`Result_hpy_4D_10times` 当前不存在。因此本轮不运行
或生成这些下游的伪比较，状态保持 `unverified`。

## 本轮断言

```text
verify_manifest_4150: PASS 4/4
verify_4150_lowlevel: PASS 3/3
verify_4150_fermion: PASS 3/3
verify_4150_fermion_runner: PASS 12/12
verify_4150_hyp_ope_runner: PASS 3/3
verify_4150_momsmear: PASS 7/7
verify_4150_effmass: PASS 3/3
inspect_4150_effmass: assets=7 pass=7 diff=0 unverified=0 rows=25
```

完整主回归和报告编译结果见最终交付说明；本文件只记录可追溯数值，不把未运行的
3pt、ratio、barematrix 或完整 TMD 链写成通过。

## 最终回归（2026-08-30）

```text
python examples/pyqcd/conftest.py: 42 passed, 0 failed
verify_manifest_4150.py: PASS 4/4
verify_4150_lowlevel.py: PASS 3/3
verify_4150_fermion.py: PASS 3/3
verify_4150_fermion_runner.py: PASS 12/12
verify_4150_hyp_ope_runner.py: PASS 3/3
verify_4150_momsmear.py: PASS 7/7
inspect_4150_momsmear.py: roots=7 groups=58 nopol pass=58 diff=0; polar pass=74 diff=42 unverified=58; exit=2 (预期)
verify_4150_effmass.py: PASS 3/3
inspect_4150_effmass.py: assets=7 pass=7 diff=0 unverified=0 rows=25
```

## 报告验收（2026-08-30）

`docs/report_donghx_4150_reproduction_20260830.tex` 已用 XeLaTeX 编译两遍，并对全部
渲染页完成视觉检查。正式 PDF 为
`docs/report_donghx_4150_reproduction_20260830.pdf`：27 页，16:9，页尺寸
`453.54 x 255.12 pt`；`Overfull=0`、`Float too large=0`、`Missing character=0`、
`Underfull=0`；`pages_actual=27` 与 `pages_rendered=27`。新增的极化对照页、effmass
聚合页、验收页、来源行和页脚均未见遮挡、裁切或越出安全区。
