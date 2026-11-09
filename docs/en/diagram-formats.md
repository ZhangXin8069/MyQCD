# Diagram formats

`myqcd.diagram_export` writes the same `Diagram` into six formats without
external dependencies:

| Format | Function | Use |
|---|---|---|
| JSON | `to_json` | machine-readable structure |
| Mermaid | `to_mermaid` | Markdown/HTML documentation |
| LaTeX table | `to_latex_table` | papers and reports |
| TikZ-Feynman | `to_tikz` | publication figures |
| Graphviz DOT | `to_dot` | automatic layout |
| SVG | `to_svg` | browser/vector output |

The SVG/TikZ layout places trees on a chain, pure cycles on a circle,
parallel edges on quadratic curves and external legs on short stubs.

## Reproduce

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

## Comparison with the reference libraries

`pyfeyn2` and `pyfeyngen` provide richer automatic layouts and LaTeX
renderers, but they are GPL-3.0 or optional dependencies. `myqcd` keeps a
zero-dependency subset for auditability. The formats here are structural:
no external process is invoked and no physics symmetry factor is inferred.
