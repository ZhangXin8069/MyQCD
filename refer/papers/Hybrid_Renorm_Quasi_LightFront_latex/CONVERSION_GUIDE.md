# CONVERSION_GUIDE — Hybrid_Renorm_Quasi_LightFront_latex

## 底稿来源
- arXiv 官方源：`https://arxiv.org/e-print/2008.03886`（gzip tar，含
  `hybrid_ren.tex`、`hybrid_ren.bbl` 与 4 张图 PDF）。
- 书目信息经 Inspirehep API 交叉核对：Nucl. Phys. B 964 (2021) 115311，
  doi:10.1016/j.nuclphysb.2021.115311。

## 归一化说明
- `elsarticle`（preprint,12pt）→ `\documentclass[11pt]{article}` +
  geometry a4paper margin=2.5cm；宏包统一为 amsmath/amssymb/mathtools/
  graphicx/microtype/enumitem/url/hyperref(hidelinks)。
- 原 caption/subcaption/ulem/xcolor/bm/slashp 等宏包未被正文实质使用，
  按规范移除；源文件自定义宏（\MS,\eq,\fig,\nn 等）原样保留。
- frontmatter 的 keyword 环境 → 正文摘要后的 "Keywords:" 一行；
  作者-单位块按 article 类重排（上标字母对应单位列表）。
- 标题脚注给出期刊卷页 / arXiv id / DOI。

## 图来源
- 4 张图全部取自 arXiv 源 PDF，原样复制到 `images/`
  （npr_deltam_new.pdf, extrapolation.pdf, ZLT_pion.pdf, potential.pdf），
  以 `\includegraphics{images/...}` 相对路径引用，无占位图。

## 参考文献
- 采用源内编译产物 `hybrid_ren.bbl` 原样放入 `chapters/backmatter.tex`
  （123 条；含一条未被正文引用的条目 Zhao:2020pdf，属源文件自带，
  按"不得删条目"保留）。tex 内嵌的 thebibliography（122 条）与 bbl 键集合一致，
  二者取其一即可。

## 已知妥协点
- 无。正文（含摘要、致谢、脚注、图表 caption）逐字保留，仅排版样式归一化。
