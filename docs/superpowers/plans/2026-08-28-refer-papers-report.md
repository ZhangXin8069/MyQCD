# `refer/papers` 全量总结报告实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 从 `refer/papers/INDEX.md` 登记的 50 篇论文及其英中 LaTeX 源，生成一份中文 16:9、至少 200 页、可追溯且完成全页版式验证的总结报告，并在全部验证通过后创建本地 annotated tag `stab`。

**Architecture:** 使用一个无外部依赖的 Python 生成器读取索引和论文源，建立结构化 corpus manifest，再由同一生成器生成固定页数的 Beamer LaTeX。每篇论文固定四个 frame，使用摘要、章节标题、结果/结论段落和来源路径构成档案；主题综合页使用明确标注的物理结构式和跨论文映射。编译、渲染和检查全部在临时目录完成，最终只复制同名 `.tex`、`.pdf` 和可复查 manifest 到 `docs/`。

**Tech Stack:** Python 3 标准库（`pathlib`、`re`、`json`、`html`）、XeLaTeX、`ctexbeamer`/`beamer`、TikZ、`booktabs`、`tabularx`、`pdfinfo`、`pdftotext`、`pdftoppm`、ImageMagick 或同等图像工具、Git。

**Spec:** `docs/superpowers/specs/2026-08-28-refer-papers-report-design.md`

## Global Constraints

- 论文集合固定为 `refer/papers/INDEX.md` 的 50 行；英中目录合并计一篇，两个已有 Essential Papers 选集不重复展开。
- 直接内容证据来自中文与英文 `main.tex`、`chapters/*.tex`、转换/翻译指南和索引；当前没有论文 PDF，不能声称完成 PDF 原文交叉核验。
- 报告使用 `ctexbeamer` 与 `aspectratio=169`，固定 `frame`，不使用 `allowframebreaks`、浮动 `figure`/`table` 或主体 `\tiny`。
- 每篇论文生成四个信息单元，总页数必须不少于 200；所有数字、结果和物理结论标注为确证、推断或未验证。
- 生成的新文件使用 `report_refer_papers_all_20260828` 前缀，不覆盖 `docs/` 中已有报告。
- 不修改 `refer/papers` 的源文献、索引和指南；不提交、不推送；验证完成后只创建本地 `stab` annotated tag。
- 交付闸门是两遍 XeLaTeX、`Overfull=0`、`Float too large=0`、页数与全量渲染一致、逐页版式检查通过和 `git diff --check` 通过。

---

### Task 1: 建立可复查语料 manifest

**Files:**
- Create: `docs/build_refer_papers_report.py`
- Create: `docs/report_refer_papers_all_20260828.manifest.tsv`
- Read only: `refer/papers/INDEX.md`、50 个中文目录、50 个英文目录及随附指南

**Interfaces:**
- Consumes: `INDEX.md` 的 `英文目录 | 中文目录 | EN页 | ZH页 | 底稿 | 备注` 字段和每篇目录的 TeX 源。
- Produces: 每篇一行的 manifest，字段为 `paper_id`、`title_zh`、`title_en_dir`、`title_zh_dir`、`arxiv`、`en_pages`、`zh_pages`、`section_titles`、`abstract_excerpt`、`result_excerpt`、`source_files`、`evidence_state`；生成器后续直接读取这些字段。

- [ ] **Step 1: 写入解析与证据抽取实现**

  生成器必须：解析 50 个索引行；验证中英文目录和 `main.tex` 存在；从中文 `main.tex` 或 `chapters/abstract.tex` 提取摘要；按 `\\section`、`\\subsection`、`\\subsubsection` 收集章节；优先从包含“总结/结论/展望/讨论”的章节抽取结果段；统计公式、图、表命中数；记录所有被读取的源文件；当字段缺失时写入 `未验证：源文件未提供该信息`。

- [ ] **Step 2: 运行 manifest 生成并核对集合**

  Run: `python3 docs/build_refer_papers_report.py --manifest-only`

  Expected: 退出码 0；生成 50 行数据；每行有唯一 `paper_id`；索引页数总和为 `EN=1285`、`ZH=1175`、合计 `2460`；缺失目录和缺失摘要列表为空或被明确写入 `evidence_state`。

