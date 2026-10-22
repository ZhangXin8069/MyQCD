# dev20 以来外来内容吸收与胶子 TMD-PDF 审计

日期：2026-10-22（Asia/Shanghai）  
身份：`{物理+代码}`  
范围：`dev20..HEAD`、`refer/donghx/**`，重点
`refer/donghx/_Gradient_Flow_GluonPDF/`；`refer/git-rep/**` 只作来源与固定
OID 证据，不审计其内部实现。

## 结论

本轮已完成可证明的代码纠错、缓存契约升级、物理失败关闭和真实 conf6250
smoke。以下事项有明确实现与测试证据：

- 拒绝把源平均 C2 当作 TMD 物理输入；新增 `(source,dt)` 源分辨 strict cache。
- 每个 bootstrap/jackknife replica 内重算 ensemble 真空协方差，并保存共享索引。
- 修正 `corr3=None` 解析路径缺少 `Nconf` 归一化的 critical 错误；旧的
  ratio/c0/Sumratio 数值全部撤回并仅从缓存重跑分析层。
- full-sample central fit 与 replica uncertainty 分开。
- 可辨识性、拟合质量、plateau 平坦度和物理支持状态分开。
- helicity 复数 `nopol` 分母、物理 `T_H-S_H` 选择、复数 Fourier 约定、
  未测量 λ 外推和软因子实正域均已改为显式 fail-closed。
- 局域 spin-2 使用独立 Ioffe-time 变换，不再重复 `quasi_tmd_pdf` 的 Fourier 归一化。
- 匹配的卷积 `y` 支撑扩展到 `[-3,3]`，输出 `x` 支撑与输入 `y` 支撑分离。
- CS 比值采用文档定义的 `ln|R|`，允许统计符号翻转。
- gauge 文件 SHA-256 进入 flow/OPE strict contract。

当前仍不能给出物理胶子 TMD-PDF。缺少同几何 soft/rapidity、胶子-夸克混合、
多个流时、多个格距和受控连续极限；现有单格距 L24x72 数据最多支持诊断链。

## 来源与范围

`dev20` annotated tag 的对象为 `519ef9c`，其提交为
`3d528be28ca60d2581b50a43ae3704afb5061e85`。审计起点 HEAD 为
`3e1edd4f9d9eadd3ea07dfc47e4e92cd2fc6c0b9`。

严格 `dev20..HEAD` 有 9 个外来候选：1 个 docs、4 个 logs、4 个 gitlink。
拼音参考树在该区间无路径变化。重点目录实际由 `fc3a7c9` 导入，包含 181
个文件、4,460,308 字节；目录没有上游 URL、固定 commit 或 LICENSE，
所以只能 `reference-only`，不能把源码直接复制进生产包。

完整来源与处置矩阵见：

- `data/runs/agent-reports/provenance.md`
- `data/runs/absorb/dev20-20261022-014335/inventory.json`
- `data/runs/agent-reports/public-data.md`
- `data/runs/agent-reports/statistics-fit.md`
- `data/runs/agent-reports/extraction-matching.md`
- `data/runs/agent-reports/operator-geometry.md`
- `data/runs/agent-reports/donghx-content.md`
- `data/runs/agent-reports/flow-window-scan.md`

补充只读审计（本轮子 agent，结论已在本地复核）：

- Donghx 顶层源码/结果来源：`copy.sh` 只记录集群绝对路径，工作树没有
  上游 commit、manifest 或 LICENSE；`fc3a7c9` 同时删除了旧顶层
  `Operator.py`、`2pt_proton_*.py` 等文件。旧文档中的“完整可交付”叙述
  不能作为当前可重放证据。
- 非重点源码：LIME 记录解析、flow 步长默认值、缓存算法版本和
  `fm_to_GeV` 常数仍存在残余风险，已列入下方“仍未闭合”。
- Pz=0：独立复核确认了 `corr3=None` 的 `Nconf` 归一化错误；修复后
  10 组态 P000 代表点恢复为解析值 `-1.12093`，扩展到 11 组态后为
  `-1.13110`；严格质量门仍失败。

## 核心修复

### 源分辨 C2 与 ensemble ratio

原生产缓存只保存 `C2(dt)=mean_source C2(source,dt)`，分析层又把该源平均量
当成绝对时间序列二次 `roll`。这既丢失源轴信息，也能制造非零 ratio。

现实现：

- `pyqcd/pipeline/_steps.py:985`：新增 `source_resolved=True`，保存
  `C2[source,dt]`，每个源不再除以 `NT`。
