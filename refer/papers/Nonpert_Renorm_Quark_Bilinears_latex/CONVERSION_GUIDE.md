# CONVERSION_GUIDE.md

## 底稿来源
- arXiv:1707.07152 官方 LaTeX 源（`arxiv.org/e-print/1707.07152`，gzip tar）。
  源文件：`aux_renorm.tex`（revtex4-1 单文件）+ `aux_renorm.bbl` + `plots/*.pdf`（7 幅图）。

## 归一化说明
- `revtex4-1` → `\documentclass[11pt]{article}` + geometry(2.5cm)；
  统一宏包 amsmath/amssymb/mathtools/graphicx/microtype/enumitem/url/hyperref(hidelinks)，
  另加源文使用的 `slashed`（系统已装）。超链接配色改为 hidelinks。
- 正文、摘要、脚注、图注逐字保留；公式编号 (1)...、图表编号 Figure 1... 为 article 默认。
- 原文为 PRL 快报无分节，正文整体置于 `chapters/section01.tex`；
  致谢改为 `\section*{Acknowledgments}`；参考文献 = `.bbl` 原样
  （`chapters/backmatter_bbl.tex`，utphys-noitalics 样式产物，未删改条目）。
- 图：`plots/*.pdf` → `images/*.pdf`，`\includegraphics` 路径相应更新；
  原 `figure*`（双栏跨栏）在单栏排版下改为普通 `figure`，两幅并排小图宽 0.495\columnwidth。

## 已知妥协点
- 主标题采用刊出版（PRL 121, 022004）标题 "Nonperturbative Renormalization of
  Nonlocal Quark Bilinears from Lattice QCD"；所用 arXiv 源内标题为早期版本标题
  （"…for quasi-PDFs on the lattice using an auxiliary field"），已在该标题脚注中注明。
- 作者邮箱脚注仅 Green 一人（与源一致）；原 `\date{\today}` 以单位行替代。
- 参考文献 URL 链接颜色随 hidelinks 取消着色（内容未变）。
