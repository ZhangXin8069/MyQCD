# AGENTS.md — MyQCD docs

先读根 `AGENTS.md`。本目录只保存 Markdown、TeX、PDF 和图片形式的人工维护文档、
报告与来源快照。

- `docs/en/` 与 `docs/zh/` 是 Read the Docs 源目录；其中的 `conf.py`、
  `requirements.txt` 和 `.readthedocs.yaml` 是构建入口，属于允许的例外。
  站点构建不得 `import myqcd`，也不依赖原生库或 CUDA。

- 当前物理说明必须引用仓库内 `refer/git-rep/PyQCD/`；不得使用仓库外 PyQCD 路径。
- `docs/pyqcd_reference/` 是固定提交的只读快照，不按当前接口回写或批量改写。
- 来源定位、公式审计结果与理论解释分开陈述；旧 PDF、日志或局部编译不能冒充本轮验证。
- 当前 `docs/.gitignore` 对子目录有忽略规则；新增文件后先用 `git check-ignore -v <path>`
  核对跟踪范围，不得用强制暂存绕过边界。

交付前至少运行 `git diff --check` 和根 `AGENTS.md` 指定的严格格式审计。
