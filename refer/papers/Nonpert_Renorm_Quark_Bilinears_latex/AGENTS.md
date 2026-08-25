# AGENTS.md

本目录为论文 "Nonperturbative Renormalization of Nonlocal Quark Bilinears from
Lattice QCD"（Green, Jansen, Steffens, PRL 121, 022004 (2018); arXiv:1707.07152）
的英文 LaTeX 转排（自 arXiv 官方源归一化重排）。

编译：
```bash
cd 本目录 && xelatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex  # 两遍
```
成品：`build/main.pdf`。详见 `CONVERSION_GUIDE.md`。
