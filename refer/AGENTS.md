# AGENTS.md — refer

格点 QCD 部分子物理文献工作目录，包含三部分：

- `papers/`：50 篇原文的双语 LaTeX 转排（100 个目录）+ 2 套 38 篇导读文选；
- `books/`：8 个教科书的英/中 LaTeX 转排目录；
- `git-rep/`：4 个外部参考代码子模块（PyQCD、PyQCU 已初始化；LQCD_Wickcontraction_reduce、
  feyncalc 当前为空目录）。

原始论文/书籍 PDF 是选编与转排时的本地语料，不随本库保存（`*.pdf` 被 `.gitignore` 排除）。
当前工作区 `papers/`、`books/` 下均无 PDF，`build/main.pdf` 也未保留；除另行注明外，
文档中的页数都是历史实测记录。2026-10-21 仅复验了两套导读文选（EN 36 页 / ZH 35 页）。

## 精华论文选集（2026-08-25 生成）

从本地 99 篇论文语料及其全部参考文献的引文网络中精选 **38 篇奠基文献**，
分八章导读（理论根基 / 模拟引擎 / 梯度流 / LaMET / 重整化 / 胶子PDF / TMD与拟合 /
AI采样），每条含书目卡片、入选理由（附库内引文计数）、物理内容与关键公式。
两套目录实际位于 `papers/` 下：

| 目录 | 语言 | 文档类 | 页数（2026-10-21 复验） |
|---|---|---|---|
| `papers/Essential_Papers_on_Lattice_QCD_Parton_Physics_latex/` | EN | book | 36 |
| `papers/格点QCD部分子物理精华论文选_latex/` | 中文 | ctexbook | 35 |

## 编译

```bash
# 原文/书籍转排（main.tex 使用当前目录相对路径）
cd <dir> && xelatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex  # 两遍

# 两套导读文选（main.tex 使用 \input{../chapters/...}）
cd <dir>/build && xelatex -interaction=nonstopmode -halt-on-error ../main.tex  # 两遍
```

- 选集成品：`papers/<选集目录>/build/main.pdf`；结构为 `main.tex` + `chapters/*.tex`，无图片依赖。
- 2026-10-21 选集复验：两遍编译零错误，英文 36 页、中文 35 页。
- 用户输入清单：`.agent.*.list`（会话原始记录，不入库）。

## 选编依据

38 篇 = 14 篇库内原文里程碑 + 24 篇引文网络枢纽（每篇被库内 ≥3 篇引用，
多数 ≥8 篇）。书目信息转录自库内论文参考文献并交叉核对；不确定字段标 [?]。

## 原文论文转排库（2026-08-26 生成）

`papers/` 下为 **50 篇精华论文的原文 LaTeX 转排库**：每篇一对目录——
`<Slug>_latex/`（英文 article 转排）+ `<中文名>_latex/`（中文 ctexart 译本）。
底稿取 arXiv 官方源归一化改造（49/50；Wilson74 复用 books/ 已验证转排），
100 个目录 xelatex 两遍编译零错误，历史合计 2460 页；当前工作区未保留 PDF，
该页数尚未在 2026-10-21 全量复验。原 PARTIAL 2 处（CT18 缺图、NNPDF17 中文大表图嵌入）
已于 2026-08-26 修复。

- 索引：`papers/INDEX.md`（仅覆盖 50 篇原文；两套导读文选见上节）。
- 结构约定与质量说明：`papers/AGENTS.md`。
- 已知缺口：20 个转排目录缺简版 `AGENTS.md`（19 个中文 + 1 个英文），两套选集目录缺
  `AGENTS.md` 与 `CONVERSION_GUIDE.md`/`TRANSLATION_GUIDE.md`；`papers/anomalpap5.tex`
  为 0 字节遗留文件。清单与状态见 `papers/AGENTS.md`。
- 5 篇前印本经典（Gross-Wilczek/Altarelli-Parisi/HMC/Collins-Soper/Parisi-Wu）
  因无开放获取底稿暂缺。
