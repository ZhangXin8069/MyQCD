# AGENTS.md — Chiral_Symmetry_YM_Gradient_Flow_latex

Lüscher《Chiral symmetry and the Yang–Mills gradient flow》(JHEP 04 (2013) 123,
arXiv:1302.5246) 的英文 LaTeX 转排目录，由 arXiv 官方源归一化重排而来，
正文逐字保留。编译：

```bash
cd build && xelatex -interaction=nonstopmode -halt-on-error ../main.tex   # 两遍
```

成品：`build/main.pdf`（34 页）。结构：`main.tex` + `chapters/*.tex` +
`luescher-macros.tex` + `images/`。详见 CONVERSION_GUIDE.md。
