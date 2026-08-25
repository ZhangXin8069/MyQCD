# CONVERSION_GUIDE.md

## 底稿来源
- arXiv:0905.2160 官方 LaTeX 源（`https://arxiv.org/e-print/0905.2160`，2009-05-13 tar 包，
  REVTeX4 主文件 `distillation.tex` + 15 个分节 tex + `distillation.bbl`）。
- 发表版信息：Phys. Rev. D 80, 054506 (2009)，DOI 10.1103/PhysRevD.80.054506，
  预印本号 JLAB-THY-09-985，PACS 11.15.Ha / 12.38.Gc / 12.38.Lg（已并入标题块 date 区）。

## 归一化说明
- `\documentclass[11pt]{article}` + geometry(2.5cm) + amsmath/amssymb/mathtools/
  graphicx/microtype/enumitem/url/hidelinks-hyperref；移除 revtex4、epsfig、color(dvips)、latexsym。
- 保留源内自定义宏 `\beq`/`\eeq`；`\Box` 由 amssymb 提供。
- 正文逐字保留（含原文笔误如 "must also included"、"it it crucial"、"100 configuration"）。
- 结构：main.tex + chapters/section01..05 + backmatter.tex（致谢 + 原 .bbl 的
  thebibliography 原样保留，含其自带 fallback 宏定义）；22 条文献一条未删。
- 编号：article 默认节/公式编号；原 figure* 在单栏下等同 figure，未改动。

## 图来源
- 源包 figs/*.eps 共 10 个被引用的 EPS 全部复制到 images/ 并用 Ghostscript 9.55
  (`gs -dEPSCrop -sDEVICE=pdfwrite`) 转 PDF；`\includegraphics{images/xxx.pdf}`。
- wavefn.eps 的 BoundingBox 为 `(atend)`，导致 gs 报错；已把文件尾部的真实
  bbox (31 36 714 524) 写回头部后再转换（images/wavefn_fixed.eps 为中间产物）。
- 源包中 twopi_prin.ps 未被正文引用，未纳入。

## 已知妥协点
- 无。图全部取自官方源并转换成功；无占位图。