- `pyqcd/pipeline/_tmd9.py:507`：source-resolved 2pt 使用独立 v2 contract，
  shape `(NT,NT)`，显式记录 `source_axis_order="source,dt"`。
- `pyqcd/analysis/_disconnected.py:100`：生成一次共享重采样索引。
- `pyqcd/analysis/_disconnected.py:117`：在每个 replica 内计算
  `mean(C2*O)-mean(C2)mean(O)`，再除以 `mean(Re C2)`。
- `pyqcd/analysis/_tmd_ratio.py:211`：TMD 入口拒绝一维源平均 C2。

已知一维旧缓存无法物理修复为源分辨数据，只能重新计算；本轮没有对其做
静默广播或兼容猜测。

### ensemble covariance 归一化 critical 修复

`pyqcd/analysis/_disconnected.py` 的 `corr3=None` 路径先对
`C2×OPE` 做 `configuration × source` 求和，却只除了 `n_source`；随后
`c2_mean`/`op_mean` 又按 configuration 与 source 双重平均。解析反例
`C2=[1,3]`、`OPE=[2,6]` 因此从正确值 `1` 错成 `6`。

现实现改为除以 `n_source * len(selected)`，并新增
`test_analytic_corr3_path_uses_ensemble_mean_normalization`。修复后真实
P000 的 `(T,tau,z,b)=(8,4,0,0)` 从旧产物 `-21.61751` 恢复为
`-1.12093`（10 组态），与独立解析重算一致；加入 conf4150 后的 11 组态
值为 `-1.13110`。所有修复前的 ratio/c0/Sumratio 数值均作废；当前产物已
仅用 strict 2pt/OPE 缓存重新生成。

### 统计状态与 full-sample fit

- `pyqcd/analysis/_fitter.py:899`：新增 full-sample central fit，使用 replica
  covariance，但中心值不再复制某个任意 replica。
- 新增 `pyqcd/analysis/_bare_sumratio.py`：实现物理 `Tmin=floor(0.6fm/a)+1`、
  forward Sumratio-difference、同 cut 内 omission-penalized AIC、逐 replica
  quality/fallback 选择及 `M_quality`/`M_filled` 分栏。
- `pyqcd/analysis/_tmd_ratio.py:101`：plateau 数据可辨识性、常数平台质量、
  物理支持状态分层保存。
- TMD 拟合报告明确标注“last successful replica fit”，并另列 central fit。
- artifact 保存 seed、共享 indices、index SHA-256、组态 ID、SVD/rank、
  finite fraction、median `chi2/dof`、quality 和 physical status。
- `configuration_ratio` 及把 factorized C3 再减一次 `C2*O` 的路径已禁用。
- `fit_ZR` 在无正自由度、非有限代价或优化器失败时抛错；`fit_ZR_samples`
  将坏样本写 NaN，并保留 usable/partial/unusable 状态。

### Fourier 与局域 spin-2

参考物理归一化为：

```text
H(z) = -2 R_MS(z) / [4 pi alpha_s(aE)]
Q(x) = (1/pi) integral_0^infinity dlambda cos(x lambda) H(lambda)
```

- `pyqcd/renorm/_tmdextract.py:185` 新增 `ioffe_time_distribution`，直接积分
  `H(lambda)`，只使用 `1/pi`。
- `quasi_tmd_pdf` 继续保留其自身 `1/(2 pi Pz) * Pz^2/Pt^2` 约定，两者不再混用。
- Gaussian 解析 Fourier oracle 验证了幅度与指数宽度，而不是只检查有限性。
- `z=0` 使用严格一圈局域 spin-2 inverse，不沿用非局域 endpoint 公式。

### CS 与 NLO/gg-only 匹配

- `pyqcd/renorm/_tmdextract.py:284` 的 CS 比值改为 `ln|R|`。
- 工作流在满足 `sqrt(8 tau)<z` 的首个代表点提取 CS，不再固定 `z_ref=1`。
- 匹配输出 `x` 与卷积输入 `y` 分开；工作流使用 `x∈[-0.98,0.98]`、
  `y∈[-3,3]`，并在 `|x|<0.02` 处不发布结果。
- `scheme_c0_coefficient` 和 `apply_scheme_c0_correction` 接入
  `q_hybrid=q_MS-g F[c0*h]`；`c0(0)=0`，其余点使用
  `5/6 log(z_eff²μ²e^{2γE}/4)+3/2`。
