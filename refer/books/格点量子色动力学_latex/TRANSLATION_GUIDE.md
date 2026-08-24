# 中文翻译指南 (Translation guide for chapter agents)

You are translating one chapter of **C. Gattringer & C. B. Lang, *Quantum
Chromodynamics on the Lattice* (LNP 788, Springer 2010)** from English LaTeX
into **Chinese (Simplified)**, producing a compilable `ctexbook` chapter.

## Input / output
- **Input**: the English LaTeX chapter in this directory, e.g. `chapters/chapterNN.tex`.
- **Output**: overwrite the SAME file with the fully translated Chinese version.
  (The chapter file already exists in the Chinese project — translate it in place.)

## What to translate — and what to leave untouched

**Translate to Chinese:**
- All **prose** (paragraph text) — use standard physics/particle-physics Chinese
  terminology. This is the main work.
- **Section / subsection titles** (`\section{...}`, `\subsection{...}`) and the
  chapter title (`\chapter{...}`).
- **Figure captions** inside `\caption*{Fig. X.Y. ...}` — keep the `Fig. X.Y.`
  prefix as-is (or write "图 X.Y"), translate the description.
- **Table captions** and any table content (labels/words).
- **Footnotes** (`\footnote{...}`).
- The **dedication**, if present.

**Do NOT change (leave exactly as in the source):**
- **All mathematics**: `$...$`, `$$...$$`, `\begin{equation}...\end{equation}`,
  `align`, `multline`, `gathered`, `split`, `\frac`, etc. — the math is
  language-independent; do not touch it.
- **All LaTeX commands and macros** — `\chapter`, `\section`, `\ket`, `\bra`,
  `\ev`, `\tr`, `\order`, `\half`, `\label`, `\ref`, `\includegraphics{figXY.png}`,
  `\emph`, etc. Keep command names; only translate the human-readable text
  arguments inside `{...}`.
- **Equation numbers, figure numbers, cross-references**.
- The **References / bibliography** section — keep it in English (they are
  bibliographic citations). You may add a `\section*{参考文献}` heading in
  Chinese, but the entries stay English.
- In-text citations like `[1–4]` stay as they are.

## Chinese physics terminology (use these)
| English | 中文 |
|---------|------|
| path integral | 路径积分 |
| lattice | 格点 (also 晶格) |
| Euclidean | 欧几里得 (Euclidean time 欧氏时间) |
| Hilbert space | 希尔伯特空间 |
| scalar field | 标量场 |
| gauge field / gauge theory | 规范场 / 规范理论 |
| fermion / quark / gluon | 费米子 / 夸克 / 胶子 |
| hadron | 强子 |
| meson / baryon / proton / pion | 介子 / 重子 / 质子 / 介子 (π 介子) |
| correlation function | 关联函数 (also 关联子) |
| partition function | 配分函数 |
| Hamiltonian | 哈密顿量 |
| propagator | 传播子 |
| Wilson loop / Polyakov loop | 威尔逊圈 / 波利亚科夫圈 |
| plaquette | 基本方格 (Plakette/plaquette, 常用“小方块”或“方格”) |
| effective mass | 有效质量 |
| chiral symmetry | 手征对称性 |
| Monte Carlo | 蒙特卡罗 (直接保留 Monte Carlo 亦可) |
| renormalization | 重整化 |
| chemical potential | 化学势 |
| temperature | 温度 |
| continuum limit | 连续极限 |
| Euclidean action | 欧氏作用量 |
| Grassmann numbers | 格拉斯曼数 |
| hopping parameter | 跳跃参数 |

When a term is commonly kept in English in Chinese physics writing (e.g. QCD,
SU(3), Monte Carlo, Metropolis, Wilson, Ginsparg–Wilson, Haar 测度 is "哈尔测度"
but often written as "Haar 测度"), use the common mixed Chinese/English form.

## Formatting conventions
- Keep the `.tex` structure: same `\chapter`/`\section`/`\subsection` commands,
  same `equation`/`align` environments, same `\includegraphics` calls.
- The chapter is compiled under `ctexbook` — Chinese text will wrap
  automatically; do not force manual line breaks in prose.
- Use Chinese full-width punctuation（，。；）for Chinese prose.
- Keep `\emph{...}` on translated terms where the original emphasized them.

## Quality bar
- The chapter must compile under the project's `main.tex` (xelatex + ctexbook).
- Math must be byte-for-byte identical to the English source where the source
  is correct.
- Translation must be faithful, fluent, and use standard Chinese physics
  terminology. Do not invent or drop content.
- Keep the same length roughly (don't summarize or omit).

## Self-check
After translating, compile to check:
```
cd /root/lattice-pdf/books/格点量子色动力学_latex
xelatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex
```
If your chapter causes errors, fix them before finishing.
