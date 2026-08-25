# AGENTS.md

本目录是 H. Suzuki 论文 "Energy–momentum tensor from the Yang–Mills
gradient flow"（PTEP 2013, 083B03; arXiv:1304.0533）的英文归一化 LaTeX
转排版（由 arXiv 官方源重排，标准 article 类）。

编译：

```bash
xelatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex  # 两遍
```

成品：`build/main.pdf`。详见 `CONVERSION_GUIDE.md`。
