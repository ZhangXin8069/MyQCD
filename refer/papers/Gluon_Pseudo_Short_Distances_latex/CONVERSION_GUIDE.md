# Conversion Guide

- 论文: Gluon Pseudo-Distributions at Short Distances: Forward Case,
  I. Balitsky, W. Morris, A. Radyushkin, Phys. Lett. B 808 (2020) 135621.
- 底稿来源: arXiv 官方源 `arxiv.org/e-print/1910.13963`（单文件 Gluon0803f.tex，
  elsarticle 双栏类 + 6 幅 PDF 矢量图），未使用本地 PDF 重排。
- 归一化说明: `\documentclass[11pt]{article}` + a4paper/2.5cm；统一宏包
  amsmath/amssymb/mathtools/graphicx/microtype/enumitem/url/hyperref(hidelinks)。
  去除 elsarticle 私有宏与全部注释残渣；正文文字、公式、脚注、致谢逐字保留。
- physics 宏包以手写等价宏替代：`\dd`→`\mathrm{d}`，`\bra/\ket` 自定义；
  保留原文宏 `\euv`、`\nn`、算符 `\Si`、`\Ci`。
- 编号: 采用 article 默认连续编号；删除原稿各节 `\setcounter{equation}{0}`
  与 `\theequation` 重定义（所有 \ref 经两次编译解析正常）。
- 图来源: 全部 6 幅取自 arXiv 源（images/*.pdf），无占位图。
- 已知妥协点:
  - 原稿重复 label `gsing`（两处），第二处改名为 `gsingb`（均未被引用）。
  - 原稿被注释掉的 keywords 未收录（源中即注释状态）。
