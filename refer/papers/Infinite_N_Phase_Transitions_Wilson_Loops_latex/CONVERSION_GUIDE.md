# Conversion guide

- Source: official arXiv e-print `hep-th/0601210` (paper.tex + reflist.tex + 9 EPS figures).
- Class normalized: JHEP3.cls -> standard `article` 11pt, geometry a4 margin 2.5cm,
  packages amsmath/amssymb/mathtools/graphicx/microtype/enumitem/url/hyperref(hidelinks).
- Macros mapped: `\FIGURE[ht]{..}` -> figure env; `\epsfig{file=x.eps}` ->
  `\includegraphics{images/x.pdf}`; `\email` -> mailto `\href`; `\acknowledgments` ->
  `\section*`; eqnarray `\cr` -> `\\`. Original `\be/\ee`, labels, comments kept.
- Figures: all 9 EPS converted to PDF with ghostscript (`gs -sDEVICE=pdfwrite -dEPSCrop`),
  stored in `images/`; every figure available, no placeholders.
- Cross-reference fix: hard-coded textual range "equations (2.4-2.7)" (per-section JHEP
  numbering) re-labeled as (\ref{eq:smearA})--(\ref{eq:fnsol}) = new eqs (4)-(7);
  Langevin equation keeps label `langev`.
- Title-page footnote carries journal ref/arXiv/DOI (DOI follows the standard
  10.1088/1126-6708/2006/vol/page JHEP pattern [?]).
- Text preserved verbatim including source typos ("fitted he eigenvalue",
  "$\hat W[L_1,L_2,;f;n]$", duplicated "Nucl. Phys." in bibitem ape10);
  bibliography reproduced unchanged (comments included).
- Compile: xelatex twice into build/; result build/main.pdf, no errors, no undefined refs.
