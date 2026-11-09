# Conversion Guide

- **Source**: arXiv:1310.7471 official e-print tarball (v1, Oct 2013), file `matching1.tex` + `vertex.eps`/`self.eps`. No local library PDF.
- **Normalization**: revtex4 (prd, preprint) → `article` 11pt + geometry a4paper margin 2.5cm; unified packages amsmath/amssymb/mathtools/graphicx/microtype/enumitem/url/hyperref(hidelinks). REVTeX-only macros (`\affiliation`, epsfig/psfrag/colordvi/slashed/enumerate/bm) removed; unused custom preamble macros dropped. Body text, equations (incl. hard-coded Eq./Sec. numbers), comments in bibliography kept verbatim.
- **Title block**: rebuilt for article class; author corrected "Xiaonu Xiong" (arXiv v1 typo) → "Xin Xiong" per published PRD 90, 014051 (2014); footnote carries DOI + arXiv id.
- **Figures**: EPS converted with epstopdf → `images/vertex.pdf`, `images/self.pdf`; original `.eps` also stored. Figure 1 layout preserved (side-by-side).
- **Structure**: main.tex + chapters/section01–05.tex + chapters/backmatter.tex (acknowledgments moved to end of section05; thebibliography verbatim incl. pseudo-items `footnote`, `footnote1`, `axial`, `negele`, `ren`).
- **Known compromises**: commented-out draft paragraphs in the source (intro alternatives, Z(-xi) remark) omitted as they are non-printing comments; equation order untouched so all textual references (Eq. (1), Eq. (12)) match original numbering.
