# Conversion Guide — INTRODUCTION TO LATTICE QCD → LaTeX

Source: R. Gupta, "Introduction to Lattice QCD" (arXiv:hep-lat/9807028v1, 11 Jul 1998),
a 150-page set of school lectures. This repo is a faithful LaTeX transcription.

## Directory layout

```
main.tex                      master document (already written)
chapters/secNN_name.tex       one chapter file per original section (1–20)
extract/secNN.txt             raw pdftotext output per section (INPUT, read-only)
images/figN.png               extracted figures, Fig.1–Fig.35 (referenced from chapters)
```

## Numbering model (important)

The source numbers sections 1–20, subsections 6.1, 6.2, …, sub-subsections
14.2.1, …, equations (5.1), …, but figures globally (Fig. 1–35) and tables
globally (Table 1–8). main.tex is set up so:

- each original section → `\chapter` (auto-numbered 1–20, matching the source),
- each original subsection → `\section`, sub-subsection → `\subsection`
  (auto-numbering then reproduces the source's 6.1, 14.2.1, …),
- equations auto-number per chapter → (5.1), (6.2), … matching the source,
- figures and tables are forced to global numbering so they come out 1–35 / 1–8.

So: **do not hand-number anything**. Write `\begin{equation}`, `\begin{table}`,
`\begin{figure}` with empty numbering and let the counter do the work.

## Per-chapter transcription rules

1. **Input**: read `extract/secNN.txt`. It has page separators
   `% -------- PDF page N --------`. Strip the running heads
   ("INTRODUCTION TO LATTICE QCD" / "Rajan Gupta") and standalone page numbers
   (single integers that appear at the top or bottom of a page block).
2. **Output**: write `chapters/secNN_name.tex` (lower-case, underscore for the
   name; e.g. `sec05_minkowski_euclidean.tex`).
3. First line: `\chapter{<exact source section title>}` (chapter number is
   automatic).
4. Body paragraphs: plain text, blank line between paragraphs, `\noindent` not
   required.
5. **Equations**: the pdftotext output is a mangled linear rendering of the
   math. Reconstruct each equation into correct LaTeX using your knowledge of
   the physics. Examples:
   - `x2E = 4 X x2i = x 2 − t2 = −x2M`  →  `x_E^2 = \sum_{i=1}^4 x_i^2 = \mathbf{x}^2 - t^2 = -x_M^2`
   - `p0 ≡ E → ip4`  →  `p_0 \equiv E \to i p_4`
   - `γµ (1 − γ5 ) V`  →  `\gamma_\mu (1 - \gamma_5) V`
   - `W R T = 1/Z R dU WRT eβ/2N (W11 +W11 )` → a proper integral equation.
   Display equations go in `\begin{equation} ... \end{equation}`; inline math in
   `\( ... \)` or `$ ... $`.
6. **Tables**: transcribe as
   `\begin{table}[htbp] \centering \begin{tabular}{...} ... \end{tabular} \caption{...} \label{tab:N} \end{table}`.
7. **Figures**: wherever the source shows `Fig. N. <caption>`, insert
   `\begin{figure}[htbp] \centering \includegraphics[width=0.8\textwidth]{images/figN.png} \caption{<caption text>} \label{fig:N} \end{figure}`.
   Place it at the natural location (the paragraph discussing it). Omit the
   `Fig. N.` prefix from the caption text.
8. **Faithfulness**: transcribe the prose as-is — do not add commentary,
   editorial notes, or new content. Fix pdftotext artifacts (stray line breaks,
   split words, spacing). Preserve the meaning and all physics content.
9. Use LaTeX conventions: `---` for em-dash, `` ` `` and `'` for quotes,
   `\textit` for italic, `\textbf` for bold. Greek and math symbols belong in
   math mode, not as Unicode.
10. Sub-sections like "14.2.1. Wilson Loops" → `\subsection{Wilson Loops}`.

## Do not

- Do not `\tag` equations, `\setcounter`, or hardcode any numbers.
- Do not invent figures — only the 35 extracted PNGs exist.
- Do not leave Unicode math symbols in the text; convert to LaTeX math.
