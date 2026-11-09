# Release checklist

## Before building

- [ ] `pyproject.toml` and `myqcd/__init__.py` versions match.
- [ ] `git ls-files pyproject.toml MANIFEST.in myqcd/py.typed` nonempty.
- [ ] `python -m pytest` (11 known `refer/papers` failures allowed).
- [ ] `python -m myqcd.operator_audit` returns 48/48.
- [ ] `python -m sphinx -b html -W docs/en ...` and `docs/zh` succeed.

## Build

```bash
rm -rf build dist myqcd.egg-info
python -m build --sdist --no-isolation
python -m twine check dist/*
```

## Remote checks

- [ ] `pip install --index-url https://pypi.org/simple myqcd==<ver>` in a
      fresh venv.
- [ ] `python -m myqcd` returns `verified_core_without_inventory` without a
      source checkout.
- [ ] `python -m myqcd.operator_audit` returns 48 checks.
- [ ] PyPI JSON has only sdist and six project links.
- [ ] RTD `myqcd` and `myqcd-zh` build the current commit.

## Delivery

```bash
gpush.sh
gpush.sh -t gitee.com
```

- [ ] Local/GitLab/Gitee HEAD match.
- [ ] No force push and no rewritten tags.
- [ ] Log archived and `logs/AGENTS.md` has no blank line at EOF.
