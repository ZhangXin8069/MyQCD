# 外部 QCD 参考库吸收报告（2026-11-09）

## 范围与方法

- 目标：为 MyQCD 的「算符构建」与「费曼图构建/导出」补齐可执行能力，参考 GitHub 上高质量
  的 QCD 理论库与费曼图作图库。
- 调研方式：3 个并行子代理（QCD 理论库、作图库、现有子模块可吸收性）+ 主代理 GitHub API
  核验。其中现有子模块分析代理返回完整结果；两个外部检索代理因 GitHub 网络重试超时被终止，
  其候选由主代理用 GitHub API 与 `git ls-remote` 独立核验。
- 同步位置：`refer/git-rep/`，全部以上游固定提交的 Git 子模块形式只读引入。
- 约束：不复制上游源码；GPL-3.0 与无许可证内容只作 `reference-only`；实现均为 MyQCD
  独立重写，并在测试中断言数学恒等式。

## 新增参考子模块

| 子模块 | 上游 | 固定提交 | 许可 | 用途 | 处置 |
|---|---|---|---|---|---|
| `syhep` | <https://github.com/mardsouza/syhep> | `77d3d4861ef3556acdd1e3a757a6efbe6598428e` | GPL-3.0 | SymPy 高能物理符号计算、旋量代数 | reference-only |
| `RGBeta` | <https://github.com/aethomsen/RGBeta> | `946db15bdb489a772aa26272f527081708527920` | MIT | QCD/EFT 重整化群 beta 函数（Mathematica） | reference-only |
| `pyfeyn2` | <https://github.com/APN-Pucky/pyfeyn2> | `d5de3ea0f0dd929be800b8a5dd377f9fec7fa0cf` | GPL-3.0 | Python 费曼图绘制，含 TikZ/DOT/Mermaid 渲染器 | reference-only |
| `pyfeyngen` | <https://github.com/paulhenry46/pyfeyngen> | `530a357467944e53320ce72e3e4683cbb771f0d2` | MIT | 粒子语法 → TikZ-Feynman 代码生成 | reference-only |

既有子模块的许可与吸收边界：

| 子模块 | 固定提交 | 许可 | 结论 |
|---|---|---|---|
| `PyQCD` | `2e6c868f4573b50746acdc7ad9dad2d7af4e9a0a` | MIT | 事实源，只读引用 |
| `feyncalc` | `1ee480093293a01a82b3e365d026808f1d4e1c17` | GPL-3.0 | 只按数学恒等式重写，不复制代码 |
| `LQCD_Wickcontraction_reduce` | `033d607cdb753e98ddc6c26dff594f319d8406f2` | 无 LICENSE 文件 | 只按算法描述重写，不复制代码 |

## 吸收矩阵

