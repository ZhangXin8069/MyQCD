# Conversion guide

- Source: arXiv:1006.4518 official TeX source (e-print tarball, plain TeX
  with CERN `format`/`macros` files), fetched from arxiv.org.
- Normalization: plain-TeX source converted to standard LaTeX
  (`article`, 11pt, a4paper/2.5cm margins). Original `\equation/\enum/\nexteq`
  displays mapped to `equation/align/split`; global sequential equation
  numbering (article default) replaces the per-section (1.1),(2.1),... scheme;
  all in-text references converted to `\eqref/\ref`.
- Original macros kept as newcommands (`\rmd,\rme,\rmO,\Sw,\Nf,\MSbar,
  \euler,\SUthree,...`); plain-TeX `\Re` redefined as operator Re;
  `\cases` replaced by amsmath `cases`.
- Figures: original EPS plots (plots/*.eps) converted to PDF via ghostscript
  (`gs -dEPSCrop`); included from `images/`. All 4 figures present.
- Table 1 re-set as a LaTeX `tabular`; data unchanged.
- Bibliography: all 20 items of the original `biblio` file kept verbatim
  in `chapters/backmatter.tex` (only markup translated: `{\it ...}` ->
  `\textit{...}`).
- Acknowledgements moved from end of sect.~5 to an unnumbered section in
  backmatter (per house style). Footnote dagger marker dropped (LaTeX
  auto-numbering).
- Content is verbatim; no text added or removed.
