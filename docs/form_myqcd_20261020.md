# MyQCD form 整改记录（2026-10-20）

## 目标

清理本轮唯一真实 form 冲突 `logs/.DS_Store`，补充精确忽略规则，并把根
`AGENTS.md` 的现有 form 约定收口为唯一的管理标记块。整改基线为提交
`7bb3e0dae650e56760d1814dab8b22f874844b42`。

## 冲突表

| 对象 | 类型 | 当前位置 | 预期规则 | 冲突 | 处理 |
|---|---|---|---|---|---|
| `.DS_Store` | macOS 元数据文件 | `logs/.DS_Store` | `logs/` 仅允许索引、日志和机器证据扩展名 | 是 | 以 Git 可恢复方式删除 |
| `.gitignore` | 忽略规则 | 根 `.gitignore` | 阻止 `logs/` 中的 `.DS_Store` 再次入库 | 是 | 在日志放行规则之后追加精确排除 |
| form 根规则 | `AGENTS.md` 章节 | 根 `AGENTS.md` | 使用唯一 `form-skill` 管理块并保留本地规则 | 是 | 用同步脚本生成唯一标记块 |
| 本地 form 技能 | 规则正文 | `skills/form/SKILL.md` | 与根规则一致，明确禁止日志树元数据文件 | 是 | 小幅补充不变量 |

## 改动

- 执行 `git rm -- logs/.DS_Store`，删除已跟踪的 6,148 字节 Apple Desktop
  Services Store 文件；未删除其他文件。
- 在根 `.gitignore` 末尾追加 `logs/**/.DS_Store`，该规则位于 `!logs/**`
  之后，同时覆盖 `logs/.DS_Store` 与 `logs/**/.DS_Store`。
- 使用 `/root/configure/skills/form/scripts/form-agents-sync.sh` 将原有 form
  约定迁入唯一 `<!-- form-skill:start -->` / `<!-- form-skill:end -->`
  标记块，保留本地目录、例外、测试入口和历史证据规则，并明确
  `logs/` 不允许 `.DS_Store`。
- 更新 `skills/form/SKILL.md` 的日志不变量，明确 `logs/` 不允许
  `.DS_Store`。

如需在本地恢复删除前的内容，仅用于排查：

```bash
git restore --source=7bb3e0dae650e56760d1814dab8b22f874844b42 -- logs/.DS_Store
```

恢复后不得重新跟踪该文件。

## 验证证据

| 检查 | 基线与整改后结果 |
|---|---|
| `python -m pytest -q` | 基线 `112 passed in 339.80s`；整改后 `112 passed in 333.02s` |
| `python skills/lqcd-course/scripts/sympy_validation.py --check-only` | 基线与整改后均为 `175/175 passed` |
| `python skills/lqcd-course/scripts/course_examples/run_all.py --quiet` | 基线与整改后均为 `26/26 passed` |
| `form-audit.sh --root /root/MyQCD --strict --quiet` | 退出码 0，无警告 |
| `form-snapshot-verify.sh --quiet` | 退出码 0 |
| `form-agents-sync.sh --check --quiet` | 退出码 0，标记块与托管内容一致 |
| `git check-ignore --no-index -v logs/.DS_Store logs/data/.DS_Store` | 两条路径均由 `.gitignore:452` 的 `logs/**/.DS_Store` 命中 |
| `git ls-files -- '*.DS_Store'` | 无输出 |
| `python -m compileall -q myqcd skills/lqcd-course/scripts skills/refer/scripts` | 退出码 0 |
| `git diff --check` | 退出码 0 |
| `git diff --cached --check` | 退出码 0 |

## 未决项

- 课程命令本轮完整通过，没有因外部 `../PyQCD` 路径产生阻塞，也没有读取该路径。
- 按任务要求未提交、未推送、未创建或改写标签。
