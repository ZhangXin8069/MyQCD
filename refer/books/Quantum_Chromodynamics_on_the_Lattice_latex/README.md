# Quantum Chromodynamics on the Lattice — LaTeX transcription

A LaTeX reconstruction of the textbook

> **C. Gattringer and C. B. Lang, *Quantum Chromodynamics on the Lattice:
> An Introductory Presentation***, Lecture Notes in Physics **788**,
> Springer (2010), DOI 10.1007/978-3-642-01850-3.

The source PDF was converted to a compilable LaTeX book.  All prose is
reproduced faithfully; all displayed equations are re-typeset from the
(heavily mangled) text extraction using standard lattice-QCD notation and
auto-numbered to match the original chapter.figure numbering; the 34 figures
were cropped from the original pages and are stored separately in `images/`.

> **Note on fidelity.** Because the conversion was automated from a PDF text
> extraction, equations are a *best-effort reconstruction*.  They are
> physically correct standard expressions, but small typographic differences
> from the printed book are possible.  Figures are 300-dpi raster crops of the
> original vector graphics.

## Structure

```
Quantum_Chromodynamics_on_the_Lattice_latex/
├── main.tex                  # master file: title, TOC, includes all chapters
├── preamble.tex              # packages, page geometry, physics macros
├── chapters/
│   ├── preface.tex
│   ├── chapter01.tex … chapter12.tex
│   └── appendix.tex
├── images/                   # extracted figures, figXY.png (X=chapter, Y=number)
├── extract/                  # raw pdftotext per chapter (source material)
├── build/                    # compile output (main.pdf, aux files)
├── extract_figures.py        # script that cropped the figures from the PDF
├── figures_map.md            # figure number → image file + caption
├── CONVERSION_GUIDE.md       # rules used by the conversion agents
└── README.md
```

## Compiling

```bash
cd Quantum_Chromodynamics_on_the_Lattice_latex
xelatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex
xelatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex   # run twice
```

The compiled PDF is `build/main.pdf` (~408 pages).

Requires: `xelatex` (TeX Live) with the packages `amsmath amssymb amsthm
mathtools graphicx xcolor microtype booktabs multirow caption enumitem url
hyperref cleveref geometry fancyhdr`.

## Reproducing the figures

The figures were extracted with `extract_figures.py`, which:
1. locates each `Fig. X.Y.` caption line via `pdftotext -bbox`,
2. walks up from the caption (skipping axis labels) to the enclosing body-text
   line to bound the figure region,
3. renders that region of the original PDF with `pdftoppm` at 300 dpi.

It writes one PNG per figure into `images/`.  See `figures_map.md` for the
figure list.
