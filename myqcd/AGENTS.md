# AGENTS.md — MyQCD Python package

先读根 `AGENTS.md`。本目录是 `myqcd/` 主包，只放可执行的公式、来源与物理边界审计代码；
测试统一放在 `myqcd/testing/myqcd/`。

## 已验证入口

```bash
python -m myqcd
python -m myqcd.operator_audit --root .
python -m myqcd.pyqcd_theory_audit --root .
python -m pytest myqcd/testing/myqcd
python -m compileall -q myqcd
```

`python -m myqcd` 在 `refer/papers/INDEX.md` 缺失时自动跳过论文清单
（`status=verified_core_without_inventory`），核心检查仍然执行；指定
`--paper-id` 或 `--inventory-json` 时因无法校验/写出清单而以退出码 2 报错。
不能把跳过清单当作完整 CLI 验证。

- PyQCD 事实源只允许是仓库内 `refer/git-rep/PyQCD/`；默认入口不得回退到仓库外路径。
- `verified` 只覆盖代码实际检查的代数、组合、量纲或有限维代理，不扩展到非微扰矩阵元、
  真实系综、GPU、连续极限或未执行的物理推导。
- 新增测试放在约定测试树；不要在此目录创建临时脚本、运行数据或复制上游源码。
