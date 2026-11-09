# 迁移说明

## 从 PyQCD 约定迁移

- `gamma(0)` 是单位矩阵哨兵，`gamma(4)` 是时间分量。
- DR 基中 `gamma5 = diag(1,1,-1,-1)`；没有变换时不要替换成手征基。
- 历史 `_baroperator` 表中的 `gamma_mu` 代表元是时间分量；
  `myqcd.operators` 使用显式分量名（`V1`–`V4`）。

## 颜色归一化

历史 `myqcd.derivations` 的 SU(3) 代码使用反厄米归一化
`tr(T^aT^b) = -delta^{ab}/2`。`myqcd.color` 与 `myqcd.color_traces`
使用 `+delta^{ab}/2`。比较 Casimir 或 f/d 缩并前必须先转符号。

## Fierz 符号

Fierz 引擎使用对偶基与 Euclidean Gram 符号。Minkowski 或不同 gamma
表示需要先做基变换；不要直接搬系数。

## CLI 行为

缺 `refer/papers/INDEX.md` 时 `python -m myqcd` 跳过论文清单
（`verified_core_without_inventory`）。指定 paper id 或 inventory JSON
时以退出码 2 报错。

## 打包

只发布 sdist。`pyproject.toml`、`MANIFEST.in`、`README.zh-CN.md` 与
`myqcd/py.typed` 必须保持跟踪；白名单 `.gitignore` 可能漏掉
extensionless 文件。
