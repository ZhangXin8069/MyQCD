# CONVERSION_GUIDE — NNPDF17_High_Precision_Data_latex

## 底稿来源
- arXiv:1706.00428 官方源 (`https://arxiv.org/e-print/1706.00428`, gzip tar)，含全部
  `sec-*.tex`、`nnpdf31.bbl`、264 个 `plots/` 图源与 `tables/` 表格源。
- 库内本地 PDF 未使用（arXiv 源完整）。

## 归一化说明
- `\documentclass[11pt]{article}` + geometry(a4paper,margin=2.5cm)；统一宏包
  amsmath/amssymb/mathtools/graphicx/microtype/enumitem/url/hidelinks-hyperref，
  另按需保留 float、multirow（表格源码需要）；去掉 epsfig/cite/afterpage/JHEP.bst。
- 原文宏块（\be/\ee、\frac 重定义等）逐字保留于 main.tex，公式渲染与原文一致。
- `\epsfig{width=…,figure=…}` 机械改写为 `\includegraphics[width=…]{images/…}`；
  图片路径 `{plots/...}` → `{images/plots/...}`。
- sec-results.tex 包装文件已就地展开；致谢从 sec-delivery 尾部切出，连同
  nnpdf31.bbl 原文一并置于 chapters/backmatter.tex。
- 标题块重排：报告编号 + 标题 + 作者/单位照录；脚注行给出期刊卷页与 arXiv 号。

## 图来源
- 源图全部可用：252 个被引用图（plots/ 目录 PDF/PNG）全量收录至 images/plots/，
  超过 60 张上限；因源图零成本全量可得，为保证保真度未做删减，无占位图。

## 已知妥协点
1. DOI 具体后缀无法在允许域名内核实，标题脚注中标 `[?]`。
2. 编号沿用 article 默认（原稿即 \numberwithin 分节编号），未模仿双栏排版。
3. 参考文献为 .bbl 原文照录（JHEP.bst 风格），个别条目信息不全系原 bbl 所致。
