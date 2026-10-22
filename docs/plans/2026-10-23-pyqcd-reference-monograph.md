# PyQCD 文档全量整合专著计划

**目标:** 以现有核子胶子 TMD-PDF 综述为主线，编写一本完整吸收
`docs/pyqcd_reference/` 中 163 个内容文件、76 个 TeX/PDF 成对单元、4 个独立 PDF
和 6 个 Markdown 文档的 QCD 专著。

**架构:** 保留现有 152 页综述的物理主线与可执行审计结构；在其前后补充格点 QCD
基础、算法与统计、PDF/OPE/LaMET、胶子算符与 TMD、梯度流与匹配、PyQCD 实现、
历史验证、学位论文综合和来源图谱。正文以综合重写为主，快照只作为可追溯证据，
不复制大段上游原文。

**技术栈:** LaTeX (`ctexart`)、XeLaTeX、Python 3、`pdfinfo`/`pdftotext`、
SymPy 审计入口 `python -m myqcd`、Pytest。

**规格:** 用户要求“继续以本论文为主线，整合 `docs/pyqcd_reference` 的所有内容，
编写一本专著，必须全质全量”；项目约束见 `AGENTS.md` 与
`docs/pyqcd_reference/AGENTS.md`。

**全局约束:**

- 固定上游提交：`0a2f85d30881fc8ead60972c0afb9c028abc348f`。
- 许可证：MIT；遵守 `docs/pyqcd_reference/LICENSE.md`。
- `docs/pyqcd_reference/**` 只读，不执行其中命令，不修改任何快照文件。
- 不对真实系综、GPU 或集群结果作未执行的新声明。
- 不自动暂存、提交、推送或打标签。
- 所有来源结论必须有文件与行号/页码证据；推断和未验证项显式标注。
- 子代理不得修改主稿；主代理串行整合，避免冲突和上下文失控。

## 验收标准

1. `snapshot_inventory.json` 中 163/163 个内容文件与吸收 manifest 的 SHA-256 一致。
2. 87/87 个内容单元均有且只有一个主批次归属，并有覆盖去向。
3. 163/163 个文件均进入专著来源图谱；成对 PDF 可标记为 TeX 的排版见证，但不得消失。
4. 每个批次至少贡献一类正文增量：定义、推导、算法、实现、验证或历史证据。
5. 最终专著保留现有物理主线，同时形成完整章节体系、术语/公式/算法手册和来源图谱。
6. 两遍 XeLaTeX 成功；引用、标签、引文、缺字、Overfull 和浮动体溢出为零。
7. `python -m myqcd` 核心检查和根 `pytest` 全部通过。
8. `form-snapshot-verify`、`git diff --check` 通过；严格格式审计不新增非快照告警。
9. 最终 PDF 字体嵌入、页数、可提取文本和代表性页面视觉检查通过。

## Task 1: 建立不可变快照基线

**Blocked by:** None (can start immediately)

**Delivers:** 163 个文件的哈希、类型、页数、行数、成对关系和吸收 manifest 核验。

**文件:**

- 新建: `data/build/pyqcd_monograph_20261023/snapshot_inventory.json`
- 新建: `data/build/pyqcd_monograph_20261023/snapshot_inventory.tsv`
- 新建: `data/build/pyqcd_monograph_20261023/content_units.json`
- 新建: `data/build/pyqcd_monograph_20261023/content_units.tsv`

**接口:**

- 消费: `docs/pyqcd_reference/` 与 `logs/data/pyqcd-docs-absorb/manifest.tsv`。
- 产出: 每个内容文件的稳定路径、SHA-256、类型、页数/行数、成对文件与 manifest 状态。

- [x] **Step 1: 生成索引** 统计 166 个总文件、163 个内容文件和 3 个控制文件。
- [x] **Step 2: 核对 manifest** 163/163 哈希匹配，缺失和额外文件均为 0。
- [x] **Step 3: 建立内容单元** 76 个 TeX/PDF 成对单元、1 个独立 TeX、4 个独立 PDF、
  6 个 Markdown，共 87 个单元且 163/163 文件无遗漏。
