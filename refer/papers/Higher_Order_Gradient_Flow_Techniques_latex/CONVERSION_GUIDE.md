# CONVERSION_GUIDE

- Source: arXiv:1905.00882v2 official LaTeX source (e-print tarball), paper = JHEP 06 (2019) 121
  (INSPIRE-confirmed; task hint "Eur. Phys. J. C" was wrong).
- Normalized per SPEC: article 11pt + geometry 2.5cm; removed epsf/scalefnt/rotating/fancyhdr/
  authblk/filemod/showlabels/tocstyle/ulem/cite packages; title block re-typeset by hand.
- `\abbrev` redefined as `{\small #1}` (was `\scalefont{.9}`); `slashed` package replaced by
  hand macro `\slashed{#1} := \not{#1}` in macros.tex; everything else verbatim from source.
- Figures: all PDFs from src figs/ + dias/ copied to images/, include paths rewritten
  `{dias/...}`,`{figs/...}` -> `{images/...}`. All figures available, no placeholders.
- Bibliography: gradflow-setup_ref.tex bibitems inlined into chapters/backmatter.tex with the
  original \bibentry/\journal/\arxiv* macros; entries unchanged.
- Known compromises: TOC style standard; original fancy header block (FERMILAB-PUB etc.) kept
  only in the title footnote; hyperref hidelinks instead of colored links.
