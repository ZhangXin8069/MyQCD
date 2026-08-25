# Conversion Guide

- Source: arXiv:1810.00048v2 [hep-ph] official e-print (`arxiv.org/e-print/1810.00048`),
  gzip tar containing `BVZ-corr.tex`, `BVZ-corr.bbl`, `BVZplots/` (12 PDF figures).
- Title: "Power corrections and renormalons in parton quasi-distributions"
  by V. M. Braun, A. Vladimirov, J.-H. Zhang (Univ. Regensburg).
- Normalization: REVTeX4-1 two-column replaced by `article` 11pt + geometry;
  unified packages amsmath/amssymb/mathtools/graphicx/microtype/enumitem/url/hyperref(hidelinks).
- Package substitutions: `slashed` -> hand-written `\slashed{#1}{=}\!\!\!/` macro;
  MnSymbol/dsfont/bbold/marvosym/SIunits were loaded but never used in the body and dropped.
  `widetext` environment defined as no-op (single column).
- Body text kept verbatim (abstract, footnotes, acknowledgements, appendix);
  PACS numbers moved to the `\date` line; title block rebuilt in standard LaTeX.
- Figures: original `BVZplots/*.pdf` copied to `images/BVZplots/`; all 12 used, no placeholders.
- Bibliography: pre-generated `BVZ-corr.bbl` (69 entries) appended verbatim to
  `chapters/backmatter.tex`; apsrev helper macros are self-defined inside the .bbl.
- Structure: main.tex + chapters/section01..05.tex + chapters/backmatter.tex
  (acknowledgements + Appendix A + bibliography).
- Known compromises: none content-related; numbering is article default (single column),
  equation/table numbering may differ from the PRD printed version only by layout.
