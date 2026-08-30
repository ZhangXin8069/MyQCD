# 从零开始学习格点 QCD：梯度流核子胶子 TMD-PDF

这是一套面向高中毕业生的中文 16:9 Beamer 课程。课程从函数、向量、概率、经典场和量子力学讲起，逐步进入 QCD、Euclidean 路径积分、格点规范场、费米子、Monte Carlo、谱学、有限体积/有限温度、各种重整化方案，最后落实为梯度流方案下核子胶子 TMD-PDF 的可审计实现设计。

教学核心自包含，不要求读者用论文补齐定义或推导。论文图谱的作用是追溯研究证据、比较方案与训练阅读原文，而不是替代主课。

## 课程规模

- 35 卷，每卷 5 单元，共 175 个学习单元；
- 每单元固定 5 张教学 frame：物理图像、定义与公式、推导与证据、计算算法、练习与完整解答；
- 核心全集实际 1159 页，编译页数与 Ghostscript 实测一致；
- 6 份论文图谱收录 P01--P50，完整原始 PDF 共 1115 页，每篇恰好出现一次；
- 175 条课程级 SymPy 验证，加 26 个可修改的教学代码例题。

## 35 卷学习路线

| 阶段 | 卷 | 学习出口 |
|---|---|---|
| 数学与基础物理 | V01--V06 | 量纲、线性代数、Fourier、概率与数值、时空与场、量子力学、QFT |
| QCD、格点与测量基础 | V07--V12 | QCD、Euclidean 格点、费米子求解、Monte Carlo、核子关联与统计拟合 |
| 部分子与目标算符 | V13--V15 | collinear PDF、LaMET/quasi 分布、指定 gauge-link class 的胶子 TMD 算符 |
| 梯度流与端到端原型 | V16--V20 | 流时方案、断连核子测量、soft/重整化/匹配、联合极限与独立实现 |
| 群论与量子场论深化 | V21--V26 | 有限群、李群/李代数、粒子物理、QFT、规范量子化、非微扰结构 |
| 格点专题 | V27--V32 | 谱学、多强子/Lüscher、有限体积、有限温度、费米子方案、改进与尺度 |
| 研究级重整化与资格考核 | V33--V35 | 局域/非局域重整化、soft/rapidity/CS、联合极限和完整链审计 |

建议按卷顺序学习。每卷先做“先修诊断”，再完成五个单元；不能独立完成卷末练习时不要跳到下一阶段。V35 的通过标准不是“运行出一张图”，而是能说明每个中间对象、数组轴、方案、误差和停止门。

## 最终项目的准确边界

课程的主研究目标固定为自旋平均核子中的非极化胶子 `f_1^{g[-,-]}`；其他 future/past link class、螺旋度与线偏振通道均作为显式扩展。完整结果必须同时具备：非零横向间隔、有限 staple、含 `2E` 与 Euclidean projector 归一化的真实核子胶子三点、声明 Wilson 方向/regulator/zero-bin/转换核的 quasi-soft 与 rapidity 处理、胶子--singlet 匹配，以及 `a/L/Pz/tau/ell` 多尺度误差验证。梯度流只提供 UV 平滑和流方案；它不会自动消除 Wilson 线线性发散，也不会自动完成 soft subtraction 或 rapidity 重整化。

局域极限要求场端点和路径共同收缩；重整化 TMD 的 `b_T→0` 联系用 small-`b_T` OPE，而不是直接等同 collinear PDF。局域小流时展开也不能直接用于 finite-staple；缺少完整路径、端点、cusp 与 mixing 的转换核时，结果必须停在 finite-flow prototype。

证据状态只能依次升级：

```text
接口存在 → 受控测试通过 → 方案闭合 → 真实数据验证
```

缺少任一门时，产物应称为“接口骨架”“带 staple 的裸准关联函数”或“梯度流胶子 quasi-PDF 原型”，不能命名为完整 TMD-PDF 物理结果。

## 文件与稳定编号