| 来源与证据 | 正向价值 | MyQCD 缺口 | 处置 | 落点与验证 |
|---|---|---|---|---|
| `feyncalc/FeynCalc/Dirac/DiracTrace.m:645-653`（Hahn Trace4 递归） | 任意偶数 γ 链的迹闭式 | 无 Dirac 迹 | adapt | `myqcd/gamma.py:trace_gamma_product`；与显式 4×4 矩阵迹逐项对拍 |
| `feyncalc/FeynCalc/Dirac/DiracTrace.m:76,104,538`（`TraceOfOne`） | 迹归一化必须显式 | 约定不清 | adapt | `myqcd/gamma.py:SPINOR_DIM=4` 固定为 4，文档写明 |
| `feyncalc/FeynCalc/Dirac/DiracReduce.m:15-27`（SPVAT 基） | 长 γ 串约化到 5 类结构 | 无双线性基 | adapt | `myqcd/operators.py:dirac_bilinear_structures`（16 基）与 `decompose_dirac_bilinear` |
| `feyncalc/FeynCalc/SUN/SUNTrace.m:213-250` | SU(N) 迹闭式与长迹递归 | 无颜色代数 | adapt | `myqcd/color.py`；采用厄米归一化 `Tr[T^aT^b]=δ^{ab}/2` |
| `feyncalc/FeynCalc/SUN/SUNSimplify.m:506-556` | Cvitanović 颜色收缩与 Fierz | 颜色 Fierz 缺失 | adapt | `myqcd/color.py:color_fierz_tensor/color_fierz_residual`（残差精确为零） |
| `feyncalc/FeynCalc/SUN/SUNSimplify.m:585-619` | `f`/`d` 恒等式与 Casimir | 颜色不变量缺失 | adapt | `myqcd/color.py:structure_constants/symmetric_constants/casimir_*` |
| `feyncalc/FeynCalc/Dirac/DiracOrder.m:203-220` | 字典序规范化 | 长链规范化 | reference-only | 当前只支持 16 基分解与迹；未实现通用规范化 |
| `feyncalc/FeynCalc/Dirac/DiracTrick.m:105-125`（γ5 方案机） | NDR/Larin/BMHV | γ5 方案边界 | reference-only | 明确不做 D 维 γ5 方案；见证据边界 |
| `PyQCD/pyqcd/lattice/_gamma.py:1-103` | DR 基与 0..17 索引 | 与 PyQCD 对接 | adapt | `myqcd/gamma.py:gamma/gamma_matrices/gamma5`，索引逐一复刻 |
| `PyQCD/pyqcd/contraction/_baroperator.py:38-123` | `C=γ4γ2`、H/T/C 符号 | 无共轭/宇称符号 | adapt | `myqcd/gamma.py:charge_conjugation_matrix/gamma_properties/parity_sign` |
| `PyQCD/pyqcd/lattice/_gamma.py:266-296` | 双宇称投影 | 无投影器 | adapt | `myqcd/gamma.py:parity_projectors` |
| `LQCD_Wickcontraction_reduce/kernels/correlator_wick_normalizer.py:863-938` | Dirac 索引图：闭环取迹、开链取矩阵元 | 只有组合配对 | adapt | `myqcd/gamma.py:dirac_trace` + `myqcd/feynman.py` 图结构 |
| `LQCD_Wickcontraction_reduce/kernels/correlator_wick_normalizer.py:475-485` | 原场序 → 标准序的置换宇称 | 介子槽序隐患 | reference-only | 记录为风险；未改现有 `wick.fermion_fields` 语义 |
| `pyfeyn2/pyfeyn2/render/latex/tikzfeynman.py` | TikZ-Feynman 渲染 | 无图导出 | adapt | `myqcd/diagram_export.py:to_tikz`（零依赖字符串生成） |
| `pyfeyn2/pyfeyn2/render/latex/dot.py` | DOT 输出 | 无 Graphviz 导出 | adapt | `myqcd/diagram_export.py:to_dot` |
| `pyfeyngen/src/pyfeyngen/exporter.py:3` | 粒子图 → TikZ | 无语法/布局层 | adapt | `myqcd/feynman.py` 规则清单 + `diagram_export` |
| `syhep/src/syhep`（SymPy HEP） | 旋量代数与截面计算 | 旋量振幅未实现 | reference-only | 只作后续扩展参考 |
| `RGBeta/Package/TensorCalculations.m:15-26` | 重整化张量与 beta 函数 | 无 RGE 求解 | reference-only | 本库只做公式审计，不求解 beta 函数 |

## 拒绝与风险

| 项 | 处置 | 理由 |
|---|---|---|
| 复制 FeynCalc `.m` 代码 | reject | GPL-3.0 与 MyQCD MIT 不兼容 |
| 复制 LQCD_Wickcontraction_reduce 代码 | reject | 无 LICENSE，默认保留所有权利 |
| 复制 pyfeyn2 渲染器代码 | reject | GPL-3.0；只参考接口分层，独立实现字符串导出 |
| FeynArts 图生成 | reject | 不在 feyncalc 子模块内，且依赖 Mathematica 运行时 |
| 完整 γ5 方案机/圈积分 | reference-only | 超出当前「可执行公式审计」边界 |
| 介子 `(bar, q)` 槽序 | 风险记录 | 现有 `wick.fermion_fields` 先夸克后反夸克；调用方必须显式按物理序构造 |

## 颜色与 γ 基约定对照

- 新增 `myqcd/color.py` 使用厄米生成元 `T^a = λ^a/2`，`Tr[T^aT^b] = +δ^{ab}/2`。
- 既有 `myqcd/derivations.py:219-243,401` 使用 `T^a = iλ^a/2`，`tr(T^aT^b) = -δ^{ab}/2`。
- 两套约定不可混用；本报告与 `color.py` docstring 明确记录差异，后续若统一需单独迁移。
- 新增 `myqcd/gamma.py` 使用 PyQCD 的 DeGrand–Rossi 基（`gamma(0)=I` 哨兵，`gamma(4)=t`）；
  LQCD_Wickcontraction_reduce 使用另一套手征型基，跨库数值对拍必须先做基变换。

## 验证

- 定向测试：58 passed（gamma/color/operators/feynman/diagram_export/audit fallback/wick）。
- 全量测试：161 passed；11 failed 全部由 `refer/papers` 文献目录缺失引起，属环境缺口。
- `python -m myqcd.operator_audit`：26 项检查，`status=verified`，0 失败。
- `python -m myqcd`：缺 `refer/papers/INDEX.md` 时自动跳过清单，返回
  `verified_core_without_inventory`，核心检查仍执行。
- 新增测试覆盖：Clifford 代数、迹定理与显式矩阵对拍、16 基秩、C/H/T 关系、SU(3) 结构与
  Fierz 恒等式、Dirac 双线性分解往返、PyQCD 索引映射、Wick 图与圈数、TikZ/DOT/SVG 导出结构。

## 证据边界

本吸收不声称完成：D 维 γ5 方案、圈积分、图同构规范化、对称因子、真实系综收缩、
GPU 数值、RGE 求解或连续极限。`verified` 仅指上述精确代数与组合恒等式。
