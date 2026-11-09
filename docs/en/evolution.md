# Evolution

`myqcd.evolution` implements the single-exponent RGE solution

$$
Z(\mu)=\left(\frac{\mu}{\mu_0}\right)^{-\gamma},
\qquad
\gamma=-\frac{d\log Z}{d\log\mu}.
$$

For a diagonal anomalous-dimension matrix the evolution matrix is diagonal;
non-diagonal mixing requires matrix exponentiation and is outside this
helper.

## Reproduce

```python
import sympy as sp

from myqcd import evolution

mu = sp.Symbol("mu", positive=True)
mu0 = sp.Symbol("mu0", positive=True)

z = evolution.solve_z(mu, mu0, 1)
assert sp.simplify(z - mu0 / mu) == 0
assert evolution.evolution_residual(3, 1, mu0, mu) == 0
assert sp.simplify(
    evolution.anomalous_dimension_from_z(z, mu) - 1
) == 0
print(evolution.evolution_table())
```

## Comparison

| Input | Evolved factor |
|---|---|
| $\gamma=0$ | 1 |
| $\gamma=1$ | $\mu_0/\mu$ |
| $\gamma=-1$ | $\mu/\mu_0$ |

The sign convention is fixed by the equation above; a different convention
changes the exponent sign.
