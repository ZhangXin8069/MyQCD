# Operator basis

`myqcd.operator_basis` extends the 16 Dirac bilinears with derivative count,
color representation, chiral combinations and Fierz rearrangement. The
structure is

$$
\mathcal{O}_{\Gamma}^{(n)}
=\bar q\,\Gamma\,D^{(n)}q,
\qquad
\dim\mathcal{O}=3+n.
$$

## Derivative operators

`DerivativeOperator` stores the Dirac structure, derivative count, color
representation and flavor labels. `mass_dimension` is $3+n$; `parity_sign`
and `charge_conjugation_sign` are inherited from the zero-derivative
bilinear. The class does not model symmetrization, tracelessness or
equation-of-motion reduction.

| Derivatives $n$ | Mass dimension |
|---|---|
| 0 | 3 |
| 1 | 4 |
| 2 | 5 |
| 3 | 6 |

## Chiral combinations

With $P_{L,R}=(1\mp\gamma_5)/2$,

$$
V_\mu\pm A_\mu
=\gamma_\mu(1\pm\gamma_5)
=2\gamma_\mu P_{R,L}.
$$

The projector identities $P_L^2=P_L$, $P_R^2=P_R$, $P_LP_R=0$ and
$P_L+P_R=1$ are checked exactly.

## Color representation

A singlet bilinear carries color factor $1$; an octet bilinear carries
$T^a$ with $a=1,\dots,8$. The index is explicit so that color contractions
can be audited separately.

## Reproduce

```python
import sympy as sp

from myqcd import operator_basis

operators_list = operator_basis.enumerate_derivative_operators(
    ("u", "d"), max_derivatives=2, colors=("singlet", "octet")
)
assert len(operators_list) == 384

operator = operator_basis.DerivativeOperator(
    "O_twist2", "V3", derivatives=2, color="octet"
)
assert operator.mass_dimension == 5
assert operator.pyqcd_gamma_index == 3
assert operator.label == "V"

assert all(operator_basis.chiral_projector_identities().values())
assert operator_basis.color_factor("octet", 3) == "T^3"

terms = operator_basis.fierz_rearrangement("S", "V1")
assert terms
print(len(terms), operator_basis.color_factor("singlet"))
```

## Comparison with standard counting

| Item | MyQCD | Standard |
|---|---|---|
| Dirac bilinears | 16 | $1+1+4+4+6$ |
| Structure × derivatives × flavor × color | $16\times(n+1)\times N_f^2\times2$ | same |
| $n=2$, $N_f=2$, both colors | 384 | 384 |
| Mass dimension at $n$ derivatives | $3+n$ | $3+n$ |

The counting is combinatorial; it does not claim that all operators are
independent after equations of motion or Fierz identities.
