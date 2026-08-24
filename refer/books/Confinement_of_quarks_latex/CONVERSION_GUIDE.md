# Conversion Guide: "Confinement of quarks"

This document records how the LaTeX transcription was generated from the
source PDF `../Confinement of qnarks.pdf` (Kenneth G. Wilson,
Phys. Rev. D 10, 2445 (1974)).

## Source material

- **Source PDF**: `../Confinement of qnarks.pdf` (15 pages, letter size,
  two-column Phys. Rev. layout; pages 2445–2459).
- **Raw extraction**: `pdftotext` per page in `extract/page01.txt` …
  `extract/page15.txt`.  Pages 1 and 15 also contain the *tail of the
  preceding paper* (effective action for composite operators) and the
  *head of the following paper* (Cheng, Ng, Young, PRD 10, 2445 (1974)),
  respectively; these are NOT part of the transcription.
- **Figures**: 10 line drawings, cropped at 300 dpi into `images/` by
  `extract_figures.py` (hand-verified regions + ink auto-crop).
  See `figures_map.md`.

## Prose

- The prose is a faithful transcription of the paper, with OCR
  artifacts of the scan corrected to the intended English (e.g.
  "gnarks" → "quarks", "mould" → "would", "w'II" → "WILSON",
  "clat." → "et al.", "tinker" kept).  Reference markers are
  superscript numbers matching the paper's reference list (1–21;
  see note below).
- In-text figure references keep the paper's style: "Figure 1",
  "cf. Fig. 2", "Fig. 6(a)", "see Fig. 10".  These resolve via
  `\ref` to the exact figure numbers (the starred `\caption*{Fig. N.
  ...}` preserves the paper's global figure numbering).

## Equations

- **Numbering**: `\theequation = \arabic{section}.\arabic{equation}`,
  so auto-numbers match the paper: section II → (2.x), III → (3.x), …
  Equation numbers in the text, e.g. "Eq. (3.13)", stay literal.
- **Notation**: the lattice gauge-field variable is written
  $\theta_{\mu\nu}(n)$ (the scan renders it variously as A/B/8/θ);
  the plaquette rescaled field is $f_{\mu\nu}$; $\psi_n, \bar\psi_n$
  are the lattice Dirac fields; $\epsilon = m_0a^4$, $\kappa = a^2/2$
  are the parameters of the full action (3.12).
- **Fidelity note (IMPORTANT)**: the PDF is a 1974 scan; `pdftotext`
  garbles many display equations.  Every equation was reconstructed
  from the raw text + the equation numbers + the surrounding prose +
  standard knowledge of this foundational paper.  The structure and
  numbering are faithful; individual prefactors/indices are
  best-effort and should be checked against the scan before citation.
  In particular:
  - Eq. (3.2)/(3.3): the lattice gauge transformation of $\psi$ and $\theta$.
  - Eq. (3.7): the field-strength definition (signs/prefactors
    reconstructed).
  - Eq. (3.42)–(3.44): the single-site Grassmann-bracket results.
  - Eq. (4.4): the term of order $g^{-2n}$.

## Document structure

- `main.tex` — `article` class, XeLaTeX; title + abstract + six sections
  + acknowledgments/references.  `\graphicspath{{images/}}` set.
- `preamble.tex` — packages and physics macros
  (`\thl{μν}` for θ, `\ev{...}` for ⟨...⟩, `\dd` for d, etc.).
- `chapters/section01.tex` … `section06.tex` + `backmatter.tex`.
- `figures_map.md`, `chapter_sections.txt`, `overfull_fixes.txt`.

## Compiling

```bash
cd Confinement_of_quarks_latex
xelatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex   # ×2 passes
```

Output: `build/main.pdf` (~29 pages); root copy `Confinement_of_quarks.pdf`.

## References note

The reference list has 20 numbered entries (1–20).  The in-text
citations "Ref. 20" and "Ref. 21" in Sec. VI are kept literal, exactly
as printed in the scan (the paper's own typesetting).
