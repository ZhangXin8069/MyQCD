# 排错

## `python -m myqcd` 报告 `verified_core_without_inventory`

缺少 `refer/papers/INDEX.md`。核心检查仍执行，论文清单被跳过；在源码
仓库之外这是预期行为。

## `pip install myqcd==<ver>` 报 no matching distribution

PyPI simple index 的边缘节点可能落后于 JSON API。等待几秒后重试；不要
重建或重传同一版本。

## 全新克隆无法构建 sdist

检查 `pyproject.toml`、`MANIFEST.in` 与 `myqcd/py.typed` 是否被跟踪。
白名单 `.gitignore` 会隐藏 extensionless 文件，除非加入例外。

## `T13` 没有 PyQCD 索引

PyQCD 中 `gamma(7)=gamma3 gamma1=-sigma13`。精确的 `sigma13` 矩阵没有
对应项；`pyqcd_gamma_index` 返回 `None`，不会静默改号。

## Fierz 符号与 Mathematica 参考不同

检查度规、gamma 基、Grassmann 约定与对偶基归一化。Minkowski 参考不能
不做基变换就逐系数比较。

## RTD 仍显示旧页面

检查 builds API 的 commit 与 state；站点可能仍在服务上一次成功构建。
Markdown 源与构建 commit 必须一致。

## `gpush.sh` 因已暂存子模块变更而中止

先显式提交 gitlink。`gpush.sh` 拒绝从工作树重写子模块指针。

## `logs/AGENTS.md` 空白错误

日志写入器可能在 EOF 留下空行。删除后重跑 `git diff --check` 再提交。
