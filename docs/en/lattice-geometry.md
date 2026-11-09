# Lattice geometry

`myqcd.lattice` provides integer-index momenta, Fourier phases, lattice
dispersion and small momentum enumerations.

## Momenta and phases

For a lattice extent $L_\mu$ and integer index $n_\mu$,

$$
p_\mu=\frac{2\pi n_\mu}{L_\mu},
\qquad
e^{-ip\cdot x}.
$$

The lattice dispersion for spacing $a$ is

$$
\hat p^2=\frac{4}{a^2}\sum_\mu\sin^2\left(\frac{p_\mu a}{2}\right),
$$

which reduces to $\sum_\mu p_\mu^2$ for $p_\mu a\ll1$.

## Reproduce

```python
import math

from myqcd import lattice

p = lattice.momentum_from_indices((1, 0, 0, 0), (4, 4, 4, 8))
assert p[0] == math.pi / 2
phase = lattice.fourier_phase((math.pi / 2, 0, 0, 0), (1, 0, 0, 0))
assert abs(phase - (-1j)) < 1e-12
assert lattice.lattice_dispersion((0.1, 0.2)) > 0
assert lattice.lattice_dispersion((0.0, 0.0)) == 0
momenta = lattice.spatial_momenta((4, 4), max_index=1)
assert len(momenta) == 9
print(lattice.momentum_permutations((1.0, 0.0, 0.0)))
```

## Comparison with the continuum

| Quantity | Lattice | Continuum limit |
|---|---|---|
| Momentum | $2\pi n_\mu/L_\mu$ | same |
| Dispersion | $4a^{-2}\sum\sin^2(p_\mu a/2)$ | $\sum p_\mu^2$ |
| Phase | $e^{-ip\cdot x}$ | same |

The dispersion comparison is exact at finite $a$; the continuum expression is
the $a\to0$ limit, not an identity at finite spacing.
