# AGENTS.md — MyQCD

## 项目边界

- 本库为复杂 Python/LaTeX 项目，主包是 `myqcd/`；`refer/` 保存外部论文和书籍资料，
  `skills/` 保存本库 agent 技能，`docs/` 保存交付文档，`logs/` 保存机器证据，
  `data/` 保存不入库的运行数据。
- 不在未获明确授权时读取仓库外的 `../PyQCD` 或其他外部目录。涉及该路径的完整课程
  重编译必须等待授权，不能以旧产物冒充新验证结果。
- 一次任务只修改相关文件；不得用 `git add -A`、强制推送、删除未跟踪用户文件或改写
  已推送标签来解决格式问题。

## 技能执行公共契约

1. 先读本文件、目标目录最近的 `AGENTS.md` 和对应 `SKILL.md`，再检查相关代码与入口。
2. 先执行只读审计和功能基线，列出批次、验证命令与回退点；计划内低风险整改可直接执行。
3. 修改后运行最小相关验证；全库改动还必须运行根测试、语法检查、旧引用搜索和严格审计。
4. 不编造物理结论、测试结果、远端状态或文件证据；未执行或不具备条件的验证明确标记为缺口。
5. 完成后按「改动内容 → 推理依据 → 验证结果 → 后续步骤」汇报。

## form 格式约定

- 库类型：`complex`。
- 主导语言：根包与技能脚本为 Python，交付文档和参考转排为 LaTeX/Markdown，其他资源为数据或图片。
- Python 文件与模块使用全小写下划线；包私有模块使用 `_` 前缀；类型使用大驼峰；
  普通函数和变量使用小写下划线；模块级常量使用全大写下划线。
- 数学或领域缩写可保留标准大写，如 `QCD`、`TMD`、`SU3`；Python 特殊名称
  `__init__.py`、`__main__.py` 是语言强制例外。
- 顶层目录白名单：`data/`、`docs/`、`logs/`、`myqcd/`、`refer/`、`skills/`。
  根目录仅允许 `README.md`、`LICENSE`、`.gitignore`、`pytest.ini` 和 agent 配置文件。
- `docs/` 只放 Markdown、TeX、PDF 和图片；`logs/` 只放 `log/json/tsv/csv/txt`；
  `data/` 只跟踪 `.gitignore`、`AGENTS.md`、`README.md`。
- 课程代码位于 `skills/lqcd-course/scripts/`，教学模块位于其 `course_examples/`；
  文献报告生成器位于 `skills/refer/scripts/`。
- 测试入口：`python -m pytest`。课程证据入口：
  `python skills/lqcd-course/scripts/sympy_validation.py --check-only` 和
  `python skills/lqcd-course/scripts/course_examples/run_all.py --quiet`。
- 格式验证入口：
  `/root/configure/skills/form/scripts/form-audit.sh --root /root/MyQCD --strict --quiet`。
- Git 交付按 `~form` 批准范围分批提交并普通推送；禁止强推。`refer/**` 保留上游目录名；
  `logs/**` 是历史证据快照，迁移记录也可以引用旧路径，但当前可执行文件和现行文档
  不得继续使用旧路径。
- `data/**` 的运行内容、缓存和图片是本库唯一批准的不入库例外；由 `data/.gitignore`
  统一排除。
