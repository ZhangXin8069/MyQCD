# MyQCD 格式治理记录（2026-09-28）

## 目标

把 MyQCD 的源码、交付物、机器日志和运行数据重新归入稳定边界：

- 源码不得位于 `data/`；
- `data/` 只跟踪 `.gitignore`、`AGENTS.md`、`README.md`；
- `logs/` 只跟踪 `log/json/tsv/csv/txt`；
- 当前文档、技能入口和命令行不得引用已迁移路径。

整改基线为提交 `bb2e69a44dd17852aa1e6b423213fa5a76a2a365`。

## 冲突表摘要

| 对象 | 当前问题 | 处理 |
|---|---|---|
| `data/docs/lattice_qcd_gluon_tmd_course/` | 课程源码、内容与验证器错误地存放在运行数据目录 | 20 个 Python 文件迁入 `skills/lqcd-course/scripts/` |
| `data/docs/build_refer_papers_*.py` | 文献报告生成器错误地存放在运行数据目录 | 2 个生成器迁入 `skills/refer/scripts/` |
| `data/` | 9,357 个历史跟踪项，包括完整虚拟环境与视觉审计图片 | 从 Git 索引移除，工作区保留并统一忽略 |
| `data/` 参数规则 | 缺少本地边界 | 新增 `.gitignore`、`AGENTS.md`、`README.md` |
| `docs/data/` | 保留 8 份重复报告构建 PDF | 从 Git 索引移除，加入忽略规则 |
| `logs/` | 242 个 `aux/nav/out/snm/toc` LaTeX 中间文件 | 从 Git 索引移除，保留允许的历史日志与 JSON |
| 根规则 | 缺少仓库级 `AGENTS.md` 和本地 form 技能 | 新增根规则与 `skills/form/SKILL.md` |

## 结构变更

课程源码新根为 `skills/lqcd-course/scripts/`：

| 路径 | 职责 |
|---|---|
| `build_course.py` | 同源生成与编译 |
| `sympy_validation.py` | 175 条课程公式验证 |
| `verify_course.py` | 结构、来源、PDF 与视觉证据验证 |
| `render_audit.py` | 全页渲染与联系表 |
| `content/` | 35 卷结构化内容 |
| `course_examples/` | 26 个可运行教学模块 |

活动视觉图片改由脚本写入
`data/lattice_qcd_gluon_tmd_course/visual_audit/`；该目录不入库。文献报告生成器
位于 `skills/refer/scripts/`。

## 验证证据

| 检查 | 结果 |
|---|---|
| `python -m pytest -q` | `112 passed` |
| `python -m myqcd` | 退出码 0 |
| `python skills/lqcd-course/scripts/sympy_validation.py --check-only` | `175/175 passed` |
| `python skills/lqcd-course/scripts/course_examples/run_all.py --quiet` | `26/26 passed` |
| `python -m compileall -q myqcd skills/lqcd-course/scripts skills/refer/scripts` | 退出码 0 |
| `form-audit.sh --strict --quiet` | 退出码 0 |
| `form-snapshot-verify.sh --quiet` | 退出码 0 |
| 当前源码、文档中的旧路径 | 清零；仅历史 `logs/**` 保留旧运行文字 |

## 未决项与恢复

`skills/refer/scripts/build_refer_papers_full_report.py --audit` 仍报告 50 个
`refer/papers/*_latex/build/main.pdf` 缺失。这些 PDF 在本次整改前就没有被 Git
跟踪，属于既有文献构建缺口，不是路径迁移造成的回归；本次没有伪造产物或改写
文献源文件。

课程 PDF 的生成指纹绑定源码路径与哈希，因此本次源码迁移后，已有 43 份 PDF
不再满足新的严格 provenance 指纹。完整重建需要读取仓库外的 `../PyQCD` 论文与
参考文件；本次遵守访问边界，未读取该目录，也没有把旧 PDF 冒充为新验证结果。
获得该路径访问授权后，应重新运行：

```bash
python skills/lqcd-course/scripts/build_course.py all --target all --jobs 4
python skills/lqcd-course/scripts/render_audit.py --dpi 96 --jobs 4
python skills/lqcd-course/scripts/verify_course.py --strict
```

需要恢复本次取消跟踪的历史运行文件时，使用基线提交，例如：

```bash
git show bb2e69a44dd17852aa1e6b423213fa5a76a2a365:data/theory-audit-venv/pyvenv.cfg
git restore --source=bb2e69a44dd17852aa1e6b423213fa5a76a2a365 -- docs/data
```

上述恢复只用于本地排查，不重新把运行数据加入 Git 跟踪。
