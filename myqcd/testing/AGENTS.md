# AGENTS.md — MyQCD tests

先读根 `AGENTS.md` 与 `myqcd/AGENTS.md`。`pytest.ini` 只收集
`myqcd/testing/myqcd/`；不要把数据、参考转排或缓存变成测试目录。

```bash
python -m pytest myqcd/testing/myqcd
python -m pytest myqcd/testing/myqcd/test_myqcd_wick.py
```

测试可依赖仓库内参考树与 `refer/papers/INDEX.md`。缺失外部参考数据造成的失败应与代码回归
分开报告；不得用跳过、删除断言或旧产物掩盖基线失败。
