"""课程内容声明的轻量辅助函数。

这里不生成教学文字，只消除结构性重复；每个单元的物理内容仍在分卷
模块中逐项给出，便于同行审阅和后续修订。
"""

from typing import Iterable, Sequence, Tuple

from .schema import ChapterChart, Lesson, Volume, lesson, volume


def terms(*items: Tuple[str, str]) -> Tuple[Tuple[str, str], ...]:
    return tuple(items)


def lines(*items: str) -> Tuple[str, ...]:
    return tuple(items)


def L(
    code: str,
    title: str,
    question: str,
    picture: Tuple[str, str, str],
    vocabulary: Tuple[Tuple[str, str], ...],
    equation: str,
    meaning: str,
    principle: str,
    derivation: Tuple[str, ...],
    algorithm: Tuple[str, ...],
    checks: Tuple[str, ...],
    exercise: str,
    solution: str,
    code_map: str = "课程内纸笔/符号计算练习",
    sources: Tuple[str, ...] = ("BOOK-MATH",),
) -> Lesson:
    """声明一个完整学习单元；SymPy 编号由课程编号唯一确定。"""

    return lesson(
        code=code,
        title=title,
        question=question,
        picture=picture,
        terms=vocabulary,
        equation=equation,
        equation_meaning=meaning,
        sympy_check=f"SYM-{code}",
        principle=principle,
        derivation=derivation,
        algorithm=algorithm,
        checks=checks,
        exercise=exercise,
        solution=solution,
        code_map=code_map,
        sources=sources,
    )


def C(
    title: str,
    x_label: str,
    y_label: str,
    bounds: Tuple[float, float, float, float],
    series: Sequence[Tuple[str, str]],
    note: str,
    source: str,
) -> ChapterChart:
    """声明卷级定量图。series 的表达式采用 PGFPlots 数学语法。"""

    x_min, x_max, y_min, y_max = bounds
    return ChapterChart(
        title=title,
        x_label=x_label,
        y_label=y_label,
        x_min=x_min,
        x_max=x_max,
        y_min=y_min,
        y_max=y_max,
        series=tuple(series),
        note=note,
        source=source,
    )


def V(
    code: str,
    slug: str,
    title: str,
    goal: str,
    prerequisites: Iterable[str],
    outcomes: Iterable[str],
    chart: ChapterChart,
    lessons: Sequence[Lesson],
    sources: Iterable[str],
) -> Volume:
    return volume(
        code=code,
        slug=slug,
        title=title,
        goal=goal,
        prerequisites=tuple(prerequisites),
        outcomes=tuple(outcomes),
        chart=chart,
        lessons=tuple(lessons),
        sources=tuple(sources),
    )


__all__ = ["C", "L", "V", "lines", "terms"]
