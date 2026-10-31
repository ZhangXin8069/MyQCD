# AGENTS.md — MyQCD package tests

先读根 `AGENTS.md`、`myqcd/AGENTS.md` 和上级 `testing/AGENTS.md`。本目录保存主包的
SymPy、Wick 配对、来源索引与 CLI 回归测试。

- 从仓库根运行 `python -m pytest myqcd/testing/myqcd`；修改单个模块时先运行对应测试文件。
- 测试应断言可观察结果、错误类型和证据边界，不复制上游实现作为自证。
- `refer/**` 是只读输入；测试不得进入或修改子模块，也不得把仓库外 PyQCD 当作事实源。
- 当前完整测试需要存在的 `refer/papers/INDEX.md` 与已初始化 PyQCD 文档；缺失时必须记录为
  环境/数据缺口，不能宣称全量通过。
