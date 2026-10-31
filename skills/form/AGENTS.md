# AGENTS.md — MyQCD form skill

先读根 `AGENTS.md`、`skills/AGENTS.md` 和本目录 `SKILL.md`。本目录维护 MyQCD 的命名、
目录、日志、数据、测试布局与 Git 交付格式规则。

- 本库特化规则以根 `AGENTS.md` 的 form 标记块和 `SKILL.md` 为准；全局 form 参考只补充通用矩阵。
- 严格审计入口：

```bash
/root/configure/skills/form/scripts/form-audit.sh --root /root/MyQCD --strict --quiet
```

- `refer/**` 是只读来源树，不因格式治理重排或小写化；当前旧路径检查需排除历史日志快照。
- 修改规则时同步检查现行入口和文档引用，不虚构未执行命令或未验证结果。
