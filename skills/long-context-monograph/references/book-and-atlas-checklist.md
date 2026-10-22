# 书稿合并、来源图谱与编译验收

本参考用于把通过评审的批次草案合并成可追踪专著，并证明书稿、来源图谱和 PDF 是同一
版本。所有路径以仓库根为工作目录；来源快照保持只读。

## 1. 书籍骨架

长稿使用规范书籍类，不用装饰成书的长文章结构。默认骨架为
`ctexbook`、A4、12pt、`twoside`，并设置可读的内外页边距、章首页和每章重置页眉。

```latex
\documentclass[UTF8,12pt,a4paper,twoside,openany]{ctexbook}
\usepackage[top=2.7cm,bottom=2.8cm,inner=2.8cm,outer=2.4cm,headheight=15pt]{geometry}
\usepackage{amsmath,amssymb,mathtools}
\usepackage{booktabs,tabularx,array,longtable}
\usepackage{graphicx,float,seqsplit}
\usepackage{fancyhdr}
\usepackage{hyperref}

\pagestyle{fancy}
\fancyhf{}
\fancyhead[LE,RO]{\small\thepage}
\fancyhead[RE]{\small\nouppercase{\leftmark}}
\fancyhead[LO]{\small\nouppercase{\rightmark}}

\begin{document}
\frontmatter
\tableofcontents
\listoffigures
\listoftables
\listofalgorithms
\mainmatter
\part{理论基础}
\chapter{引言}
\appendix
\chapter{来源图谱}
\backmatter
\begin{thebibliography}{99}
\end{thebibliography}
\end{document}
```

检查项：

- `frontmatter` 放摘要、前言和目录；`mainmatter` 重新启用阿拉伯页码；`backmatter` 放
  参考文献、索引等不编号材料。
- `part/chapter/section` 层级连续，章首页不沿用上一章页眉，奇偶页页码位于外缘。
- 所有章、节、公式、图、表和算法使用 `\label`/`\ref`，正文不手写旧章节号。
- 附录在 `\appendix` 后编号；来源图谱属于附录或审计附录，不能藏在未标记的补充文件。
- 参考文献键与 `\bibitem` 或 `.bib` 一致；中文书名和作者不因字体切换缺字。

## 2. 从 `data/` 抽取为可追踪模块

批次产物位于不入库的 `data/build/`，不能成为最终编译依赖。只抽取经过证据核对和语义
审阅的纯正文/附录，写入例如 `docs/<project>/monograph/<topic>.tex`。抽取时删除：

- 批次专用 `\documentclass`、`\usepackage`、`\begin{document}`/`\end{document}`；
- 验证 harness、临时宏、页面尺寸覆盖和来源快照中的安装/运行命令；
- 重复导言、批次完成说明、TODO 与未审阅的整段复制。

保留章节内容、唯一命名空间标签、公式与表格，以及必要的来源说明。对每个模块执行：

```bash
if git check-ignore -q docs/pyqcd_physics/monograph/lattice_foundations.tex; then
  echo 'tracked module path is ignored' >&2
  exit 1
fi
rg -n '\\input\{data/' docs/pyqcd_physics
```

`git check-ignore -q` 对未忽略文件返回 1，因此上面的组合以退出码 0 表示该模块
不是被忽略的运行数据；第二条应无匹配。主稿中的输入路径使用
`\input{docs/.../module.tex}`，使干净检出和 CI 能复现编译。

## 3. 跨批次合并清单

### 标签与定义

- 合并前后分别提取 `\label{...}`，重复标签必须降到零。
- 批次标签保留来源前缀，例如 `b01:u040-...`；主稿若需稳定公共标签，再建立显式映射。
- 同名宏只保留一个权威定义。用 `\providecommand` 前先确认语义一致；不同含义改用独立名称。
- 检查 `\ref`、`\eqref`、`\cite`、图文件和 bibitem 的闭包，不以“少几条 warning”代替闭合。

### 表格、公式与浮动体

- 宽表优先改 `longtable` 或 `tabularx`，必要时缩字号和拆分列；不缩小到不可读。
- 多行公式用 `align`/`split`/`aligned` 分行，长推导移入附录并保留主文逻辑链。
- 图和算法设置明确宽度、最大高度和分页策略；跨章浮动体不得遮挡正文或越过页边界。
- 对 `Overfull \hbox`、`Overfull \vbox` 和 `Float too large` 修改内容或版式，不删除日志。

### 非 ASCII 路径与哈希

中文文件名需要实际可用的 CJK 字体和可断行路径。来源路径宏可用 `seqsplit`；哈希按固定
长度切段，在段间插入 `\allowbreak` 或换行，避免 64 字符不可断字符串溢出。

```latex
\providecommand{\sourcepath}[1]{%
  \seqsplit{#1}}
```

生成路径参数时转义 `_` 等 TeX 特殊字符；不要只把中文路径塞进 Latin Modern Mono
或 `\path`，否则 XeCJK 可能绕过 CJK fallback。需要等宽展示时，应单独验证混合字体。
生成器应把哈希切成例如 16 字符一段，并在段间使用 `\allowbreak`；渲染时保持原哈希
语义，不得插入会让人误认为是哈希内容的空格或连字符。编译日志中的
`Missing character` 必须为零。

## 4. 来源图谱生成

图谱是机器索引的渲染结果，不维护第二份手写大表。输入至少包括：

