# AGENTS.md

本目录是 Bali, Lang, Musch, Schäfer (RQCD),
"Novel quark smearing for hadrons with high momenta in lattice QCD",
Phys. Rev. D 93, 094515 (2016), arXiv:1602.05525 的 LaTeX 归一化转排版
（底稿为 arXiv 官方源，正文逐字保留）。

编译：
```bash
cd Novel_Quark_Smearing_High_Momenta_latex && \
xelatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex  # 两遍
```
成品：`build/main.pdf`。结构：`main.tex` + `chapters/*.tex` + `images/*.pdf`。
