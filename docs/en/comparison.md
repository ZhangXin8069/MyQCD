# Comparison with reference libraries

| Project | Role | License | What `myqcd` takes |
|---|---|---|---|
| PyQCD | lattice-QCD numerical package | MIT | DR gamma conventions, operator naming |
| FeynCalc | Mathematica gamma/color algebra | GPL-3.0 | mathematical identities, reference only |
| LQCD_Wickcontraction_reduce | Wick reduction | no LICENSE | algorithmic ideas, reference only |
| pyfeyn2 | Python Feynman diagrams | GPL-3.0 | renderer interface ideas, reference only |
| pyfeyngen | particle syntax -> TikZ | MIT | export workflow ideas |

`myqcd` does not copy GPL-3.0 or unlicensed source. Every implemented
identity is independently rewritten and tested; external repositories are
read-only submodules.

## Structural differences

- PyQCD performs numerical tensor contractions; `myqcd` checks exact algebra.
- FeynCalc is a Mathematica package; `myqcd` is Python/SymPy and zero-extra
  dependency for the operator/diagram layer.
- pyfeyn2 has richer automatic layouts; `myqcd` provides a zero-dependency
  subset with explicit topology invariants.
- `myqcd` deliberately omits loop integrals and ensemble fits.

## Compatibility notes

Gamma signs and color normalization are convention-dependent. The
`myqcd.color` layer uses $+\delta^{ab}/2$; the historical
`myqcd.derivations` SU(3) code uses $-\delta^{ab}/2$. A cross-library
numerical comparison must first convert the basis and normalization.
