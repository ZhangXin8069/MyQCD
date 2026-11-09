# Troubleshooting

## `python -m myqcd` reports `verified_core_without_inventory`

`refer/papers/INDEX.md` is missing. The core checks still ran; the paper
inventory was skipped. This is expected outside the source checkout.

## `pip install myqcd==<ver>` says no matching distribution

The PyPI simple index edge may lag behind the JSON API. Retry after a few
seconds; do not rebuild or re-upload the same version.

## A fresh clone cannot build the sdist

Check that `pyproject.toml`, `MANIFEST.in` and `myqcd/py.typed` are tracked.
The whitelist `.gitignore` hides extensionless files unless an exception is
present.

## `T13` has no PyQCD index

PyQCD stores `gamma(7)=gamma3 gamma1=-sigma13`. The exact `sigma13` matrix
has no entry; `pyqcd_gamma_index` returns `None` instead of silently
changing the sign.

## Fierz signs look different from a Mathematica reference

Check the metric, gamma basis, Grassmann convention and the dual-basis
normalization. A Minkowski reference cannot be compared coefficient by
coefficient without a basis conversion.

## RTD still shows the old page

Check the builds API commit and state; the site may still be serving the
previous successful build. The Markdown source and the build commit must
match.

## `gpush.sh` aborts with staged submodule changes

Commit the gitlink explicitly first. `gpush.sh` refuses to rewrite submodule
pointers from the working tree.

## `logs/AGENTS.md` whitespace error

The log writer can leave a blank line at EOF. Remove it and rerun
`git diff --check` before committing.