- `snapshot_inventory.json`：163 个内容文件的路径、类型、字节、行/页、SHA-256、成对关系；
- `content_units.json`：87 个知识单元的主文件、伴生文件和规模；
- `integration_ledger.tsv`：单元到批次、章节、目标产物和覆盖状态的唯一映射；
- 固定提交、许可证、manifest 匹配和控制文件计数。

生成器必须断言内容文件数、单元数和目标章节键完整，再输出来源图谱。图谱至少包含：

1. 来源基线与控制文件；
2. 单元级主文件、伴生 PDF、类型、规模和目标章节；
3. 文件级路径、类型、行/页、字节和 SHA-256；
4. TeX/PDF 成对关系、独立 PDF、历史重复版本的处理说明；
5. 文件级与单元级覆盖结论。

当前项目可用生成器：

```bash
python data/build/pyqcd_monograph_20261023/generate_source_atlas.py
git diff -- docs/pyqcd_physics/pyqcd_reference_source_atlas.tex
```

生成后复核逐文件编号连续、每个 PDF 未因去重消失、每个哈希按段断开、所有中文路径可
渲染。生成器的输入变化时重新生成，不直接编辑生成区。

## 5. 两遍 XeLaTeX

在 `data/build/` 中保存 aux/log/out/toc，不把中间件写回 `docs/`。当前主稿命令：

```bash
BUILD_DIR=data/build/pyqcd_monograph_20261023/main_build
mkdir -p "$BUILD_DIR"
xelatex -interaction=nonstopmode -halt-on-error -output-directory="$BUILD_DIR" docs/pyqcd_physics/report_gluon_tmd_lattice_qcd_review_20261023.tex
xelatex -interaction=nonstopmode -halt-on-error -output-directory="$BUILD_DIR" docs/pyqcd_physics/report_gluon_tmd_lattice_qcd_review_20261023.tex
```

两遍均须退出 0。第二遍后检查最终 log，不使用第一遍结果判定目录、引用或页码已经稳定。

```bash
LOG="$BUILD_DIR/report_gluon_tmd_lattice_qcd_review_20261023.log"
if rg -n 'LaTeX Error|Undefined control sequence|undefined references|Citation .* undefined|Reference .* undefined|Rerun to get|Overfull \\(hbox|vbox)|Float too large|Missing character' "$LOG"; then
  echo 'compile diagnostics found' >&2
  exit 1
fi
```

命令无匹配时退出 0。若出现诊断，先修复再重跑两遍；不得用 `\sloppy` 全局掩盖所有溢出，
也不得把只读来源中的历史 warning 当作本次可忽略。

## 6. 引用、标签和 PDF

检查重复标签与缺失引用键：

```bash
rg --no-filename -o '\\label\{[^}]+\}' docs/pyqcd_physics/report_gluon_tmd_lattice_qcd_review_20261023.tex docs/pyqcd_physics/monograph/*.tex | sed 's/.*\\label{//; s/}$//' | sort | uniq -d
rg -n '\\(ref|eqref|cite)\{' docs/pyqcd_physics/report_gluon_tmd_lattice_qcd_review_20261023.tex docs/pyqcd_physics/monograph/*.tex
pdfinfo "$BUILD_DIR/report_gluon_tmd_lattice_qcd_review_20261023.pdf" | rg '^(Pages|Page size|File size):'
pdffonts "$BUILD_DIR/report_gluon_tmd_lattice_qcd_review_20261023.pdf"
```

重复标签命令应无输出；引用键与源定义由编译日志和辅助审计共同确认。PDF 需要检查页数、
A4 尺寸、字体嵌入和可提取文本，并对摘要、长表、公式密集页、章首页和来源图谱做代表性
页面目视检查。未做视觉检查时明确写为验证缺口。

## 7. 全量验收门

| 维度 | 机器证据 | 通过条件 |
|---|---|---|
| 文件覆盖 | inventory、manifest、integration summary | 163/163 文件哈希匹配，缺失/额外为 0 |
| 知识覆盖 | integration ledger、batch coverage | 87/87 单元唯一归属，缺失/重复为 0 |
| 来源图谱 | 生成器输出与最终 PDF | 每个内容文件、伴生 PDF 和哈希均在最终图谱 |
| 编译 | 两遍 XeLaTeX 日志 | 两遍均 0；undefined refs/cites、Overfull、Float too large、Missing character 为 0 |
| PDF | `pdfinfo`、`pdffonts`、页面抽查 | 页数与尺寸符合交付，字体嵌入，代表性版面无遮挡 |
| 公式审计 | `python -m myqcd` | 核心检查通过；库存级未解析项与核心失败分开报告 |
| 根测试 | `python -m pytest` | 全部通过且记录收集/通过数量 |
| 格式治理 | `form-snapshot-verify`、`form-audit --strict --quiet` | 快照验证通过；本次文件无新增告警 |
| Git | `git diff --check` | 无空白错误，未混入来源快照或运行数据 |

最终日志按以下顺序记录，确保他人能从证据复现结论：

```text
固定来源与许可证
inventory / content units 基线哈希
批次分配与失败派发
唯一一次重试与串行降级
实际修改和新增文件
最终 PDF 页数与字节数
两遍编译和日志扫描
引用、标签、字体与视觉检查
文件/单元/哈希闭环
根测试、公式审计、格式审计、Git 检查
未执行验证与仍需人工判断的物理结论
```
