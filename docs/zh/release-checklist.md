# 发布检查单

## 构建前

- [ ] `pyproject.toml` 与 `myqcd/__init__.py` 版本一致。
- [ ] `git ls-files pyproject.toml MANIFEST.in myqcd/py.typed` 非空。
- [ ] `python -m pytest`（允许 11 个已知 `refer/papers` 失败）。
- [ ] `python -m myqcd.operator_audit` 返回 48/48。
- [ ] `python -m sphinx -b html -W docs/en ...` 与 `docs/zh` 成功。

## 构建

```bash
rm -rf build dist myqcd.egg-info
python -m build --sdist --no-isolation
python -m twine check dist/*
```

## 远端检查

- [ ] 在全新 venv 中 `pip install --index-url https://pypi.org/simple myqcd==<ver>`。
- [ ] 源码树外 `python -m myqcd` 返回 `verified_core_without_inventory`。
- [ ] `python -m myqcd.operator_audit` 返回 48 项检查。
- [ ] PyPI JSON 只有 sdist 和六个 project links。
- [ ] RTD `myqcd` 与 `myqcd-zh` 构建当前提交。

## 交付

```bash
gpush.sh
gpush.sh -t gitee.com
```

- [ ] 本地/GitLab/Gitee HEAD 一致。
- [ ] 不强推、不改写标签。
- [ ] 日志归档，`logs/AGENTS.md` 末尾无空行。
