# CONVERSION_GUIDE.md

## 底稿来源
- arXiv 官方 LaTeX 源：`https://arxiv.org/e-print/hep-lat/0311018`
  （任务单给出的 hep-lat/0307022 实为 Adams & Bietenholz 另一篇论文，
  经核对后改用本文正确的 id hep-lat/0311018；源内含 stout_links.tex、
  stout_links.bbl 及 4 幅 EPS 图）。
- 无库内本地 PDF。

## 归一化说明
- `\documentclass[aps,prd,twocolumn]{revtex4}` → `[11pt]{article}` +
  geometry/a4paper/2.5cm；统一宏包 amsmath,amssymb,mathtools,graphicx,
  microtype,enumitem,url,hyperref(hidelinks)。
- 额外引入 `natbib[numbers]`：原 .bbl 为 REVTeX/natbib 格式（含
  \bibitem[...] 可选标签与 \bibinfo 等宏），用 natbib 数字模式可把全部
  22 条文献**逐字原样**收录而不改写条目。
- 标题块重排为 article 式 title/author/affiliation；期刊卷页年、arXiv id
  与 PACS 以题下信息行给出；`\pacs{}`/`\affiliation{}`/`\date{\today}`
  等 REVTeX 命令按规范移除。
- 正文、摘要、公式、脚注式内容逐字保留；6 节各成 chapters/sectionNN.tex；
  致谢+参考文献在 chapters/backmatter.tex（bbl 原文照录）。

## 图来源
- 源内 4 幅 EPS 用 epstopdf 转 PDF 存 `images/`（xelatex 不直接支持 EPS）；
  `\includegraphics` 去掉了 twocolumn 版式的 `bb=` 裁剪参数，宽度改为
  单栏相对宽度（0.98\textwidth / 0.78\textwidth）。图内容未改动。

## 已知妥协点
- REVTeX 的 `acknowledgments` 环境在 article 类不存在，导言区以同名环境
  映射到无编号 \section*，正文文字未动。
- 公式编号沿用 article 默认全局顺序编号（原文 revtex 编号方式一致）。
- 式 (eq:sigma) 末行空行的编号行为与 arXiv 源一致，未做修饰。
