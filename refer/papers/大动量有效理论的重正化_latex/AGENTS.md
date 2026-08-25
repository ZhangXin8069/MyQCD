# AGENTS.md

本目录是 Ji–Zhang–Zhao《Renormalization in Large Momentum Effective Theory of Parton Physics》(PRL 120, 112001 (2018), arXiv:1706.08962) 的中文全译本（对应英文转排版 `../Renorm_LaMET_PRL_latex/`）。

编译（两遍）：

```bash
mkdir -p build && cd build && xelatex -interaction=nonstopmode -halt-on-error ../main.tex && xelatex -interaction=nonstopmode -halt-on-error ../main.tex
```

成品：`build/main.pdf`。
