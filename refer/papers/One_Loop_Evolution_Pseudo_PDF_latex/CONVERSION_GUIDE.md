# Conversion Guide — One_Loop_Evolution_Pseudo_PDF_latex

## Source
- arXiv:1801.02427v3 [hep-ph] (3 Jul 2018), official TeX source
  (`https://arxiv.org/e-print/1801.02427`, single file `psevol0702.tex`
  in revtex4-1 twocolumn + 13 PDF figures).
- Published as Phys. Rev. D 98, 014019 (2018);
  DOI: 10.1103/PhysRevD.98.014019 (journal ref verified on arxiv.org abs page).

## Normalization
- `\documentclass[11pt]{article}` + `geometry` (a4paper, margin 2.5cm);
  packages amsmath/amssymb/mathtools/graphicx/microtype/enumitem/url/hyperref(hidelinks).
- REVTeX removed; two-column -> single column; PACS block moved under the
  abstract as plain text; title-block footnote carries arXiv id / PRD DOI.
- Original macros kept where used by body text (`\nn`, `\gsim`, `\lsim`).
- Body text transcribed verbatim from the source, including abstract,
  acknowledgements and all 30 bibliography entries (thebibliography kept
  verbatim in `chapters/backmatter.tex`).
- Sections split into `chapters/section01..05.tex`; `\acknowledgements`
  replaced by `\section*{Acknowledgements}`.
- Figures: 11 referenced PDF figures copied from the arXiv source into
  `images/` and included via relative paths (`images/xxx`). `mu21new.pdf`
  was unused by the source and is not shipped.

## Known compromises
- Negative `\vspace` tweaks of the two-column layout removed (single-column
  normalization); figure widths kept at original inch values.
- Inline commented-out fragments of the source were dropped exactly as the
  original compiler would have (e.g. "The curve itself corresponds to"
  fragment was commented out upstream).
