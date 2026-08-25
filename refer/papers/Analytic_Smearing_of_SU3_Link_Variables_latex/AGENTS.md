# AGENTS.md

本目录是 C. Morningstar & M. Peardon, "Analytic Smearing of SU(3) Link
Variables in Lattice QCD", Phys. Rev. D 69, 054501 (2004) 的英文 LaTeX
转排（arXiv:hep-lat/0311018 源码归一化重排，正文逐字保留）。

编译（两遍）：
```bash
cd build 之外的本目录内执行：
xelatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex
```
成品：`build/main.pdf`。详见 CONVERSION_GUIDE.md。
