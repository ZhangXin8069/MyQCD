# 格点 QCD 到梯度流核子胶子 TMD-PDF 课程实施计划

**目标：** 在 `docs/lattice_qcd_gluon_tmd_course/` 交付一套面向高中毕业生、无需外部补充资料、可长期自学并最终独立实现梯度流重整化核子胶子 TMD-PDF 的中文 16:9 Beamer/PDF 课程。

**架构：** 课程由 35 卷教学主线、6 卷论文原文图谱、一个核心全集和一个全局索引组成。教学主线采用同一套结构化内容数据生成，确保术语、公式、算法、练习和来源编号一致；论文图谱逐页纳入 50 篇完整原始 PDF，并赋予稳定的 `Pxx-pyyy` 页面 ID。构建器只依赖 Python 标准库、XeLaTeX、Ghostscript 和已登记的本地资料。

**技术栈：** Python 3.11、SymPy 1.14（Conda `qcu`）、XeLaTeX/ctexbeamer、TikZ、booktabs、tabularx、pgfplots、Ghostscript。

**规格：** 用户于 2026-08-30 提出的“从零基础到自主实现梯度流核子胶子 TMD-PDF 的千页级格点 QCD 入门 PPT”要求。

**全局约束：**

- 受众默认只有高中数学和物理经验；新概念先给直觉，再给定义和推导。
- 不以篇幅为压缩目标；核心推导、数值算法、验证门、练习与解答不得省略。
- 物理结论必须经过对称性、量纲、极限或独立数值检查中的至少一种验证。
- 区分“接口存在、测试通过、方案闭合、真实数据验证”四种证据状态。
- 不把梯度流 UV 平滑误写成 rapidity subtraction；不把直线 quasi-PDF 原型误写成完整 TMD。
- 不修改 MyQCD/PyQCD 既有源代码、paper/book 原文或系统配置；不提交、不推送。

## 文件职责

| 路径 | 职责 |
|---|---|
| `docs/lattice_qcd_gluon_tmd_course/README.md` | 学习路径、构建命令、编号和引用规则 |
| `docs/lattice_qcd_gluon_tmd_course/course_style.tex` | 16:9 主题、编号/跳转宏、安全区和统一视觉语义 |
| `docs/lattice_qcd_gluon_tmd_course/course_content.py` | 35 卷、175 个学习单元的稳定导入入口（正文按 `content/` 分卷） |
| `docs/lattice_qcd_gluon_tmd_course/build_course.py` | 生成核心分卷、核心全集、全局索引和论文图谱 TeX |
| `docs/lattice_qcd_gluon_tmd_course/sympy_validation.py` | 为每条主推导生成 `SYM-<EqID>` 可执行验证证据 |
| `docs/lattice_qcd_gluon_tmd_course/verify_course.py` | 清单、编号、引用、占位符、页数、日志和渲染验证 |
| `docs/lattice_qcd_gluon_tmd_course/render_audit.py` | 43 份 PDF 的 3489 页渲染、自动筛查和联系表生成 |
| `docs/lattice_qcd_gluon_tmd_course/visual_audit/` | 57 张联系表、逐页图和人工视觉验收记录 |
| `docs/lattice_qcd_gluon_tmd_course/myqcd/` | 26 个群论/QFT、谱学、重整化/TMD 的可运行 SymPy 教学例题 |
| `docs/lattice_qcd_gluon_tmd_course/paper_sources.json` | P01--P50 完整原始 PDF 的唯一路径、URL 与缓存哈希 |
| `docs/lattice_qcd_gluon_tmd_course/generated/` | 机械生成的 Beamer 源文件 |
| `docs/lattice_qcd_gluon_tmd_course/pdf/` | 编译后的核心分卷、全集、索引和论文图谱 PDF |
| `docs/lattice_qcd_gluon_tmd_course/SOURCES.md` | book/paper/代码/skill 的可追溯来源注册表 |

### Task 1：课程数据模型与统一编号

**消费：** 用户规格、MyQCD 公式注册表、PyQCD 共享约定与 TMD 六阶段链。

**产出：** `course_content.py` 中的 `Volume`/`Lesson` 数据；`course_style.tex` 中的 `K/Def/Eq/Thm/Fig/Tbl/Alg/Ex/Sol/Src` 锚点与跳转宏。

- [x] 定义 35 卷依赖顺序和每卷 5 个不可跳过的学习单元。
- [x] 每单元填写直觉图像、术语、主公式、逐步推导、可执行算法、边界检查、练习、解答和来源。
- [x] 每条主公式绑定唯一 `SYM-<EqID>`；复用 MyQCD 现有精确检查或在课程内补齐新的 SymPy 检查。
- [x] 每单元至少一张 TikZ 关系图，每卷至少一张带坐标/单位/图注的 PGFPlots 定量图；示意与实测严格区分。
- [x] 编号由卷号与单元号组成，分卷和全集编译时保持不变。
- [x] 验证 175 个单元 ID 唯一、先修关系无环、最终能力覆盖完整 TMD 六阶段。

