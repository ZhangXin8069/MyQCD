# AGENTS.md — papers（原文论文 LaTeX 转排库）

50 篇精华论文的**原文转排库**（2026-08-26 由 agent 生成），与本目录的导读文选
（`Essential_Papers_on_Lattice_QCD_Parton_Physics_latex/`、
`格点QCD部分子物理精华论文选_latex/`）并列互补：文选是评注导读，本库是原文全文。

## 结构约定

- 每篇两个目录：`<Slug>_latex/`（英文转排）+ `<中文名>_latex/`（中文译本）。
- 英文版：`article` 类；`main.tex` + `chapters/sectionNN.tex`（每节一文件）+
  `chapters/backmatter.tex`（致谢/附录/参考文献）+ `images/`；由 arXiv 官方源
  归一化改造而成（去除 REVTeX/elsarticle 等期刊私有宏，统一标准宏包），正文逐字保留。
- 中文版：`ctexart`（XeLaTeX，字体 AR PL UMing CN / Droid Sans Fallback）；逐节忠实翻译；
  公式照抄不改；人名与参考文献列表保留英文；插图复用英文目录 `images/`。
- 每目录附 `CONVERSION_GUIDE.md`（英文版来源与妥协点）或 `TRANSLATION_GUIDE.md`
  （中文版约定）及简版 `AGENTS.md`。

## 编译

```bash
cd <目录> && xelatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex  # 两遍
```

## 索引与质量

- 总索引：`INDEX.md`（50 行：目录对 / 实测页数 / arXiv 底稿 / 备注）。
- 100 个目录全部 xelatex 两遍编译通过、日志零错误；合计 2455 页。
- 已声明妥协（PARTIAL）2 处：`CT18_Global_Analysis_latex`（收录 36/88 图，余为占位）、
  `NNPDF17_High_Precision_Data_latex`（中文版 5 张大表以英文原表嵌入）。
- 未收录 5 篇前印本经典（无开放获取底稿）：Gross–Wilczek/Politzer 1973、
  Altarelli–Parisi 1977、Duane et al. 1987(HMC)、Collins–Soper 1981、Parisi–Wu 1981。
- 书目勘误：文选卡片中 Morningstar–Peardon 的 arXiv id 应为 hep-lat/0311018（非 0307022）。
- 生产日志：`.make.2026-08-25-08-59-10.log`；用户输入清单 `.agent.*.list`。