| 路径 | 用途 |
|---|---|
| `content/` | 35 卷结构化内容的单一事实源 |
| `course_style.tex` | 统一视觉、编号、跳转与安全区 |
| `sympy_validation.py` | 与 175 单元一一对应的课程验收 |
| `myqcd/` | 26 个面向学习者的 SymPy 例题 |
| `paper_sources.json` | P01--P50 完整原始 PDF 的唯一路径、URL 与缓存哈希 |
| `build_course.py` | 同源生成和两遍 XeLaTeX 构建 |
| `verify_course.py` | 结构、来源、页数、日志和产物硬门 |
| `render_audit.py` | 43 份 PDF 的全页渲染、自动筛查与联系表生成 |
| `SOURCES.md` | book/paper/code/skill 的可追溯来源表 |
| `generated/` | 35 分卷、核心全集、索引、6 图谱及 manifest |
| `pdf/` | 通过构建闸门的最终 PDF |
| `visual_audit/` | 3489 个渲染页、57 张联系表和人工审阅记录 |

知识对象统一使用 `K/Def/Eq/Thm/Fig/Tbl/Alg/Ex/Sol/Src/SYM-卷.单元`。论文使用 `Pxx`，具体原始页使用 `Pxx-pyyy`。分卷与全集共享同一 frame 片段，合订时编号不变。

## 构建

SymPy 必须使用项目的 Conda `qcu` 环境：

```bash
cd docs/lattice_qcd_gluon_tmd_course
conda run -n qcu python sympy_validation.py
conda run -n qcu python myqcd/run_all.py --json generated/myqcd_examples.json
```

生成 43 份主 TeX、35 个共享片段、来源表和 manifest：

```bash
python build_course.py generate
```

分层编译；每份文档均运行两遍 XeLaTeX：

```bash
python build_course.py compile --target index
python build_course.py compile --target volumes --jobs 4
python build_course.py compile --target atlases --jobs 2
python build_course.py compile --target core
```

全量生成并编译也可使用：

```bash
python build_course.py all --target all --jobs 4
```

编译日志通过后，将全部 43 份 PDF 渲染为逐页图并生成 8×8 联系表：

```bash
conda run -n qcu python render_audit.py --jobs 4
```

必须逐张查看 `visual_audit/contact_sheets/` 中的全部联系表；只有连续覆盖所有页面，并核对自动标记的
疑点页之后，才能在 `visual_audit/manual_review.json` 中填写 `status=passed`、实际检查页数以及三个零缺陷
计数。`render_audit.py` 会对 43 份源 PDF、DPI 和联系表参数计算 SHA-256 审计指纹；源文件、页数、
渲染参数或联系表数有任何变化，旧人工记录都不会被升级为通过。

快速验收与严格验收：

```bash
conda run -n qcu python verify_course.py --run-sympy --check-paper-identities
conda run -n qcu python verify_course.py --run-sympy --check-paper-identities --require-pdfs \
  --json generated/course_verification.json
```

构建器拒绝 `Overfull`、`Float too large`、`Missing character`、未定义引用和实际页数不符。严格验收还
要求 `pages_expected=pages_rendered=pages_checked`、57 张联系表齐全、自动疑点为空，并且遮挡、裁切和
安全区越界计数均为零。未完成人工逐页检查时只能写“编译验收完成”，不能写“视觉验收完成”。

## 论文与代码来源

P01--P50 的书目信息来自 `refer/papers/INDEX.md`。40 份完整 PDF 直接读取 `../PyQCD`，其余 10 份为 arXiv 官方 PDF，保存在 `paper_cache/` 并固定 SHA-256。中文转排目录可用于术语对照，但因部分目录缺图，不作为论文图谱原文。

PyQCD 只作为接口和证据来源，本课程不会修改它。smoke/demo 只能证明形状和数据流；真实 GPU 求逆、真实系综三点函数和最终物理结果必须在相应硬件与数据上另行执行，并保留配置、日志、中间量和误差账本。
