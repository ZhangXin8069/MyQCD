# AGENTS.md — MyQCD data

`data/` 只承载运行数据、缓存和审计产物，只允许 Git 跟踪 `.gitignore`、
`AGENTS.md` 与 `README.md`。不得把源码、配置、人工维护文档或测试放入本目录。

课程脚本默认把视觉审计图片写到
`data/lattice_qcd_gluon_tmd_course/visual_audit/`；该树由
`skills/lqcd-course/scripts/render_audit.py` 生成，可由课程 PDF 重建。
