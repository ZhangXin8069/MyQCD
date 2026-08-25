# CONVERSION_GUIDE

## 底稿来源
- arXiv:2312.05032（v3, 2024-07-18），`https://arxiv.org/e-print/2312.05032` 官方 LaTeX 源
  （WilsonlineGF.tex + JHEPbst/bbl + figs/*.pdf）。
- 书目确认（inspirehep API）：JHEP 06 (2024) 210；作者 Nora Brambilla, Xiang-Peng Wang；
  preprint TUM-EFT 182/23。

## 归一化说明
- 文档类 jheppub(article 变体) → `\documentclass[11pt]{article}` + geometry/amsmath/amssymb/
  mathtools/graphicx/microtype/enumitem/url/hyperref(hidelinks)；去掉 jheppub.sty。
- `slashed` 宏包 → 手写 `\slashed{}` 宏（\vcenter+\ooalign 实现，main.tex 内定义）。
- 标题块手工重排：title/authors/affiliations/emails + preprint/JHEP 卷期/arXiv 行。
- `\acknowledgments`（jheppub 私有）→ `\section*{Acknowledgments}`。
- 正文逐字保留（含摘要、脚注、Note added、致谢、附录）；原 eqnarray 编号结构不动，
  编号沿用 article 默认。原稿中 ``heavy” 等弯引号为源文件原样，未改写。

## 结构
main.tex + chapters/section01–05.tex + chapters/backmatter.tex（致谢+附录A+参考文献）。

## 图来源
- arXiv 源 figs/ 中实际使用的 7 个 PDF 复制到 images/（Wilsonlineself, quarkself, qvertex,
  gluonself, gluonvertexcombine2, quarkquasi, plot）；figs/ 中 gluonvertexcombine.pdf 与
  gluonvertexcombine1.pdf 原文未被引用，未收录。无占位图。

## 已知妥协点
- 无。两次 xelatex 编译退出码 0，无 error、无 undefined reference/citation。
