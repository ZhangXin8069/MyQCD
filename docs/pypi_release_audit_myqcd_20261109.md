# myqcd PyPI 发布台账（2026-11-09）

> 判定口径：以 `pip install myqcd==<ver>` 从 PyPI 远程安装到全新 venv 的结果为准。
> 本地 sdist 与源码树 import 只作为构建前证据。

## 发布事实

| 项 | 值 |
|---|---|
| 分发名 | `myqcd` |
| 导入名 | `myqcd` |
| 版本 | `0.1.2`（当前；0.1.0 为首版） |
| 上传物 | 仅 sdist：`dist/myqcd-0.1.0.tar.gz`、`0.1.1`、`0.1.2` |
| 用户名 | `TWINE_USERNAME=__token__` |
| 凭据变量 | `PYPI_ZHANGXIN8069_API_KEY`（只从 `~/env-key.sh` 读取，不落盘） |
| 项目页 | <https://pypi.org/project/myqcd/0.1.2/> |
| 文档站 | <https://myqcd.readthedocs.io/>（线上项目已存在，中英文构建通过） |

## 发布记录

| 版本 | 变更 | 证据 |
|---|---|---|
| 0.1.0 | 首次发布：算符/费曼图层与打包接口 | `twine check` PASSED；PyPI 远程安装通过 |
| 0.1.1 | 修复默认 CLI 缺 `INDEX.md` 时 traceback；`operator_audit` 默认根改为当前目录；顶层子模块可发现；移除未使用导入 | 全量 161 passed（11 个 `refer/papers` 环境缺口）；PyPI 远程安装后 `python -m myqcd` 返回 `verified_core_without_inventory` |
| 0.1.2 | 修复外部腿边被计入圈数；TikZ 导出声明 `external` 顶点；根 README 改为英文默认并新增 `README.zh-CN.md`；补全 PyPI Project links | 全量 163 passed（11 个环境缺口）；PyPI 0.1.2 远程安装、CLI 与 Project links 全部通过 |

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
| 9 | PyPI 上传 | `twine upload` 三次均 exit 0（0.1.0、0.1.1、0.1.2） | ✅ |
| 10 | simple index 传播 | 三个版本均出现在 simple index；0.1.2 首次安装需重试一次（CDN 边缘滞后） | ✅ |
| 11 | PyPI 远程安装 | 新 venv 分别安装 0.1.0、0.1.1、0.1.2；版本/路径/代数检查通过 | ✅ |
| 12 | 双远端推送 | gitlab 260fc13、gitee 260fc13；GitHub 260fc13 | ✅ |
| 13 | Read the Docs 双语言构建 | `sphinx -W docs/en` 与 `docs/zh` 均 `build succeeded.` | ✅ |
| 14 | 双语代码块逐字节一致 | overview/usage/install 的围栏块完全一致 | ✅ |
| 15 | 文档示例可执行 | `usage.md` 的 3 个 python 块顺序执行通过 | ✅ |
| 16 | RTD 线上项目 | API：`myqcd` 与 `myqcd-zh` 存在；build commit 260fc13、state=finished；两站页面 200 | ✅ |
| 17 | 缺 `INDEX.md` 时默认 CLI 可用 | 安装环境 `python -m myqcd` exit 0，`status=verified_core_without_inventory` | ✅ 0.1.1 |
| 18 | `operator_audit` 默认根目录 | 安装环境从 `/tmp` 运行，输出写入 `/tmp/logs/data/operator_audit/` | ✅ 0.1.1 |
| 19 | 外部腿不计入圈数 | `E_int - V + C`；含 `-1` 端点的边不计入内部边 | ✅ 0.1.2 |
| 20 | TikZ 外部顶点 | 含外部腿时输出 `\vertex (external)` | ✅ 0.1.2 |
| 21 | 英文默认 README + 中文版 | `README.md` 英文、`README.zh-CN.md` 中文，sdist 同时包含两者 | ✅ 0.1.2 |
| 22 | PyPI Project links | JSON `project_urls` 含 Documentation/Homepage/GitLab/Gitee/GitHub/Issues 六项 | ✅ 0.1.2 |

## 构建与安装证据

```text
Successfully built myqcd-0.1.2.tar.gz
Checking dist/myqcd-0.1.2.tar.gz: PASSED
members=31
readme_en=1 readme_zh=1 py.typed=1 testing=0 agents=0
```

干净 venv（先本地 sdist，后 PyPI 远程）：

```text
version: 0.1.2
file: .../site-packages/myqcd/__init__.py
python -m myqcd: exit=0, status=verified_core_without_inventory
myqcd (console): exit=0, status=verified_core_without_inventory
operator_audit: status=verified, check_count=26
PyPI project_urls: 6 labels
```

0.1.0 的安装证据：

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
