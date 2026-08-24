# Conversion guide for chapter agents

You are converting one chapter of *Quantum Chromodynamics on the Lattice* by
Gattringer & Lang (LNP 788, Springer 2010) from the raw `pdftotext` dump into
clean, compilable LaTeX.

## Input / output
- **Input**: `extract/chNN.txt` (raw pdftotext output for your chapter). Read it fully.
- **Output**: write `chapters/chapterNN.tex` (one file per agent — do not touch
  any other chapter file).
- The master file `main.tex` already does `\input{preamble}` and includes each
  chapter. `\graphicspath{{images/}}` is set, so images resolve as
  `\includegraphics[width=...]{figXY.png}`.

## What the raw text looks like
`pdftotext` output is noisy. You must clean it up:
- **Page numbers** (a bare number at top or bottom) and **running heads** (e.g.
  `1 The path integral on the lattice` repeated at the top of every page) must be
  **deleted**. The chapter's own title and section headings are real structure —
  keep them.
- The **publisher footer** on the first page of each chapter
  (`Gattringer, C., Lang, C.B.: ... DOI 10.1007/978-3-642-01850-3 ...`)
  must be deleted.
- **Math glyphs are mangled** by the extraction. The character `` is usually
  `\rangle`, `` is `\langle`, ``/`` are also angle brackets from another
  font, `ﬁ` is the `fi` ligature, `−` is minus. Superscripts/subscripts appear on
  separate lines. **Reconstruct every equation from context using your physics
  knowledge** (lattice QCD / quantum field theory). This is the most important
  part of the job. The equation numbers `(1.3)`, `(4.77)`, etc. are preserved in
  the text — use them to stay oriented, but DO NOT typeset the numbers yourself
  (LaTeX auto-numbers).

## Document structure
- Start each chapter file with `\chapter{<Exact chapter title>}`.
- Use `\section{...}`, `\subsection{...}`, `\subsubsection{...}` exactly as the
  book does (the section titles are visible in the raw text, e.g.
  `1.1 Hilbert space and propagation in Euclidean time`).
- Keep the prose text **faithful to the original**, in English, correcting only
  extraction artifacts. Keep paragraph breaks.

## Equations
- Use `\begin{equation} ... \end{equation}` for displayed equations.
- **Preserve the order** of equations so the auto-numbers match the book's
  numbering.
- Use `align`, `gather`, `split`, `cases` where the original needs them.
- In-text references like `(3.61)` can be left as literal `(3.61)` text.
- Use the macros defined in `preamble.tex`:
  - `\ket{n}` → `|n\rangle`, `\bra{u}` → `\langle u|`, `\braket{u}{v}`,
    `\bbraket{u}{A}{v}`, `\vac` for `|0\rangle`
  - `\tr`, `\Tr`, `\ev{...}`, `\order{...}`, `\half`
  - `\im` for the imaginary unit, `\dd` for an upright `d`
  - `\Nc`, `\Nf` for `N_c`, `N_f`
- Do not invent new notation where a standard one exists.

## Figures
The figures of your chapter (from `figures_map.md`) were extracted to
`images/`. At the position where the book shows a figure (the raw text contains
its caption line starting `Fig. X.Y.`), insert:

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.8\textwidth]{figXY.png}
  \caption*{Fig. X.Y. \emph{<caption text as in the book, cleaned up>}.}
  \label{fig:XY}
\end{figure}
```

- Use the exact image filename from `figures_map.md`.
- Pick `width` (typically `0.6\textwidth`–`0.9\textwidth`) so the figure is not
  distorted or tiny. Data plots that span the full page width → `0.9\textwidth`.
- Use `\caption*` (starred) so LaTeX does not re-number it; keep the original
  `Fig. X.Y.` text inside. This preserves the book's numbering exactly.
- If your chapter has no figures, skip this.

## Footnotes
The book uses numbered footnotes. If a footnote is identifiable in the raw text
(its body text appears at the bottom of a page), convert it with `\footnote{...}`
at the appropriate place in the prose. If the footnote anchor is ambiguous,
place it where it most plausibly belongs.

## References section (end of chapter)
Each chapter ends with a `References` section. Reproduce it as:

```latex
\section*{References}
\begin{enumerate}[label={[\arabic*]}]
  \item ... first reference ...
  \item ... second reference ...
\end{enumerate}
```

Keep the references as printed (authors, title, journal, volume, pages, year).
In-text citation markers like `[1–4]` can stay as literal text.

## Quality bar
- The `.tex` file must compile. Avoid stray characters from the extraction.
- Match the book's structure and content as closely as possible.
- Math must be **physically correct** (this is lattice QCD — reconstruct the
  standard expressions).
- If a passage is genuinely too mangled to recover, reproduce the closest
  reasonable LaTeX you can and add a short `% [unrecovered: ...]` comment.
- Do NOT include the preface/TOC/index in a chapter file.
