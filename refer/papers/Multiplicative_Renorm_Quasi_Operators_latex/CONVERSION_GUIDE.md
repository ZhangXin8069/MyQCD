# CONVERSION_GUIDE

## 底稿来源
- arXiv 官方源 `arXiv:1809.01836`（e-print tar.gz，主文件 `gluon_ren_v0917.tex` + `paper.bbl` + 4 幅 EPS 图）。
- 原稿为 revtex4-1 双栏；本版按统一规范改为 `article` 单栏。

## 归一化说明
- `\documentclass[11pt]{article}` + geometry(2.5cm)；宏包 amsmath/amssymb/mathtools/graphicx/microtype/enumitem/url/hyperref(hidelinks)。
- 移除 revtex4-1、epsfig、epstopdf、slashed、extarrows、bm 等期刊/冗余宏包。
- `extarrows` 的 `\xlongequal{UV}` 以手写宏 `\stackrel{\text{#1}}{=}` 等价替换（正文两处）。
- revtex 的 `\email`/`\affiliation` 改为标题块 + 脚注邮箱；文首加 PRL 卷页与 arXiv 行。
- 正文散文逐字保留（含摘要、致谢、Note added）；公式原样照抄；编号为 article 默认。

## 图来源
- 源内 4 幅 EPS（oneloop-g, div-topo-g, Green-1-g, Green-2-g）用 ghostscript 转为 PDF 放入 `images/`，全部保留，无占位图。

## 参考文献
- `paper.bbl` 原样复制为 `chapters/bibliography.tex` 并在 `backmatter.tex` 中 `\input`，未删改条目。

## 已知妥协点
- 无。原文无附录；`\today` 日期行删除（以发表信息代替）。
