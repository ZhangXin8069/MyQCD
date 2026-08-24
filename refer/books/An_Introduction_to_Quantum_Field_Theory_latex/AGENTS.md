# AGENTS.md — An_Introduction_to_Quantum_Field_Theory_latex

Peskin & Schroeder《An Introduction to Quantum Field Theory》英文 LaTeX 转排（源 PDF 在 `../`）。

## 结构

`main.tex`（book 类，三个 part：I. 费曼图与 QED ch01–07、II. 重整化 ch08–13、III. 非阿贝尔规范理论 ch14–22 + 附录）；`chapters/chXX.tex` 每章一个文件；`images/` 图（figX.Y.png）；`extract/` 原始 pdftotext（只读）；`build/` 编译产物。

## 编译

```bash
cd build; xelatex -interaction=nonstopmode -halt-on-error ../main.tex   # 两遍
```

需要 `slashed` 宏包（TeX Live）。方程按章自动编号 `(2.1)`；图保持原书 X.Y 编号。部分未定义引用（如 eq:4.48）来自原书引用但未编号的公式，保留原样。
