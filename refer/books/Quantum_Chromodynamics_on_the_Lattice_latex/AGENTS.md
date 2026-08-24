# AGENTS.md — Quantum_Chromodynamics_on_the_Lattice_latex

Gattringer & Lang《Quantum Chromodynamics on the Lattice》(LNP 788, Springer 2010) 英文 LaTeX 转排——格点 QCD 标准教科书。

## 结构

`main.tex`（book 类）+ `preamble.tex`（物理宏 `\ket`/`\bra`/`\ev`/`\tr`/`\order`/`\Nc` 等）；`chapters/preface.tex` + `chapter01.tex`–`chapter12.tex` + `appendix.tex`；`images/figXY.png`（34 图）；`extract/chNN.txt`（原始提取，只读）；`figures_map.md`；`CONVERSION_GUIDE.md`；`build/`。

## 编译

```bash
xelatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex   # 两遍
```

## 方程约定（忠实原书）

- 公式自动编号匹配原书 `(1.3)`、`(4.77)` 等——绝不手写编号或 `\tag`
- 图用 `\caption*{Fig. X.Y. ...}`（星号）保持原书精确图号
- 使用 `preamble.tex` 宏而非自造记号
- 中文译本：`../格点量子色动力学_latex/`
