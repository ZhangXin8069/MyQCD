# AGENTS.md — MyQCD

## 项目边界

- 本库的核心定位是解释 `refer/git-rep/PyQCD/` 中的物理，专注 QCD，尤其是格点
  QCD、胶子算符、梯度流、重正化、匹配和 TMD-PDF。主包 `myqcd/` 提供可执行公式
  审计；`docs/` 保存物理说明与报告；`refer/papers/`、`refer/books/` 保存本地
  LaTeX 文献辅助；`skills/` 保存维护技能；`logs/` 保存机器证据；`data/` 保存
  不入库的运行数据。
- `refer/git-rep/PyQCD/` 是唯一 PyQCD 源码事实源，
  `refer/git-rep/PyQCD/refer/` 是其只读参考树。不得修改、移动或复制上游子模块
  内容；新增说明写入 `refer/git-rep/docs/`。
- 不在未获明确授权时读取 `/root/MyQCD` 之外的目录，也不得退回使用仓库外同级 PyQCD。
  真实系综或 GPU 验证必须另行确认资源与运行时，不能用旧产物冒充新验证结果。
- 一次任务只修改相关文件；不得用 `git add -A`、强制推送、删除未跟踪用户文件或改写
  已推送标签来解决格式问题。

## 技能执行公共契约

1. 先读本文件、目标目录最近的 `AGENTS.md` 和对应 `SKILL.md`，再检查相关代码与入口。
2. 先执行只读审计和功能基线，列出批次、验证命令与回退点；计划内低风险整改可直接执行。
3. 修改后运行最小相关验证；全库改动还必须运行根测试、语法检查、旧引用搜索和严格审计。
4. 不编造物理结论、测试结果、远端状态或文件证据；未执行或不具备条件的验证明确标记为缺口。
5. 完成后按「改动内容 → 推理依据 → 验证结果 → 后续步骤」汇报。

<!-- form-skill:start -->
## form 格式约定

> 本库原有明确约定与本节通用规则冲突时，以原有约定为准；用户明确指令优先于二者。

- 库类型：`complex`。
- 主导语言：根包与技能脚本为 Python，交付文档和参考转排为 LaTeX/Markdown，其他资源为数据或图片。
- Python 文件与模块使用全小写下划线；包私有模块使用 `_` 前缀；类型使用大驼峰；
  普通函数和变量使用小写下划线；模块级常量使用全大写下划线。
- 数学或领域缩写可保留标准大写，如 `QCD`、`TMD`、`SU3`；Python 特殊名称
  `__init__.py`、`__main__.py` 是语言强制例外。
- 顶层目录白名单：`data/`、`docs/`、`logs/`、`myqcd/`、`refer/`、`skills/`。
  根目录仅允许 `README.md`、`LICENSE`、`.gitignore`、`pytest.ini` 和 agent 配置文件。
- Agent 指令文件唯一名称是 `AGENTS.md`；`AGENT.md` 是历史输入错误，不是兼容别名。
  同目录同时存在两者时，必须先将 `AGENT.md` 的有效内容合并到 `AGENTS.md` 并去重，
  再删除 `AGENT.md`，并同步全部现行引用。
- `docs/` 只放 Markdown、TeX、PDF 和图片；`logs/` 只放 `AGENTS.md` 以及
  `log/json/tsv/csv/txt` 文件，不允许 `.DS_Store`；`data/` 只跟踪 `.gitignore`、
  `AGENTS.md`、`README.md`。
- 测试入口：`python -m pytest`；公式与来源审计入口：`python -m myqcd`。
- 格式验证入口：
  `/root/configure/skills/form/scripts/form-audit.sh --root /root/MyQCD --strict --quiet`。
- Git 交付按 `~form` 批准范围分批提交并普通推送；禁止强推。`refer/**` 保留上游目录名；
  `logs/**` 是历史证据快照，迁移记录也可以引用旧路径，但当前可执行文件和现行文档
  不得继续使用旧路径。
- PyQCD 源码、文档和 `refer/` 参考统一从仓库内
  `refer/git-rep/PyQCD/` 解析；仓库外同级 PyQCD 不再是有效入口。
- `data/**` 的运行内容、缓存和图片是本库唯一批准的不入库例外；由 `data/.gitignore`
  统一排除。
<!-- form-skill:end -->
