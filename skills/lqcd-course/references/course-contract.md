# 格点 QCD 长课程验收合同

本参考在创建、扩展、全量编译或审查课程时读取；普通单页措辞修订不必加载。

## 课程固定结构

- 35 卷，每卷 5 单元，共 175 单元。
- 每单元生成 5 个教学 frame；每卷另有标题/路线、先修诊断、卷级定量图、能力清单和来源。
- 核心全集必须超过 1000 个实际 PDF 页面；论文图谱页数另计，不可用于填充核心页数。
- 论文库固定解析 P01--P50；`refer/papers/INDEX.md` 提供书目，`paper_sources.json` 唯一指定完整原始 PDF、
  官方 URL/缓存、页数与 SHA-256，六册图谱中每篇恰好出现一次。
- SymPy 证据包含 175 条课程验收和 `myqcd/` 下 26 个教学例题；两套结果分别汇总、分别执行。

## 35 卷依赖主线

1. V01--V06：数学语言、线性代数与对称性、Fourier/概率/数值、时空与场、量子力学、量子场论。
2. V07--V12：QCD 规范理论、Euclidean 格点规范场、格点费米子与求解器、Monte Carlo 系综、强子关联函数、统计拟合。
3. V13--V15：部分子分布、LaMET/quasi 分布、胶子 TMD 非局域算符与投影。
4. V16--V20：梯度流、真实断连核子测量、soft/重整化/匹配、联合极限与独立端到端实现。
5. V21--V26：有限群、李群、粒子物理、QFT、规范量子化、非微扰场论。
6. V27--V32：谱学、多强子、有限体积、有限温度、费米子方案、改进/边界/尺度。
7. V33--V35：局域与非局域重整化、研究级联合设计、最终资格考核。

## 每单元内容合同

| 对象 | 最低完整性 |
|---|---|
| 物理图 | 三节点因果/计算关系；说明是示意还是数据 |
| 定义 | 至少 3 项，符号、单位和约定不含混 |
| 主公式 | 一条稳定 Eq ID；给物理含义、适用条件和极限 |
| 推导 | 至少 3 个可复核转移；不跳过决定符号/归一化的步骤 |
| 算法 | 至少 4 步；输入、状态、计算、停止/验证、输出闭合 |
| 检查 | 至少 2 项，优先对称性、量纲、自由/退化极限与独立实现 |
| 练习 | 能检验本节出口；同页或下一固定页给完整解答 |
| 来源 | book/paper/code/skill 至少一项；自编补足要明确标注 |
| SymPy | `SYM-<lesson>` 一条；记录假设、通过项和不可验证边界 |

## PDF 硬闸门

1. XeLaTeX 两遍成功，PDF 非空且可由 `pdftotext` 提取主要文字。
2. `Overfull=0`、`Float too large=0`、`Missing character=0`、未定义引用为 0。
3. 每份 PDF 的编译记录必须绑定当前 TeX、样式、片段与论文原文输入指纹，同时绑定 PDF/日志哈希和
   两遍 XeLaTeX 状态；源变化但页数不变时旧 PDF 也必须失败。
4. `pages_expected=pages_actual=pages_rendered=pages_checked`；全页检查不是抽查。
5. `occlusion_pairs=0`、`clipped_objects=0`、`outside_safe_area=0` 只能在视觉证据支持时填写。
6. 主体文字保持投影可读；不使用 `tiny` 或整体缩放承载主信息。
7. 当前 43 份主 PDF 应生成 57 张 8×8 联系表；活动根目录固定为 `visual_audit/`，render schema 固定为
   `lattice-qcd-course-render-audit-v2`。必须逐张连续审阅；自动筛查无异常不能替代人工检查。外部与
   内嵌人工记录必须共享 manual schema、status、SHA-256 审计指纹、页数、联系表数和三类缺陷计数；
   PDF、页数、参数或联系表变化后立即失效。旧 render 版本只可归档，不得作为活动输入。
8. 生成片段中的空根号占位和字面 `\textasciicircum{}` 必须为零；根号参数、上标组与显式下标组需由
   序列化器回归用例验证，避免“版式通过但公式语义错误”。
9. 严格验收必须现场重跑两层 SymPy，并核对精确 ID/lesson/check/assumption/boundary 集合；缓存 JSON 需
   绑定脚本、SymPy 版本、结构化课程指纹、本次运行时间、严格模式开关以及活动视觉 schema/指纹，`0/0`、
   任意伪造 ID、旧失败快照或不同视觉指纹的通过快照一律不得作为当前证据。
10. 每页渲染图和每张联系表记录唯一预期路径、尺寸与 SHA-256；审计指纹还绑定 Ghostscript 版本、命令、
    DPI 和 8×8 网格。只核对页数或重复使用同一张图不得通过。

## 研究终点停止条件

主目标固定为自旋平均核子中的非极化胶子 `f_1^{g[-,-]}`；其他 link class、胶子螺旋度和线偏振通道
作为显式扩展，不得混作同一分布。最终项目必须能从配置出发生成可审计的中间产物：flowed links、
Clover/dual field、指定 future/past gauge link 的 finite-staple gluon operator、含 `2E` 与 Euclidean
projector 归一化的逐组态 C2/loop/C2×loop、`1/(N-1)` 无偏协方差、共享重采样、声明 `v/vbar`、
rapidity regulator、zero-bin 和 quasi-to-standard 核的 soft/Z/ratio/hybrid、Fourier、共同 `x` 或
共同 Ioffe time 且至少三个有效 `Pz` 的 CS kernel、胶子--singlet matching、`a/L/Pz/tau/ell` 外推和
误差账本。

局域极限要求端点及路径共同收缩；`b_T→0` 与 collinear PDF 的物理联系使用 small-`b_T` OPE。局域
SFTE 不得直接外推 finite-staple：缺少依赖 `z,b_T,ell,sqrt(8tau)`、端点、cusp 与 mixing 的 `C_Gamma`
时停在 finite-flow prototype。合法窗口还要求整条路径及端点到源、汇和最近时间边界（扣除源汇
smearing 支撑）的最短距离满足 `a << sqrt(8tau) << d_Gamma`；周期边界另查绕回，开放边界另查边界
污染。任一层缺证据就停在相应状态，不跨门命名为完整物理结果。
