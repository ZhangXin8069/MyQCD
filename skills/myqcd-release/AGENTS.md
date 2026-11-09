# AGENTS.md — myqcd-release

先读根 `AGENTS.md`、`skills/AGENTS.md` 和本技能 `SKILL.md`。

- 本技能只负责 `myqcd` 的 PyPI、Read the Docs、双语 README 与双远端发布；
  物理结论必须由 `myqcd.operator_audit` / `myqcd.pyqcd_theory_audit` 和测试提供。
- 发布凭据只从 `~/env-key.sh` 的环境变量读取；不打印、不写入日志或 Git。
- 不修改 `refer/git-rep/` 子模块工作树；参考库只读。
- 版本只能递增；PyPI 同版本不可覆盖，修正必须发新版本。
- 双远端推送使用 `gpush.sh` 与 `gpush.sh -t gitee.com`；Gitee 自动同步 GitHub。