- rapidity 因子 `zeta_z=(2|y|Pz)^2` 作用于卷积输入 `y*g(y)`，不再误按输出 `x` 索引。
- 端点转换、绝对归一化和匹配使用同一固定 `alpha_s=0.25` 与同一格距。
- 由于没有 soft/rapidity 测量和 g/q mixing，matching 永远保持
  `physical_acceptance=false`。

### 缓存与 provenance

- strict cache 继续使用 canonical JSON、SHA-256、唯一 `data` dataset、
  shape/dtype/finite 和原子发布。
- `pyqcd/operator/_gluon_ope.py` 的 ILDG reader 已改为严格遍历 LIME
  record magic、64-bit length、128-byte type 与
  `ildg-binary-data` payload byte count；不再用首链接幺正性搜索 ±16 KiB
  偏移。合成 LIME 容器与真实 conf6250 读取均通过。
- `pyqcd/pipeline/_tmd9.py:386` 对真实 gauge 文件计算流式 SHA-256。
- flow contract 绑定 gauge 内容；OPE contract 再绑定 flow contract SHA。
- `pyqcd/testing/tmd/pdf_workflow.py:117` 输出 `data_provenance.json`，
  记录输入路径、大小、mtime、gauge SHA 及所用 cache contract。

## 真实数据 smoke

数据：`/public` 的 beta6.20 L24x72 conf6250。

### 源分辨 2pt

- 输出 shape：`(72,72)`，dtype `float64`，全有限。
- CPU/Torch complex64 计算时间：约 276 秒。
- contract：`pyqcd.pipeline.multi-2pt.v2-source-resolved`。
- `C2(source,0)` 的源间 spread 约 0.0757，证明源轴不是可丢弃的重复信息。
- 运行目录：`data/runs/tmd-source-resolved-conf6250-v2/`。

### Flow 与 OPE

- Wilson flow `tau=3`：238 秒；Clover `E(t=0)=2.2867`，`E(t=3)=0.0453`。
- TMD OPE `(13,5,72)`：46 秒，shape/dtype/finite 全通过。
- OPE contract 含 `flow_contract_sha256`，其值为
  `7cc528eb152d53eac90386137b7c55c3d51f428beb388d65b6703d048599151c`。
- gauge SHA-256：`e68a9c1f55f03a14955da431a496ec775c3c20c179544a3e60ce9975544bc861`。
- 运行目录：`data/runs/tmd-source-ope-conf6250-v3/`。

### 物理状态

conf6250 是单组态。严格链路输出：

- `Nsample=1`，ratio 样本和 c0 plateau 为 NaN。
- `fit_status=statistically_unidentifiable`。
- `chain_status=diagnostic_only`。
- `physical_acceptance=false`。
- 未生成任何 `diagnostic_*tmd_pdf*` 数值，因为 plateau quality gate 未通过。

这是正确失败关闭，不是计算失败。只有完整多组态源分辨 C2 重新计算后，
ratio/plateau 才具备统计输入。

## `refer/donghx/**` 其他内容

- `refer/donghx` 只能作为无上游固定版本、无许可证的只读历史快照；
  `copy.sh` 的来源是集群绝对路径，不能替代 URL/commit 证明。
- `AGENTS.md` 与 `docs/AGENTS.md` 仍引用已不在工作树的旧顶层源码；
  `donghx_code_analysis` 和 `pure_gluon_ope_distillation` 是历史/AI
  派生阅读材料，不是独立数值验证。
- `_codex/Markdown` 是日期化交接记录，可吸收流窗口、统计契约、状态分层
  和 line-mass/SFTE 边界，但其 `/public` 路径和当前运行状态不可复用。
- `fit_bare` 技能明确要求保存 `M_quality`、`selected_available`、
  fallback 状态和共享 bootstrap 索引；本轮 `_bare_sumratio.py` 已按此
  契约实现。
- `Note/Gradient_Flow/main.tex` 是最新权威约定：非极化 `T_U-S_U`、螺旋度
  `T_H-S_H`；`T+S` 仅保留 legacy diagnostic。
- 该文档要求在物理外推中满足 `a << r_flow << |z|, Lambda_QCD^-1` 且
  `Pz r_flow << 1`。当前 `tau=3` 的 `r_flow/a=sqrt(24)=4.899`，绝大多数
  小 z 点不满足，因此本轮只允许 diagnostic。
- `Note/Quark_PDF/quark_pdf_note.tex` 是夸克 channel 的 Fourier/matching
  convention 参考，不能替代胶子 soft/rapidity 与混合矩阵。
