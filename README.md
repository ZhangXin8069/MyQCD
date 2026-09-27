# MyQCD

MyQCD 是 ZhangXin 的格点 QCD 理论审计与课程工程仓库。

## 目录

| 路径 | 用途 |
|---|---|
| `myqcd/` | 论文公式的 SymPy 审计包与测试 |
| `skills/` | 课程、文献与格式治理 agent 技能 |
| `docs/` | 报告、课程源码、PDF 与说明文档 |
| `logs/` | 可复现实验与构建的机器证据 |
| `data/` | 不入库的运行数据和缓存 |
| `refer/` | 外部书籍、论文及参考仓库 |

## 验证

```bash
python -m pytest
python -m myqcd
python skills/lqcd-course/scripts/sympy_validation.py --check-only
python skills/lqcd-course/scripts/course_examples/run_all.py --quiet
```

仓库格式约束、外部访问边界和各技能入口见根 `AGENTS.md`。
