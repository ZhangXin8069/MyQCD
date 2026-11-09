# myqcd PyPI 发布台账（2026-11-09）

> 判定口径：以 `pip install myqcd==<ver>` 从 PyPI 远程安装到全新 venv 的结果为准。
> 本地 sdist 与源码树 import 只作为构建前证据。

## 发布事实

| 项 | 值 |
|---|---|
| 分发名 | `myqcd` |
| 导入名 | `myqcd` |
| 版本 | `0.1.0` |
| 上传物 | 仅 sdist：`dist/myqcd-0.1.0.tar.gz` |
| 用户名 | `TWINE_USERNAME=__token__` |
| 凭据变量 | `PYPI_ZHANGXIN8069_API_KEY`（只从 `~/env-key.sh` 读取，不落盘） |
| 项目页 | <https://pypi.org/project/myqcd/0.1.0/> |
| 文档站 | <https://myqcd.readthedocs.io/>（配置就绪，线上项目待网页绑定） |

## 验收清单

| # | 检查项 | 证据 | 状态 |
|---|---|---|---|
| 1 | 版本一致 | `pyproject.toml` 与 `myqcd/__init__.py` 均为 `0.1.0` | ✅ |
| 2 | `twine check` | `dist/myqcd-0.1.0.tar.gz: PASSED` | ✅ |
| 3 | sdist 含 `py.typed` | `tar -tzf ... | grep -c myqcd/py.typed` → 1 | ✅ |
| 4 | sdist 不含测试 | `myqcd/testing/` 命中数 0 | ✅ |
| 5 | sdist 不含 `AGENTS.md` | 命中数 0 | ✅ |
| 6 | `SOURCES.txt` 无家目录绝对路径 | `/home/` 命中数 0 | ✅ |
| 7 | 构建无弃用/绝对路径告警 | `grep -iE "deprecat|path must be relative"` → 空 | ✅ |
| 8 | 干净 venv 安装本地 sdist | `myqcd.__file__` 含 `site-packages`；26 项审计 verified | ✅ |
| 9 | PyPI 上传 | `twine upload` exit 0 | ✅ |
| 10 | simple index 传播 | 轮询立即出现 `myqcd-0.1.0.tar.gz` | ✅ |
| 11 | PyPI 远程安装 | 新 venv `pip install myqcd==0.1.0` exit 0；版本/路径/代数检查通过 | ✅ |
| 12 | 双远端推送 | gitlab.itp.ac.cn + gitee.com（见最终日志） | 待推送 |
| 13 | Read the Docs 双语言构建 | `sphinx -W docs/en` 与 `docs/zh` 均 `build succeeded.` | ✅ |
| 14 | 双语代码块逐字节一致 | overview/usage/install 的围栏块完全一致 | ✅ |
| 15 | 文档示例可执行 | `usage.md` 的 3 个 python 块顺序执行通过 | ✅ |
| 16 | RTD 线上项目 | 未提供 RTD token，未执行网页注册/绑定 | 未验证 |

## 构建与安装证据

```text
Successfully built myqcd-0.1.0.tar.gz
Checking dist/myqcd-0.1.0.tar.gz: PASSED
members=30
```

干净 venv（先本地 sdist，后 PyPI 远程）：

```text
version: 0.1.0
file: .../site-packages/myqcd/__init__.py
installed-package checks: OK
status: verified, check_count: 26, failed_checks: 0
```

## 证据边界

- 仅发布 sdist；纯 Python 包，wheel 可选但本次未上传。
- 完整测试在 Python 3.12 + SymPy 1.14 上执行；3.10/3.11/3.13 未自动验证。
- Read the Docs 源文件与本地构建已验证，但线上项目 slug `myqcd` 是否已创建、
  是否绑定两个语言版本，取决于 Read the Docs 账号侧操作，本次未执行。
- 颜色约定：新 `myqcd.color` 为厄米 `+δ^{ab}/2`；历史 `derivations.py` 为
  反厄米 `-δ^{ab}/2`，不可混用。