- `basis_vertex_weights_20261015.md` 等文档明确存在跨时间随机权重 A/B
  差异及未解决的联合分布问题；本轮没有在缺少原始 basis/perambulator
  provenance 时把任一方案宣称为无偏。
- `_Gradient_Flow_GluonPDF/NO_Z0_NORMALIZATION.md` 明确禁止把 `M(0)` 当作
  绝对 PDF 幅度或替代 `Pz=0` hybrid 分母。
- 旧结果文档中“可交付 PDF”的叙述与当前 soft/rapidity、gg-only、单 a/单 tau
  状态冲突，不能作为本轮物理验收依据。

## Pz=0 hybrid 分母专项结果

本轮已把 P000 正式接入分析阶段，产物位于
`data/runs/tmd-production-10conf/analysis/tmd_ratio/`：

- `sumratio_difference_P000.npz`：修复后的零动量 Sumratio-difference。
- `zero_momentum_denominator_status.json`：逐点质量、central/replica
  fallback 与 `used_for_pdf=false` 状态。
- `diagnostic_c0_tmd_proton_P000.png` 等图只作诊断，不是 hybrid 归一。

修复归一化后，先重跑 10 组态；随后加入第 11 个可用组态 conf4150。当前
11 组态、1000 个 bootstrap replica 的结果为：

```text
P000 Sumratio quality: 52/65; central fallback 13; replica fallback mean 1.46%
P200 Sumratio quality: 51/65; central fallback 14; replica fallback mean 1.23%
P400 Sumratio quality: 65/65; central fallback 0;  replica fallback mean 0.12%
```

严格 loader 要求所有 65 点通过且所有 replica 无 fallback，因此仍拒绝
进入 `tmd_renormalize_hybrid`/Z_R。P000 失败点主要由
`candidate_bootstrap_success_fraction < 0.90` 引起；这不是归一化错误，
也不是可以靠把 `M_filled` 当物理值绕过的问题。当前 `chain_status` 明确为
`diagnostic_only`、`physical_acceptance=false`，并同时记录
`zero_momentum_denominator_quality_gate_failed` 与
`flow_step_size_above_reference_0p01`、
`flow_radius_not_smaller_than_all_nonzero_b`。

因此，`Pz=0` 分母已具备可重放诊断和 fail-closed 状态，但没有通过物理
hybrid 接入门；Z_R 仍没有同方案、多格距产物，不能声称已闭合。

## 受控 flow-window 扫描

为避免继续用 tau=3 的无效 b 窗口做表面统计，新增可复现入口
`pyqcd.testing.tmd.flow_window_scan`，并计算两个满足
`sqrt(8 tau) < z,b` 的诊断：

- 共同输入：11 组态，`z/a=0,3..12`，`b/a=3,4`，1000 bootstrap。
- `tau=0.5`（`r_flow/a=2`）：P000 quality `17/22`、P200 `18/22`、
  P400 `22/22`；P400 replica fallback 均值 `0.064%`。
- `tau=1.0`（`r_flow/a=2.828`）：P000 quality `14/22`、P200 `17/22`、
  P400 `22/22`；P000 replica fallback 均值 `6.82%`。

该扫描证明 P400 中心质量在两个 flow time 下稳定，但 P000/P200 仍有真实
flow-time/统计敏感性；P400 也仍有非零 replica fallback。两点不是
`tau→0` 外推，不能用来挑选“更好看”的流时，也不能升级为物理 PDF。
完整记录见 `data/runs/agent-reports/flow-window-scan.md`。

## 仍未闭合

- 同流时、同 staple 几何、同表示的 soft/rapidity 测量。
- 胶子-夸克 singlet mixing 的完整 `Z_ij` 矩阵及夸克 TMD 输入。
- 至少两个受控 `Pz`、多个 `tau`、多个 `a` 和 `ell` 扫描。
- 当前 `tau=3` 的 `r_flow/a=sqrt(24)=4.899`，`B_LIST=0..4` 中所有非零
  `b` 都满足不了 `r_flow < b`；同一流时下 `z=1..4` 也不满足
  `r_flow < z`。因此现有 `b⊥`/小 `z` 输入不能作为受控 SFTE 物理输入，
  只能作诊断。要得到物理 TMD，必须降低流时并显式选择满足窗口的 `b`，
  或增加更大的横向分离。
- Fourier 大 `lambda` 尾部模型与 `x→0`、`x→1` 系统误差。
- 10 组态以上的源分辨 C2/OPE 重算及真实 ratio/plateau 质量。
- `refer/donghx` 上游 URL、固定 commit 和许可证。
- 当前生产运行使用 `eps=0.05`，而参考冻结口径为 `eps=0.01`；状态中已记录
  `flow_step_size_above_reference_0p01`，但尚未做步长收敛重算。
