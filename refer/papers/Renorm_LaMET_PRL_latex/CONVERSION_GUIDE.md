# CONVERSION_GUIDE.md

- 底稿来源：arXiv:1706.08962 官方 e-print（单文件 gzip `renorm_v5.tex`，REVTeX4-1 源），2026-08-25 获取。
- 归一化：`\documentclass[11pt]{article}` + geometry(2.5cm)；统一宏包 amsmath/amssymb/mathtools/graphicx/microtype/enumitem/url/hyperref(hidelinks)。
- 移除 revtex4-1 及未被正文使用的宏包（mathrsfs、slashed、epsfig、color、array、verbatim）；仅保留正文实际用到的快捷宏 `\beq/\eeq`（eqnarray）与 `\non`。
- 正文逐字保留，含摘要、致谢、脚注式 Note、参考文献（含 INSPIRE 引用计数注释行）。
- 小节标题按原文保留小写形式（introduction / conclusion）；原文第 5 节 "renormaliztion" 拼写照录。
- 原源码无任何图/表 → 无 images/ 目录，无占位图问题。
- 标题块重排：作者上标 a–d 对应四家单位；出版信息（PRL 120, 112001 (2018)；DOI；arXiv 号；MIT-CTP/4916）以 \thanks 脚注给出。
- 参考文献 greentalk 条目保留了指向 Lattice 2017 报告幻灯片的 \href 链接（原源码如此）。
- 编号：article 默认节 1–6、公式 (1)–(17)，与 arXiv 版一致。
