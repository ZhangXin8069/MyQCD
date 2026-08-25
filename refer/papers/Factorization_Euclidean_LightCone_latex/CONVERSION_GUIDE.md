# Conversion Guide — Factorization_Euclidean_LightCone_latex

## Source
- arXiv official LaTeX source: `arxiv.org/e-print/1801.03917` (file
  `quasi-pseudo-pdf-matching-footnoteedit.tex`, revtex4-1, + apsrev .bbl +
  9 figure PDFs). Local library PDF used only as cross-check.
- Bibliography inlined verbatim from the source `.bbl`
  (`chapters/bbl.tex`); no entries changed.

## Normalization
- `revtex4-1 (twocolumn)` → `\documentclass[11pt]{article}` + geometry,
  amsmath/amssymb/mathtools/graphicx/microtype/enumitem/url/bm/xspace/
  slashed/hyperref(hidelinks). Unused REVTeX-only packages (`mathrsfs`,
  `ulem`) dropped; unused draft macros (`\adrop`) removed.
- `widetext` environment kept as a no-op shim (single-column).
- Title block rebuilt manually (title/authors/affiliations) with a
  footnote-style line: preprint MIT-CTP 4960, PRD 98, 056004 (2018),
  DOI 10.1103/PhysRevD.98.056004, arXiv:1801.03917.
- Figures copied from the arXiv source to `images/`; `\includegraphics`
  paths updated to `images/…​.pdf` (original omitted the `.pdf`
  extension).

## Known compromises / fixes (content untouched otherwise)
1. Several multi-row `align`s in the original rely on `\left … \right`
   pairs split across a `\\` row break (tolerated by the original
   REVTeX setup). In plain article+amsmath these raise "Extra }" errors.
   Affected displays (Eq. 1loopdiagram sail rows and Eq. 1loopioffe)
   were made row-local by replacing only the offending delimiters with
   plain `\Bigg\{ \Bigg\}` / `\Biggl[ \Biggr]`; equation content and
   numbering unchanged.
2. Stray trailing `\nn\\` inside three single-display `eqnarray`s
   (eq:qpdf, eq:def-moments, eq:equiv) removed so that the labeled
   equation carries its own number instead of an empty extra row.
   Likewise, in ~15 labeled multi-row aligns the `\nonumber` was on the
   row carrying the label (making `\ref` resolve to a stale number);
   `\nn` placements were shifted so each labeled display gets exactly
   one correct number. No text or math symbols were altered.
3. Unicode curly quotes in one acknowledgment sentence replaced by
   LaTeX `` '' quotes.
4. Equation numbering is continuous per article default (not the PRD
   section-based style); all internal references resolve consistently.
