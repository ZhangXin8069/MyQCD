---
name: form
description: |
  当用户要求审计或整改 MyQCD 的命名、目录结构、代码框架、文档、日志、数据、
  测试布局、仓库清洁度或 Git 交付格式时使用。
metadata:
  openclaw:
    emoji: 📐
---

# form — MyQCD 格式治理

遵循根 `AGENTS.md`；本库为 `complex`，主导语言为 Python，交付文档使用
LaTeX/Markdown。通用命名矩阵、快照证据与交付模板读取全局
`/root/configure/skills/form/references/`，本库目录白名单、入口和例外以根
`AGENTS.md` 为准。冲突时，已批准且可验证的本地规则优先。

## 目录职责

| 路径 | 职责 |
|---|---|
| `myqcd/` | 论文公式审计主包；测试位于 `myqcd/testing/myqcd/` |
| `skills/<name>/scripts/` | 技能自带的可执行 Python 工具 |
| `docs/` | Markdown、TeX、PDF 和图片交付物 |
| `logs/` | 允许扩展名的机器证据与历史日志 |
| `data/` | 不入库的运行数据；只跟踪三个护栏文件 |
| `refer/` | 上游书籍、论文与参考仓库，保留来源命名 |

## 不可破坏的不变量

1. `data/` 仅跟踪 `.gitignore`、`AGENTS.md`、`README.md`。
2. `logs/` 仅跟踪 `log/json/tsv/csv/txt`；LaTeX 中间文件不提交。
3. 课程源码、内容与验证器不得放回 `data/`；成品与机器日志分别留在
   `docs/` 和 `logs/`。
4. `refer/**` 的上游命名和内容不因本库格式治理而批量小写或重排。
5. 路径迁移必须同步命令行、来源表、技能文档和所有旧引用，不能只移动文件。

## 工作流程

1. 锁定 Git 根、工作区状态、语言树、顶层目录和现有改动；先执行只读审计。
2. 运行：

   ```bash
   /root/configure/skills/form/scripts/form-audit.sh --root /root/MyQCD --quiet
   /root/configure/skills/form/scripts/form-snapshot-verify.sh --quiet
   ```

3. 建立 `对象/类型/语言/当前位置/预期规则/冲突/处理` 冲突表，按目录、移动、
   引用、文档、测试、清理、Git 的依赖顺序分批实施。
4. 每批完成后运行 Python 编译、相关测试和被移动文件的 `--help`/SymPy 冒烟。
5. 最终运行根 `pytest`、课程两层 SymPy、旧路径搜索、`git diff --check` 和
   `form-audit --strict`。不能执行的验证必须列出外部依赖与风险。
6. 交付遵循 `~diff → ~init → ~tag(dev)`；普通提交和推送按 `~form` 授权执行，
   强推、改写已推送标签和仓库外写入必须单独确认。

## 本库特化

- Python 测试入口为 `python -m pytest`，`pytest.ini` 只声明实际测试树。
- 课程命令统一从仓库根执行，源码根为 `skills/lqcd-course/scripts/`。
- `logs/` 中已有历史快照和本次迁移记录可保留旧路径文字；当前可执行文件、现行文档
  和来源表必须使用迁移后的路径。
- 完整 43 份课程 PDF 重编译需要仓库外的 `../PyQCD`；未获访问授权时只能验证源码、
  内容和 SymPy 层，不能声明 PDF 指纹已重新通过。

## 验收证据

| 维度 | 命令或证据 | 通过条件 |
|---|---|---|
| 目录/命名 | `form-audit.sh --strict` | 无警告与错误 |
| 规则快照 | `form-snapshot-verify.sh --quiet` | 退出码为 0 |
| Python | `python -m pytest` | 全部通过 |
| 课程公式 | `sympy_validation.py --check-only` | `175/175` |
| 教学模块 | `course_examples/run_all.py --quiet` | `26/26` |
| 引用迁移 | `git grep` 旧路径与旧导入 | 当前文件为零 |
| Git | `git diff --check`、远端分支与标签 | 无空白错误、目标一致 |