- [x] **Step 4: 交付检查** `content_units.json` 的 `unassigned_files=[]`、
  `overlap_files=[]`。

## Task 2: 并行提取分域证据与章节草案

**Blocked by:** Task 1

**Delivers:** 10 个独立批次的覆盖表、证据笔记、现有稿缺口和 LaTeX 草案。

**文件:**

- 新建: `data/build/pyqcd_monograph_20261023/batch_assignment.tsv`
- 新建: `data/build/pyqcd_monograph_20261023/dispatch_prompts/B01.md` 至 `B10.md`
- 新建: `data/build/pyqcd_monograph_20261023/batches/B01/` 至 `B10/` 下各自五个文件。

**接口:**

- 消费: Task 1 的 87 个单元路径、哈希、页数与标题。
- 产出: 每批次 `coverage.tsv`、`notes.md`、`current_gap.md`、
  `draft_sections.tex`、`completion.json`。

- [ ] **Step 1: 派发** 同一条响应并行调用 10 个 `agent-dispatch.sh --task-file`。
- [ ] **Step 2: 汇总** 检查每批 `all_units_covered=true` 且无重复单元。
- [ ] **Step 3: 抽查** 每批抽取至少 2 个物理结论与来源行/页核对。
- [ ] **Step 4: 交付检查** 汇总 87/87 覆盖，记录失败批次并串行补齐。

## Task 3: 设计专著章节与来源图谱结构

**Blocked by:** Task 2

**Delivers:** 章节映射表、术语/符号约定和 163 文件来源图谱。

**文件:**

- 修改: `docs/pyqcd_physics/report_gluon_tmd_lattice_qcd_review_20261023.tex`
- 新建: `docs/pyqcd_physics/pyqcd_reference_source_atlas.tex`
- 新建: `data/build/pyqcd_monograph_20261023/integration_ledger.tsv`

**接口:**

- 消费: 10 个批次的 `notes.md`、`current_gap.md`、`draft_sections.tex`。
- 产出: `unit_id -> batch -> chapter -> disposition -> source file` 的唯一映射。

- [ ] **Step 1: 目录设计** 建立 18 章、4 个教程附录、来源图谱和审计附录。
- [ ] **Step 2: 去重** 将历史重复版本映射到主版本并保留版本差异说明。
- [ ] **Step 3: 生成图谱** 输出 163 个文件的路径、类型、哈希、页数/行数、用途和章节。
- [ ] **Step 4: 交付检查** 映射表覆盖 87/87 单元和 163/163 文件。

## Task 4: 整合格点基础、相关函数与算法

**Blocked by:** Task 3

**Delivers:** 格点规范理论、费米子、相关函数、谱学、Monte Carlo、Krylov、
蒸馏、统计与外推的专著级章节。

**文件:**

- 修改: `docs/pyqcd_physics/report_gluon_tmd_lattice_qcd_review_20261023.tex`
- 输入: `data/build/pyqcd_monograph_20261023/batches/{B01,B02,B03}/draft_sections.tex`

**接口:**

- 消费: B01–B03 的证据与草案。
- 产出: 统一记号、场论基础、格点方法、数值算法和误差预算章节。

- [ ] **Step 1: 重写基础** 合并 Symanzik、Wilson 线、场强、费米子、HQET、重正化。
- [ ] **Step 2: 重写格点计算** 合并 2pt/3pt、GEVP、Lüscher、形状因子、蒸馏和图分类。
- [ ] **Step 3: 重写算法统计** 合并传播子求解、涂抹、Monte Carlo、误差、bootstrap 和外推。
- [ ] **Step 4: 交付检查** 相关章节无重复定义，公式记号与现有稿一致。

## Task 5: 整合 PDF、胶子算符、TMD、梯度流与匹配

**Blocked by:** Task 3

**Delivers:** PDF/OPE/DGLAP/LaMET/GPD、胶子算符、极化、TMD、质子自旋、
梯度流和连续极限的完整理论链。

**文件:**