- [ ] **Step 3: 做结构化 smoke test**

  Run: `python3 docs/build_refer_papers_report.py --check-manifest docs/report_refer_papers_all_20260828.manifest.tsv`

  Expected: 退出码 0；报告 `papers=50`、`unique_ids=50`、`missing_required_fields=0`，并打印每篇的章节数、公式/图/表命中数和证据状态分布。

### Task 2: 生成逐页结构和 LaTeX 主文件

**Files:**
- Modify: `docs/build_refer_papers_report.py`
- Create: `docs/report_refer_papers_all_20260828.tex`
- Modify: `docs/report_refer_papers_all_20260828.manifest.tsv`（仅在重新生成时保持字段一致）

**Interfaces:**
- Consumes: Task 1 的 50 条 manifest。
- Produces: `frame_manifest` 注释区和 200 页以上的固定 frame；每篇四页依次对应定位、方法、结果、局限/关联；主文件可独立由 XeLaTeX 编译。

- [ ] **Step 1: 写入安全文本与页面宏**

  生成器对 TeX 特殊字符进行转义，对已有数学片段只在受控公式模板中使用；正文宏统一提供 `\\source`、`\\verified`、`\\inferred`、`\\unverified`、来源表和四类论文 frame。所有流程表格直接放进 frame，正文使用 `\\small` 或模板默认字号，来源使用 `\\scriptsize`。

- [ ] **Step 2: 写入总览和主题综合页**

  主文件开头固定生成：标题页、任务与材料边界、50 篇语料统计、证据等级、跨论文物理链条、六个主题总览、阅读导航。主题页至少覆盖 Wilson 格点规范理论、梯度流/能动量张量、LaMET/准 PDF/赝 PDF、重正化/匹配、胶子 PDF/TMD/介子 PDF、机器学习采样；所有结构式标为“结构式/示意”或附对应来源。

- [ ] **Step 3: 为每篇生成四个完整信息单元**

  每篇第 1 页放书目信息、摘要压缩和研究问题；第 2 页放章节路线、输入/算符/状态/匹配步骤和公式或公式族；第 3 页放源文件中可查的结果/验证/结论与物理含义；第 4 页放局限、证据状态、跨论文接口、对称性/量纲/极限检查和完整来源入口。无结果或无数据时明确显示“未验证”，不填造数字。

- [ ] **Step 4: 生成并做静态占位符检查**

  Run: `python3 docs/build_refer_papers_report.py --generate`

  Expected: 退出码 0；生成 `.tex` 与 manifest；`rg -n '占位符|PLACEHOLDER|TEMPLATE' docs/report_refer_papers_all_20260828.tex` 无匹配；`frame_manifest` 的 expected frame 数不少于 200；50 个 `paper_id` 各出现四次。

### Task 3: 编译与修复 LaTeX

**Files:**
- Modify: `docs/build_refer_papers_report.py` 或 `docs/report_refer_papers_all_20260828.tex`（只修复实际发现的问题）
- Create outside repository: 临时 XeLaTeX 构建目录
- Final: `docs/report_refer_papers_all_20260828.pdf`

**Interfaces:**
- Consumes: Task 2 的主文件和源文献路径。
- Produces: 非空、可提取中文文本、页数不少于 200 的 16:9 PDF。

- [ ] **Step 1: 检查工具链**

  Run: `command -v xelatex; kpsewhich ctexbeamer.cls || kpsewhich beamer.cls; kpsewhich tikz.sty; kpsewhich booktabs.sty; kpsewhich tabularx.sty; command -v pdfinfo; command -v pdftoppm; command -v pdftotext`

  Expected: 所有必需命令/宏包均有路径；缺项时停止并报告具体缺项，不静默降级为竖版。

- [ ] **Step 2: 两遍编译并统计警告**

  Run: `build_dir=$(mktemp -d); xelatex -interaction=nonstopmode -halt-on-error -file-line-error -output-directory "$build_dir" docs/report_refer_papers_all_20260828.tex; xelatex -interaction=nonstopmode -halt-on-error -file-line-error -output-directory "$build_dir" docs/report_refer_papers_all_20260828.tex`

  Expected: 两次退出码均为 0；日志中 `Overfull`、`Float too large`、`Overfull \\hbox`、`Overfull \\vbox` 均为 0；`pdfinfo` 报告页数不少于 200，页面尺寸为 16:9。

