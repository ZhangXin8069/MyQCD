# Figures in "Confinement of quarks" (Wilson, PRD 10, 2445)

All figures are cropped from the source PDF at 300 dpi into `images/`.
Each figure is a small line drawing inside one column of the two-column
Phys. Rev. layout; captions sit immediately below the figure.

| Figure | File | Caption |
|--------|------|---------|
| Fig. 1 | `images/fig1.png` | Speculative plot of photon mass vs renormalized charge `e`, in unknown units. The transition at `e_c` is second-order (see text). |
| Fig. 2 | `images/fig2.png` | Speculative plot of photon mass vs renormalized charge `e` if there is a first-order transition at `e_c`. |
| Fig. 3 | `images/fig3.png` | An example of quark (q) and antiquark (q̄) paths connecting the points 0 and x. |
| Fig. 4 | `images/fig4.png` | Example of current loop (as in Fig. 3) with extra vacuum loop. |
| Fig. 5 | `images/fig5.png` | Example of separate quark loops for the points 0 and x. (Integration over the gauge field produces gauge propagators which connect these loops.) |
| Fig. 6 | `images/fig6.png` | (a) Loop with well-separated quark and antiquark. (b) Loop with small separation between quark and antiquark. |
| Fig. 7 | `images/fig7.png` | Quark-antiquark loop with nearby vacuum loop. |
| Fig. 8 | `images/fig8.png` | Example of a lattice path P. |
| Fig. 9 | `images/fig9.png` | Elementary square on the lattice. |
| Fig. 10 | `images/fig10.png` | Filling of enclosed area of path P by elementary squares. |

## Extraction

`extract_figures.py` renders each hand-verified region (page, column,
y-range) with `pdftoppm` at 300 dpi and auto-crops to the ink bounding
box.  The regions were checked against the scan: each contains only the
figure content and its internal labels (e.g. "I", "e" for Fig. 1;
"+", "(0,0)", "(1,0)" for Fig. 8; "(o,o)" for Fig. 9) — no body text.

| Figure | Page | Column | y range (pt) |
|--------|------|--------|--------------|
| fig1 | 2 | R | 138–200 |
| fig2 | 2 | R | 640–703 |
| fig3 | 3 | L | 610–704 |
| fig4 | 3 | R | 135–212 |
| fig5 | 3 | R | 610–694 |
| fig6 | 4 | R | 135–216 |
| fig7 | 4 | R | 610–705 |
| fig8 | 6 | R | 135–204 |
| fig9 | 9 | R | 630–713 |
| fig10 | 10 | R | 590–701 |
