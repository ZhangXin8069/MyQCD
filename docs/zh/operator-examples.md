# 算符实例

物理动机明确的双线性简表。符号由 `myqcd.operators` 计算；名称只是标签，
不是带涂抹或 Wilson 线的完整插值场。

| 算符 | 结构 | 导数 | 宇称 | C | 量纲 | PyQCD |
|---|---|---|---|---|---|---|
| $\bar q\gamma_5q$ | `P` | 0 | $-1$ | $+1$ | 3 | 5 |
| $\bar q\gamma_4q$ | `V4` | 0 | $+1$ | $-1$ | 3 | 4 |
| $\bar q\gamma_4\gamma_5q$ | `A4` | 0 | $-1$ | $-1$ | 3 | 15 |
| $\bar q q$ | `S` | 0 | $+1$ | $+1$ | 3 | 0 |
| $\bar q\sigma_{12}q$ | `T12` | 0 | $+1$ | $-1$ | 3 | 8 |
| $\bar q\gamma_3D_\mu q$ | `V3` | 1 | $-1$ | $+1$ | 4 | 3 |
| $\bar q\gamma_4D_\mu D_\nu q$ | `V4` | 2 | $+1$ | $-1$ | 5 | 4 |
| $\bar q\gamma_5D_\mu q$ | `P` | 1 | $-1$ | $+1$ | 4 | 5 |

## 检查

```python
from myqcd import operators

for structure in ("S", "P", "V4", "A4", "T12"):
    operator = operators.BilinearOperator(
        name=f"O_{structure}",
        left_flavor="u",
        right_flavor="d",
        structure=structure,
    )
    assert operator.mass_dimension == 3
    assert operator.pyqcd_gamma_index is not None or structure == "T13"
print("operator examples OK")
```

## 表格不意味着什么

- 标签不包含涂抹、Wilson 线或源共轭。
- 导数算符不自动对称化或无迹化。
- PyQCD 索引是精确矩阵匹配；`T13` 没有精确项。
- 物理插值场可能混合多个结构。