- [ ] **Step 3: 按实际错误逐项修复**

  每轮只改一个转义或布局假设；中文命令、百分号、下划线、路径、长标题和表格列优先通过转义、换行或语义拆分修复，不删除来源、不使用 `\\tiny` 和整页缩放。每次修复后重跑两遍编译和警告统计，直到满足 Task 3 Step 2。

### Task 4: 全量渲染、文本和版式验收

**Files:**
- Read: 临时 PDF、全量 PNG、manifest、生成的 `.tex`
- Modify: `docs/build_refer_papers_report.py` 或 `.tex`（若检查发现问题）

**Interfaces:**
- Consumes: Task 3 的 PDF。
- Produces: 实测的 `pages_expected`、`pages_actual`、`pages_rendered`、`pages_checked` 和版式检查结论。

- [ ] **Step 1: 渲染全部页并核对页数**

  Run: `render_dir=$(mktemp -d); pdftoppm -png -r 100 docs/report_refer_papers_all_20260828.pdf "$render_dir/page"`

  Expected: PNG 数量等于 `pdfinfo` 页数；manifest 的 expected frame 数、实际 PDF 页数、渲染页数全部可对账。

- [ ] **Step 2: 全页视觉检查**

  对全部 PNG 逐页检查标题、正文、来源、表格、公式、TikZ 节点/箭头、页脚和安全区；可用 contact sheet 加速定位，但不得只抽查首中尾页。记录 `occlusion_pairs=0`、`clipped_objects=0`、`outside_safe_area=0`；异常页用临时 `\\overfullrule=5pt` 诊断后修复。

- [ ] **Step 3: 文本和来源检查**

  Run: `text_file=$(mktemp); pdftotext docs/report_refer_papers_all_20260828.pdf "$text_file"; rg -n '夸克禁闭|大动量有效理论综述|首个核子胶子部分子分布|证据|未验证|下一步' "$text_file"`

  Expected: 关键论文标题、证据状态、局限/下一步和来源文本均可提取；无明显中文乱码；50 篇论文标题各至少出现一次。

### Task 5: Git 定向复查与 `~tag:stab` 收尾

**Files:**
- Read: `git diff --stat`、`git diff --check`、新增报告文件、规格和计划
- Create: 本地 annotated tag `stab`

**Interfaces:**
- Consumes: Task 4 的全部验证证据和当前工作树。
- Produces: 只包含本次报告相关新增文件的定向复查结果，以及指向当前 HEAD 的本地稳定标签。

- [ ] **Step 1: 复查工作树边界**

  Run: `git diff --check; git diff --stat; git status --short -- docs/superpowers docs/report_refer_papers_all_20260828*`

  Expected: 无空白错误、冲突标记、意外修改 `refer/papers` 源文件或旧报告；新增文件清单与本计划一致，未提交任何内容。

- [ ] **Step 2: 运行 tag dry-run**

  Run: `git tag --list 'stab*' --sort=-creatordate; git show-ref --tags --dereference`

  Expected: 明确当前是否已有 `stab`；若标签已存在，不改写、不覆盖，记录为阻塞并停止创建；若不存在，记录当前 HEAD 和基线标签供 annotated tag 消息使用。

- [ ] **Step 3: 创建本地 annotated tag**

  Run: `base_tag=$(git tag --sort=-creatordate | head -n 1); if test -n "$base_tag"; then tag_message="follow $base_tag, 1. 完成 refer/papers 全量中文总结报告与 200+ 页 PDF 验证; [Codex]."; else tag_message="follow repository HEAD, 1. 完成 refer/papers 全量中文总结报告与 200+ 页 PDF 验证; [Codex]."; fi; git tag -a stab -m "$tag_message"`

  Expected: 仅在 Task 4 和 Task 5 Step 1 全部通过且 `stab` 不存在时执行；`git cat-file -t stab` 输出 `tag`，`git rev-parse 'stab^{}'` 等于创建前 HEAD；不 push。

- [ ] **Step 4: 最终复核标签和报告**

  Run: `git show --no-patch --format=fuller stab; pdfinfo docs/report_refer_papers_all_20260828.pdf | rg 'Pages|Page size|File size'`

  Expected: annotated tag 指向已验证的 HEAD；最终报告仍非空且页数不少于 200；总结中如实列出所有未验证项和验证计数。
