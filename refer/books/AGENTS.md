# AGENTS.md — books

格点 QCD 理论与量子场论参考教科书。每本三种形态：原始**源 PDF**、**英文 LaTeX 转排**（agent 生成）、部分有**中文 LaTeX 译本**（agent 生成，`ctexbook`）。

| 目录 | 语言 | 来源 |
|---|---|---|
| `Quantum_Chromodynamics_on_the_Lattice_latex/` | EN | Gattringer & Lang（12 章，~408 页） |
| `INTRODUCTION_TO_LATTICE_QCD_latex/` | EN | Gupta（20 节→章） |
| `An_Introduction_to_Quantum_Field_Theory_latex/` | EN | Peskin & Schroeder（22 章） |
| `Confinement_of_quarks_latex/` | EN | Wilson 1974（6 节） |
| `格点量子色动力学_latex/` | 中文 | Gattringer & Lang 中译（~392 页） |
| `格点QCD导论_latex/` | 中文 | Gupta 中译 |
| `量子场论导论_latex/` | 中文 | Peskin & Schroeder 中译（419 页） |
| `夸克禁闭_latex/` | 中文 | Wilson 中译 |

## 编译

```bash
cd <dir>; xelatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex  # 两遍
```

- 全文：各目录 `build/main.pdf`；图：各目录 `images/`（300dpi PNG）；原始提取：`extract/chNN.txt`
- Gattringer & Lang（英/中）是费米子作用量、规范场离散化、强子谱、蒸馏方法的主要参考；Wilson 论文（英/中）是格点规范理论原始表述参考