- 修改: `docs/pyqcd_physics/report_gluon_tmd_lattice_qcd_review_20261023.tex`
- 输入: `data/build/pyqcd_monograph_20261023/batches/{B04,B05,B06}/draft_sections.tex`

**接口:**

- 消费: B04–B06 的证据与草案。
- 产出: 从光锥 PDF 到格点可计算准量、软函数、匹配、流时窗口和物理 TMD 的闭合章节。

- [ ] **Step 1: 重写 PDF 基础** 合并 PDF、OPE、DGLAP、LaMET、GPD 与准/赝 PDF。
- [ ] **Step 2: 重写胶子与 TMD** 合并胶子算符、36 分量、极化、TMD 软/rapidity 与自旋。
- [ ] **Step 3: 重写流与匹配** 合并梯度流、热核、flow window、SFTX、NLO 与连续极限。
- [ ] **Step 4: 交付检查** 物理层级、极限交换、尺度窗口和失败条件明确区分。

## Task 6: 整合 PyQCD 实现、历史验证、复现实验与学位论文

**Blocked by:** Task 3

**Delivers:** PyQCD 架构与代码、真实数据对照、历史演进、独立学位论文综合、
可复现实验和研究路线。

**文件:**

- 修改: `docs/pyqcd_physics/report_gluon_tmd_lattice_qcd_review_20261023.tex`
- 输入: `data/build/pyqcd_monograph_20261023/batches/{B07,B08,B09,B10}/draft_sections.tex`

**接口:**

- 消费: B07–B10 的证据与草案。
- 产出: 代码—物理对象映射、数据流、测试门、历史审计和论文级综合章节。

- [ ] **Step 1: 实现章** 合并包架构、核心物理链、GPU/并行、缓存、provenance 和 fail-closed。
- [ ] **Step 2: 验证章** 合并 4150、dev5、stab、test6–test9 的证据与版本差异。
- [ ] **Step 3: 论文综合** 吸收两篇独立学位论文与新旧理论工作流的内容结构。
- [ ] **Step 4: 交付检查** 诊断结果不冒充物理验收，历史路径只作为快照语境。

## Task 7: 生成来源图谱与完成全书编译

**Blocked by:** Tasks 4–6

**Delivers:** 完整专著 TeX/PDF、163 文件来源图谱、术语/公式/算法手册和审计附录。

**文件:**

- 修改: `docs/pyqcd_physics/report_gluon_tmd_lattice_qcd_review_20261023.tex`
- 新建: `docs/pyqcd_physics/pyqcd_reference_source_atlas.tex`
- 修改: `docs/pyqcd_physics/report_gluon_tmd_lattice_qcd_review_20261023.pdf`
- 修改: `docs/pyqcd_physics/README.md`

- [ ] **Step 1: 组装** 合并章节、附录、图谱和参考文献。
- [ ] **Step 2: 编译** 连续两遍 XeLaTeX，修复引用、标签、缺字和版面问题。
- [ ] **Step 3: 验收** 检查页数、字体、目录、来源图谱、代表性页面和全文文本。
- [ ] **Step 4: 交付检查** `Overfull=0`、`Float too large=0`、重复标签=0、未定义引用/引文=0。

## Task 8: 全量审计、日志与收敛

**Blocked by:** Task 7

**Delivers:** 可复现证据、严格格式审计结论、根测试结果和最终日志。

**文件:**

- 新建: `logs/v<timestamp>.txt`
- 修改: `logs/AGENTS.md`

**接口:**

- 消费: Task 7 的最终 PDF、TeX、来源图谱和审计输出。
- 产出: 最终报告与恢复入口。

- [ ] **Step 1: 仓库审计** 运行 `python -m myqcd`、`python -m pytest`、
  `form-snapshot-verify`、`form-audit --strict`、旧路径搜索和 `git diff --check`。
- [ ] **Step 2: 覆盖审计** 验证 87/87 单元、163/163 文件、所有章节和来源图谱闭合。
- [ ] **Step 3: 日志** 按 `log` 的 `final` 模式归档完整报告。
- [ ] **Step 4: 收尾** 清除日志脚本可能追加的 EOF 空行，复查 Git 状态并标记 goal 完成。

