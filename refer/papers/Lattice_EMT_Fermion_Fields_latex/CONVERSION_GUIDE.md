# CONVERSION GUIDE

- Source: arXiv:1403.4772 official LaTeX source (e-print tarball), main file
  `EM_fermion_ptep_ver5.tex` (PTEP `ptephy.cls`, v5, 2015-06-17).
- Normalized to `article` class per SPEC: geometry/a4, amsmath+amssymb+mathtools,
  graphicx, booktabs, microtype, enumitem, url, hyperref(hidelinks);
  `\numberwithin{equation}{section}` keeps the original per-section numbering.
- ptephy-specific macros removed (`\preprintnumber`, `\subjectindex`, author-block
  macros); their information moved into the title block / center line.
- Fallbacks added: `\providecommand{\Tilde}`, `\providecommand{\Bar}` (LaTeX>=2020
  kernel has them natively). Unused `\newtheorem*{lem}` dropped.
- Figures: all 46 used EPS diagrams (A03-A19, B03-B18, C01-C05, D01-D08) converted
  with epstopdf into `images/*.pdf`; referenced as `images/NAME`.
  Figure captions are the bare diagram codes (C01, ...), kept verbatim from source.
- Tables 0-4 kept as original LaTeX code (booktabs). Commented-out material of the
  source retained as comments.
- Content preserved verbatim incl. abstract, footnotes, acknowledgments,
  appendices A-E and `thebibliography` (in chapters/backmatter.tex).
