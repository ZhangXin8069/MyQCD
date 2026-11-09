# Case studies

## Case 1: pion interpolating operator

The operator $\bar u\gamma_5d$ has $J^P=0^-$, $C=+1$, mass dimension 3 and
PyQCD index 5. Its matrix element is not computed here; the row only fixes
the exact algebraic labels.

## Case 2: vector meson

$\bar u\gamma_4d$ is the temporal vector structure `V4`: parity $+1$,
$C=-1$, dimension 3, index 4. Spatial components `V1`–`V3` have parity
$-1$; the component label matters.

## Case 3: axial meson

$\bar u\gamma_4\gamma_5d$ is `A4`: parity $-1$, $C=-1$, index 15. The
spatial axial structures `A1`–`A3` have parity $+1$ and $C=+1$.

## Case 4: Fierz rearrangement of a scalar product

For $(\bar\psi_1\psi_2)(\bar\psi_3\psi_4)$, the $S$–$S$ coefficients are
$+1/4$ for $S,P,V_1,\dots,V_4$ and $-1/4$ for
$A_1,\dots,A_4,T_{12},\dots,T_{34}$. The matrix identity and random-spinor
test both pass; the overall Grassmann convention is stated separately.

## Case 5: one-loop self-energy

The diagram has $V=2$, two internal edges (quark and gluon), $C=1$ and
$L=1$. The two external quark legs are stubs and do not enter
$E_{\mathrm{int}}$. The SVG and TikZ exporters place the two internal lines
on separated curves.

## Case 6: sunset

Three internal gluons between two vertices give $V=2$, $E_{\mathrm{int}}=3$,
$C=1$ and $L=2$. The topology layer reports the same loop number without
assigning a symmetry factor; that requires the identical-particle
convention.

## Case 7: color trace

$\mathrm{Tr}[T^1T^2T^3]=i/4$; the imaginary part comes from $f^{123}=1$.
$\mathrm{Tr}[T^1T^1T^8]=\sqrt3/12$; the real part comes from
$d^{118}=1/\sqrt3$. These values are checked against explicit Gell-Mann
matrices.

## Case 8: Landau-gauge transversality

The gluon propagator satisfies
$p_\mu D^{\mu\nu}=\xi p^\nu/p^2$. Only at $\xi=0$ does the contraction
vanish. The test suite checks both the Landau zero and the Feynman-gauge
non-zero value.

## What the cases do not show

They do not provide numerical matrix elements, loop integrals, symmetry
factors or continuum extrapolations. Each case is an exact algebraic
checkpoint with a declared boundary.
