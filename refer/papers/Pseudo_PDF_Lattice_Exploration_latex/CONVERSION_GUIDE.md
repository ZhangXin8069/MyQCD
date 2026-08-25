# CONVERSION_GUIDE — Pseudo_PDF_Lattice_Exploration_latex

## 底稿来源
- arXiv 官方源：`https://arxiv.org/e-print/1706.05373`（gzip tar，
  内含 revtex4-1 源文件 `pseulat1027.tex` + 19 个 PDF 图）。
  无库内本地 PDF。

## 归一化说明
- `revtex4-1`（twocolumn, aps）→ `\documentclass[11pt]{article}` +
  geometry(a4,2.5cm) + amsmath/amssymb/mathtools/graphicx/microtype/
  enumitem/url/hidelinks hyperref；单栏、article 默认节/公式编号。
- 正文（摘要、脚注式 DOI/arXiv 行、致谢、27 条参考文献）逐字保留；
  参考文献从源文件原样截取，未增删改写。
- 去除 REVTeX 私有命令：`\pacs`→正文 PACS 行；`\acknowledgements`→
  `\section*{Acknowledgements}`；affiliation→文首居中机构块。
- 交叉引用编号适配：正文 "Sections II/III/IV/V/V.D" → "Sections 2/3/4/5/5.4"。
- 技术性修正：删除第二个方程上重复的 `\label{newVDFxzQ}`；
  仅保留正文用到的宏 `\nn`。作者注释掉的草稿段落未收录。

## 图来源
- 全部 19 张图直接取自 arXiv 源包，复制至 `images/`，无占位图。

## 已知妥协点
- 双栏排版与期刊页码分栏不保留；plateau 双图以 \hfill 并排呈现。
