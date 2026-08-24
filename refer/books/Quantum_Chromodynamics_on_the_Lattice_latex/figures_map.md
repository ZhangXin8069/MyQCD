# Figure map

Extracted figures live in `images/` as PNG files (300 dpi crops of the original
pages).  Reference them in the LaTeX as `\includegraphics[width=...]{images/figXY.png}`.

| Figure   | Image file        | Chapter | Caption (from the book) |
|----------|-------------------|---------|--------------------------|
| Fig. 1.1 | `images/fig11.png`| 1       | A discretized path contributing in (1.37) |
| Fig. 2.1 | `images/fig21.png`| 2       | Schematic picture of the cubic and quartic gluon self-interaction |
| Fig. 2.2 | `images/fig22.png`| 2       | The link variables $U_\mu(n)$ and $U_{-\mu}(n)$ |
| Fig. 2.3 | `images/fig23.png`| 2       | The four link variables which build up the plaquette $U_{\mu\nu}(n)$ |
| Fig. 3.1 | `images/fig31.png`| 3       | Integrating out the common link of a product of two plaquettes |
| Fig. 3.2 | `images/fig32.png`| 3       | Sketch of a maximal tree on a 2D sublattice |
| Fig. 3.3 | `images/fig33.png`| 3       | Examples for a planar and a nonplanar loop |
| Fig. 3.4 | `images/fig34.png`| 3       | Leading contribution in the strong coupling (small $\beta$) expansion |
| Fig. 3.5 | `images/fig35.png`| 3       | Numerical data for the static quark potential |
| Fig. 4.1 | `images/fig41.png`| 4       | Schematic sketch of a Markov chain in the space of all configurations |
| Fig. 4.2 | `images/fig42.png`| 4       | The plaquette expectation value $E_P$ as a function of $\beta$ |
| Fig. 4.3 | `images/fig43.png`| 4       | The static potential $V$ for SU(3) gauge theory |
| Fig. 5.1 | `images/fig51.png`| 5       | The propagator from $n$ to $m$ is a sum over paths of link variables |
| Fig. 6.1 | `images/fig61.png`| 6       | Connected (l.h.s.) and disconnected (r.h.s.) contributions |
| Fig. 6.2 | `images/fig62.png`| 6       | Sample of quark lines contributing in hadron propagation |
| Fig. 6.3 | `images/fig63.png`| 6       | Result of a Monte Carlo simulation on a $16^3\times 32$ lattice |
| Fig. 6.4 | `images/fig64.png`| 6       | Raw data for hadron masses |
| Fig. 6.5 | `images/fig65.png`| 6       | Quenched light hadron spectrum compared with experiments |
| Fig. 7.1 | `images/fig71.png`| 7       | Allowed regions for the eigenvalues $\lambda$ of a Ginsparg–Wilson Dirac operator |
| Fig. 7.2 | `images/fig72.png`| 7       | Lattice results for the bare condensate |
| Fig. 8.1 | `images/fig81.png`| 8       | The phase diagram for QCD with Wilson fermions |
| Fig. 8.2 | `images/fig82.png`| 8       | Spectroscopy results from a fully dynamical simulation |
| Fig. 9.1 | `images/fig91.png`| 9       | Graphical representation of the sum $Q_{\mu\nu}(n)$ of plaquettes |
| Fig. 9.2 | `images/fig92.png`| 9       | Example of an overlapping discrete block spin transformation |
| Fig. 11.1| `images/fig111.png`| 11      | Propagation of a pion |
| Fig. 11.2| `images/fig112.png`| 11      | Behavior of the wave function in a box |
| Fig. 11.3| `images/fig113.png`| 11      | Relation between scattering phase shifts and the two-particle energy |
| Fig. 11.4| `images/fig114.png`| 11      | Matrix elements of operators between mesonic states |
| Fig. 11.5| `images/fig115.png`| 11      | Schematic diagram for the matrix element (11.98) |
| Fig. 12.1| `images/fig121.png`| 12      | Expectation value $|\langle P\rangle|$ as function of temperature $T$ |
| Fig. 12.2| `images/fig122.png`| 12      | Phase structure in the $(T,m)$-plane |
| Fig. 12.3| `images/fig123.png`| 12      | Sketch of the phase structure in the $(T,m_{u,d},m_s)$-space |
| Fig. 12.4| `images/fig124.png`| 12      | Pressure $p$ determined from simulations for pure SU(3) gauge theory |
| Fig. 12.5| `images/fig125.png`| 12      | The conjectured phase diagram in the $(T,\mu)$-plane |

All figures use `\graphicspath{{images/}}` set in `main.tex`, so
`\includegraphics[width=\textwidth]{figXY.png}` also resolves.