### Task 2：教学主线生成与构建

**消费：** Task 1 的结构化内容与统一样式。

**产出：** 35 个核心分卷、核心全集和总索引的 `.tex/.pdf`。

- [x] 每个学习单元生成五张完整幻灯片：“为什么/图像”“定义/公式”“推导/检查”“算法/实现”“练习/解答”。
- [x] 推导页显示对应 SymPy 验证 ID、检查对象、适用假设与通过/结构性边界；失败项阻断构建。
- [x] 每卷增加路线图、先修检查、卷末能力清单和来源页。
- [x] 核心全集输入同一批 frame 源，避免分卷与全集内容漂移。
- [x] 两遍 XeLaTeX 编译并检查未定义引用、Overfull、Float too large 与 Missing character。

### Task 3：50 篇论文原文图谱

**消费：** `refer/papers/INDEX.md`、`../PyQCD/refer/{papers,books}` 的完整原始 PDF，以及课程缓存的 10 份 arXiv 官方 PDF。

**产出：** 6 个主题论文图谱 `.tex/.pdf`，每篇包含课程接口页和全部原文页面。

- [x] 解析 50 行索引，核对 arXiv/来源、SHA-256、PDF 存在性和 Ghostscript 实测页数（合计 1115 页）。
- [x] 按规范基础、梯度流、LaMET、重整化、胶子/TMD、采样六主题分卷。
- [x] 为每个原文页面赋予 `Pxx-pyyy`，不裁改原文内容；封面页解释与课程主线的关系和证据状态。
- [x] 核对索引声明页数与实际 PDF 页数；50 篇一篇不少、一页不少。

### Task 4：代码—物理映射与自主实现终章

**消费：** PyQCD 的 gradient flow、gluon OPE/TMD、disconnected ratio、Z_R/hybrid、Fourier/CS/matching、extrapolation、pipeline/infra/statistics 入口。

**产出：** 第 19–20 卷的接口契约、伪代码、数组形状、元数据、测试矩阵和生产清单。

- [x] 逐阶段给出物理对象 → 方程 → 离散几何 → 数组 → API → 不变量的双向映射。
- [x] 明确 `b_perp=0`、空 staple、单组态 disconnected、`soft=1` 和 smoke 图的降级措辞。
- [x] 给出从合成小格点测试到真实多系综运行的逐门停止条件。
- [x] 结课项目包含配置模式、产物目录、断点续跑、统计/系统误差账本和发布前审计。

### Task 5：全量验证与复查

**消费：** Tasks 1–4 的所有源和 PDF。

**产出：** 可复现验证摘要与干净的 Git diff。

- [x] `python3 -m py_compile` 检查构建器、内容和验证器。
- [x] 运行内容验证：卷数、单元数、核心页数、论文数、论文页数、ID 唯一、引用闭合、占位符为零。
- [x] 运行全部 SymPy 检查，要求 175/175 主推导和 26/26 教学例题均通过；不能由符号代数验证的物理假设单列为边界。
- [x] 对所有交付 PDF 两遍编译；硬溢出、缺字、未定义引用为零。
- [x] Ghostscript 核对 PDF 页数并渲染全部页面；用联系表和缩略图拼图逐页目测边界、遮挡和裁切。
- [x] 运行 MyQCD 既有公式审计作为课程公式证据回归；记录无法在本机执行的 PyQCD/GPU 路径。
- [x] 执行 `git diff --check`、`git diff --stat` 和目标目录定向复查，不暂存、不提交、不推送。

## 需求覆盖自审

| 用户要求 | 对应任务 |
|---|---|
| 面向零理论基础高中毕业生 | Task 1–2 的先修卷与五步教学模板 |
| 最终能自主实现目标计算 | Task 4 的端到端实现与结课项目 |
| 理论基础到实战、由浅入深 | 35 卷依赖序列与每单元推导/算法 |
| 无需补充其他参考资料 | 核心自包含 + Task 3 全文图谱 + SOURCES |
| 公式/定理/知识点/图表统一编排与跳转 | Task 1 的全局 ID 与核心全集 |
| 图文并茂、缺图自行补充 | Task 1–2 的单元关系图、卷级定量图和图注来源 |
| 推导需要 SymPy 验证 | Task 1、5 的 `SYM-<EqID>` 注册与全量回归 |
| 借鉴 paper/book、MyQCD/PyQCD/skills | Tasks 1、3、4 的来源链 |
| 千页级、不省略 | 核心实际 1159 页 + 1115 个论文原始页及 50 个接口页 |
| 精良可长期深度学习 | 分卷、索引、练习解答、验证器和稳定编号 |

占位符扫描目标为 0；路径、模块名与验证命令在实施时以当前仓库实测结果为准。