- `fm_to_GeV=0.197`（ensemble 表）与梯度流绝对归一化使用的
  `0.1973269804` 仍有约 0.17% 差异，需要统一为单一常量或明确命名历史分支。
- flow/OPE cache contract 仍使用静态 `v1` 算法字符串；源码语义哈希/版本
  bump 尚未纳入缓存契约，旧缓存复用仍需人工审计。
- Pz=0 分母、Z_R 和 gluon-quark mixing 均未通过严格物理门；当前只能保留
  `unverified`。

因此最终物理判定为：实现与诊断链已显著纠错并完成真实 smoke；完整胶子
TMD-PDF 物理结果仍为 `unverified/blocked by missing multi-scale and
soft/mixing data`，不得发布为最终 PDF。

## 最终验证

```text
python -m pyqcd.testing
112 passed, 0 skipped, 0 failed

python -m py_compile <全部本轮修改 Python 文件>
exit=0

bash skills/form/scripts/form-audit.sh
PASS form-audit(pyqcd): registered exceptions=1147 unexpected=0

git diff --check
exit=0

严格 LIME：合成容器读回与真实 conf6250 的 573 MB 容器读取均通过。
```

当前 11 组态链的定向验证：

```text
python -B -m pyqcd.testing.tmd.verify_pdf_workflow \
  --skip-flow --allow-partial data/runs/tmd-production-10conf

[B] C2 ordering PASS
[C] 11/11 OPE shape/finite PASS
[D] P000=52/65, P200=51/65, P400=65/65, Nsample=1000 PASS
[E] PARTIAL: no physical PDF
最终：PARTIAL，严格质量与 flow-window 门未通过
```

真实 conf6250 自洽性验证：

```text
python -B -m pyqcd.testing.tmd.verify_pdf_workflow \
  --skip-flow --allow-partial data/runs/tmd-source-ope-conf6250-v3

[B] source-resolved P200 PASS
[C] TMD OPE shape/finite PASS
[D] single-configuration ratio PARTIAL, fail-closed
[E] no physical PDF artifacts, correctly PARTIAL
最终：PARTIAL，scoped 输入不足以声明物理 PDF
```

### 两真实组态扩展

以下两真实组态数字是 2026-10-22 早期归一化修复前的历史快照，仅说明当时
strict 流程能在小样本上失败关闭；修复后的可信结果以“十真实组态诊断链”
和 P000 专项表为准。

6250/6450 三动量源分辨 2pt、flow 和带 gauge/flow SHA 的 OPE 已写入
`data/runs/tmd-production-10conf/`。统一分析得到：

```text
P000>P200>P400 source-resolved C2 ordering: PASS
P200 sumratio quality/coverage: 32/65
P400 sumratio quality/coverage: 30/65
ratio arrays: (200,20,20,13,5), finite
replica fallback fraction: about 0.51/0.54
PDF chain: skipped; no physical PDF artifacts
```

该结果说明新 Sumratio/AIC 实现能在真实数据上给出有限候选，但 Nconf=2
时 fallback 比例和协方差 rank 不足，不能把有限数值误写成物理矩阵元。

### 十一真实组态诊断链

当前可用的 11 个 L24x72 组态（4150、6250–8050 生产集）的 P000/P200/P400
源分辨 2pt 与 OPE 已全部生成于 `data/runs/tmd-production-10conf/`。目录名
保留历史标识，实际现含 11 组态。统一验证结果：

```text
C2(0) ordering: P000 0.6299 > P200 0.2723 > P400 0.0242
group spread: 1.9% / 1.9% / 2.1%
OPE: 11/11 shape (13,5,72), finite
ratio: P200/P400 shape (1000,20,20,13,5), finite
Sumratio quality: P000 52/65, P200 51/65, P400 65/65
replica fallback fraction: P000 1.46%, P200 1.23%, P400 0.12%
bootstrap replicas: 1000
PDF: skipped by strict quality/coverage gate
```

200 个 replica 时曾得到 P000 `54/65`、P200 `56/65`，但提高到参考量级的
1000 replica 后降为 `52/65`、`51/65`；这说明先前较小 bootstrap 的通过数
偏乐观，不能作为质量提升。P400 central quality 全通过，但 replica fallback
仍非零。严格 loader 因此继续拒绝进入 hybrid/Z_R。该行为是有意设计，
不能把 `M_filled` 覆盖当成物理质量。
