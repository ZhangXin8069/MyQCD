# 安装

```bash
pip install myqcd
```

依赖：

- Python 3.10 或更新版本；
- SymPy 1.12 或更新版本。

完整测试套件当前在 Python 3.12 + SymPy 1.14 上执行。Python 3.10、3.11 与
3.13 已声明并预期可用，但未在本机自动验证。

## 源码安装

```bash
pip install .
```

## 文档构建

```bash
python -m sphinx -b html -W docs/en docs/en/_build
```

## 证据边界

安装包后可以使用代数、算符与图层。`python -m myqcd` 入口还需要源码仓库中的
`refer/papers/INDEX.md`；纯安装环境请改用
`python -m myqcd.operator_audit`。
