# Wilson lines

`myqcd.wilson` provides symbolic Wilson-path products and gauge-covariance
checks for 3x3 links. It stores matrices, not gauge-field arrays.

## Path product

$$
W(x,y)=U_0U_1\cdots U_{n-1}.
$$

Under a gauge transformation,

$$
U_i\mapsto G_iU_iG_{i+1}^\dagger,
\qquad
W\mapsto G_0WG_n^\dagger.
$$

The dagger path reverses the links and takes the Hermitian conjugate of each
one: $W^\dagger=U_{n-1}^\dagger\cdots U_0^\dagger$.

## Staple

A three-segment staple is described by

$$
(-L\hat z,\; b\hat b,\; (L+z)\hat z).
$$

`staple_descriptors(z,b,L)` returns these direction/length pairs.

## Reproduce

```python
import sympy as sp

from myqcd import wilson

links = (sp.diag(1, 1, -1), sp.diag(-1, 1, 1))
path = wilson.straight_path(links)
assert path.product() == links[0] * links[1]
assert path.dagger().product() == path.product().H

angles = (sp.Rational(1, 5), sp.Rational(2, 5), sp.Rational(3, 5))
gauges = tuple(
    wilson.unitary_phases(
        (sp.Rational(index, 7), sp.Rational(index + 1, 7), sp.Rational(index + 2, 7))
    )
    for index in range(4)
)
assert wilson.covariance_residual(links, gauges[:3]).is_zero_matrix
print(wilson.staple_descriptors(2, 1, 5))
```

## Boundary

The module checks the algebraic path product and covariance. It does not
read an ILDG configuration, smear links or evaluate a lattice contraction.
