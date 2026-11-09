# Glossary

**Bilinear.** A quark-antiquark structure $\bar q\,\Gamma q$ with one of the
16 Dirac matrices $\Gamma$.

**Clover.** The symmetric four-plaquette lattice field strength
$F_{\mu\nu}=-i/8\sum(P-P^\dagger)$.

**DeGrand–Rossi (DR) basis.** The Euclidean gamma representation used by
PyQCD: $\gamma(0)=I$, $\gamma(4)$ is temporal and
$\gamma_5=\mathrm{diag}(1,1,-1,-1)$.

**Dirac structure.** One of $S,P,V_\mu,A_\mu,T_{\mu\nu}$ in the 16-bilinear
basis.

**Effective mass.** $m_{\mathrm{eff}}(t)=\log[C(t)/C(t+1)]$.

**Epsilon tensor.** The totally antisymmetric $\varepsilon_{\mu\nu\rho\sigma}$
with $\varepsilon_{0123}=+1$.

**Fierz transformation.** A rearrangement of
$(\bar\psi_1\Gamma_A\psi_2)(\bar\psi_3\Gamma_B\psi_4)$ into a sum of
$(\bar\psi_1\Gamma_C\psi_4)(\bar\psi_3\Gamma_D\psi_2)$.

**Fermi sign.** The Grassmann parity of reordering fermion fields.

**Gradient flow.** A differential flow of gauge links that smears the field
at flow time $t$; the smoothing radius is $\sqrt{8t}$.

**Internal edge.** A diagram edge whose two endpoints are vertices;
external-leg edges have endpoint $-1$ and are excluded from
$E_{\mathrm{int}}$.

**Jackknife.** Leave-one-out resampling used to estimate the covariance of a
mean.

**Loop number.** $L=E_{\mathrm{int}}-V+C$ for a diagram with $C$ connected
components.

**Mixing matrix.** $Z_{ij}$ in
$\mathcal{O}_i^R=\sum_j Z_{ij}\mathcal{O}_j$.

**Momentum smearing.** A gauge-covariant phase applied to quark sources to
reach larger spatial momenta.

**Parity sign.** The sign $s$ in $\gamma_4\Gamma\gamma_4=s\Gamma$.

**RI/MOM.** A momentum-subtraction renormalization scheme defined at
$p^2=\mu^2$.

**Staple.** A three-segment Wilson path used in gluon TMD operators.

**Topology.** The combinatorial graph of vertices and edges, independent of
particle labels and momenta.

**Twist.** The difference between mass dimension and spin projection; a
leading-twist bilinear has dimension $3+n$ with $n$ derivatives.

**Wick contraction.** A pairing of quark and antiquark fields with the
corresponding Grassmann sign.

**Wilson line.** A path-ordered product of gauge links
$W(x,y)=\prod U_\mu$.

**Z factor.** The renormalization constant multiplying an operator or field.

**Symmetry factor.** The inverse of the automorphism count of a diagram. It
is **not** assigned automatically by `myqcd.topology`; the particle content
and exchange conventions must be supplied explicitly.
