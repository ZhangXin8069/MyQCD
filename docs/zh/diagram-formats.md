# 图导出格式

`myqcd.diagram_export` 把同一个 `Diagram` 写成六种格式，不依赖外部程序：

| 格式 | 函数 | 用途 |
|---|---|---|
| JSON | `to_json` | 机器可读结构 |
| Mermaid | `to_mermaid` | Markdown/HTML 文档 |
| LaTeX 表格 | `to_latex_table` | 论文与报告 |
| TikZ-Feynman | `to_tikz` | 出版级图 |
| Graphviz DOT | `to_dot` | 自动布局 |
| SVG | `to_svg` | 浏览器/矢量输出 |

SVG/TikZ 布局把树图放在水平链上、纯环图放在圆周上、平行边画成二次曲线、
外部腿画成短桩。

## 复现

```python
import json

from myqcd import diagram_export, feynman

triangle = feynman.Diagram(
    vertices=("a", "b", "c"),
    edges=(
        feynman.Edge(0, 1, "gluon"),
        feynman.Edge(1, 2, "gluon"),
        feynman.Edge(2, 0, "gluon"),
    ),
)
assert triangle.loop_count == 1
payload = json.loads(diagram_export.to_json(triangle))
assert payload["loop_count"] == 1
assert diagram_export.to_mermaid(triangle).startswith("flowchart LR")
assert "\\begin{tabular}" in diagram_export.to_latex_table(triangle)
assert diagram_export.render(triangle, "tikz").startswith("%")
print(diagram_export.export_audit(triangle)["formats"])
```

## 与参考库比对

`pyfeyn2` 与 `pyfeyngen` 提供更丰富的自动布局和 LaTeX 渲染，但它们是
GPL-3.0 或可选依赖。`myqcd` 保留零依赖子集以便审计。这里只保证结构格式，
不调用外部进程，也不推断物理对称因子。
