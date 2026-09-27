"""格点 QCD 长课程的结构化内容契约。"""

import ast
import math
import re
from dataclasses import dataclass
from numbers import Real
from typing import Tuple


Term = Tuple[str, str]
PlotSeries = Tuple[str, str]


_FORBIDDEN_TEXT_CONTROLS = frozenset("\x00\t\r\f\v")


_CHART_NAMES = frozenset(("x", "pi", "e"))
_CHART_FUNCTIONS = frozenset(
    (
        "abs",
        "acos",
        "asin",
        "atan",
        "atan2",
        "ceil",
        "cos",
        "cosh",
        "deg",
        "exp",
        "floor",
        "frac",
        "ln",
        "log10",
        "max",
        "min",
        "mod",
        "rad",
        "round",
        "sign",
        "sin",
        "sinh",
        "sqrt",
        "tan",
        "tanh",
    )
)
_CHART_AST_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Call,
    ast.Name,
    ast.Load,
    ast.Constant,
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.Pow,
    ast.Mod,
    ast.UAdd,
    ast.USub,
)


def _require_nonblank(name: str, value: object) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} 必须是非空字符串")
    if any(character in value for character in _FORBIDDEN_TEXT_CONTROLS):
        raise ValueError(f"{name} 含 NUL、制表、回车或其他禁用控制字符")


def _require_string_tuple(
    name: str,
    value: object,
    *,
    minimum: int = 1,
    exact: int | None = None,
) -> None:
    if not isinstance(value, tuple):
        raise ValueError(f"{name} 必须是 tuple")
    expected = exact if exact is not None else minimum
    if (exact is not None and len(value) != exact) or len(value) < minimum:
        qualifier = "恰有" if exact is not None else "至少有"
        raise ValueError(f"{name} {qualifier} {expected} 项")
    for index, item in enumerate(value, start=1):
        _require_nonblank(f"{name}[{index}]", item)


def _validate_chart_expression(expression: object, name: str) -> None:
    _require_nonblank(name, expression)
    assert isinstance(expression, str)
    if any(marker in expression for marker in ("\n", "\r", ";", "\\", "{", "}")):
        raise ValueError(f"{name} 含 PGFPlots 表达式禁用字符")
    try:
        tree = ast.parse(expression.replace("^", "**"), mode="eval")
    except SyntaxError as exc:
        raise ValueError(f"{name} 不是合法表达式：{exc.msg}") from exc
    for node in ast.walk(tree):
        if not isinstance(node, _CHART_AST_NODES):
            raise ValueError(f"{name} 含不允许的语法：{type(node).__name__}")
        if isinstance(node, ast.Name) and node.id not in (
            _CHART_NAMES | _CHART_FUNCTIONS
        ):
            raise ValueError(f"{name} 含未知标识符：{node.id}")
        if isinstance(node, ast.Call):
            if (
                not isinstance(node.func, ast.Name)
                or node.func.id not in _CHART_FUNCTIONS
                or not node.args
                or node.keywords
            ):
                raise ValueError(f"{name} 含非法函数调用")
        if isinstance(node, ast.Constant):
            if (
                type(node.value) not in (int, float)
                or not math.isfinite(float(node.value))
            ):
                raise ValueError(f"{name} 只允许有限数值常量")


@dataclass(frozen=True)
class ChapterChart:
    """一卷至少一张可缩放定量图；表达式使用 PGFPlots 语法。"""

    title: str
    x_label: str
    y_label: str
    x_min: float
    x_max: float
    y_min: float
    y_max: float
    series: Tuple[PlotSeries, ...]
    note: str
    source: str

    def __post_init__(self) -> None:
        for field in ("title", "x_label", "y_label", "note", "source"):
            _require_nonblank(f"chart.{field}", getattr(self, field))
        for lower_name, upper_name in (("x_min", "x_max"), ("y_min", "y_max")):
            lower = getattr(self, lower_name)
            upper = getattr(self, upper_name)
            if (
                isinstance(lower, bool)
                or isinstance(upper, bool)
                or not isinstance(lower, Real)
                or not isinstance(upper, Real)
                or not math.isfinite(float(lower))
                or not math.isfinite(float(upper))
                or not lower < upper
            ):
                raise ValueError(
                    f"chart.{lower_name}/{upper_name} 必须是有限且严格递增的数值边界"
                )
        if not isinstance(self.series, tuple) or not self.series:
            raise ValueError("chart.series 必须是非空 tuple")
        for index, item in enumerate(self.series, start=1):
            if not isinstance(item, tuple) or len(item) != 2:
                raise ValueError(f"chart.series[{index}] 必须是二元 tuple")
            label, expression = item
            _require_nonblank(f"chart.series[{index}].label", label)
            _validate_chart_expression(
                expression,
                f"chart.series[{index}].expression",
            )


@dataclass(frozen=True)
class Lesson:
    """一个学习单元；构建器把它展开为五张相互闭合的幻灯片。"""

    code: str
    title: str
    question: str
    picture: Tuple[str, str, str]
    terms: Tuple[Term, ...]
    equation: str
    equation_meaning: str
    sympy_check: str
    principle: str
    derivation: Tuple[str, ...]
    algorithm: Tuple[str, ...]
    checks: Tuple[str, ...]
    exercise: str
    solution: str
    code_map: str
    sources: Tuple[str, ...]

    def __post_init__(self) -> None:
        for field in (
            "code",
            "title",
            "question",
            "equation",
            "equation_meaning",
            "sympy_check",
            "principle",
            "exercise",
            "solution",
            "code_map",
        ):
            _require_nonblank(f"lesson.{field}", getattr(self, field))
        if not re.fullmatch(r"\d{2}\.\d{2}", self.code):
            raise ValueError(f"{self.code!r}: 单元编号必须为两位卷号.两位单元号")
        volume_number, lesson_number = map(int, self.code.split("."))
        if not 1 <= volume_number <= 35 or not 1 <= lesson_number <= 5:
            raise ValueError(f"{self.code}: 单元编号超出固定课程范围")
        _require_string_tuple(
            f"{self.code}.picture",
            self.picture,
            exact=3,
        )
        if not isinstance(self.terms, tuple) or len(self.terms) < 3:
            raise ValueError(f"{self.code}: 至少需要三个术语")
        for index, item in enumerate(self.terms, start=1):
            if not isinstance(item, tuple) or len(item) != 2:
                raise ValueError(f"{self.code}.terms[{index}] 必须是二元 tuple")
            _require_nonblank(f"{self.code}.terms[{index}].name", item[0])
            _require_nonblank(f"{self.code}.terms[{index}].definition", item[1])
        normalized_term_names = tuple(item[0].strip() for item in self.terms)
        if len(normalized_term_names) != len(set(normalized_term_names)):
            raise ValueError(f"{self.code}: 同一单元的术语名不得重复")
        _require_string_tuple(
            f"{self.code}.derivation",
            self.derivation,
            minimum=3,
        )
        _require_string_tuple(
            f"{self.code}.algorithm",
            self.algorithm,
            minimum=4,
        )
        _require_string_tuple(
            f"{self.code}.checks",
            self.checks,
            minimum=2,
        )
        _require_string_tuple(f"{self.code}.sources", self.sources)
        if self.sympy_check != f"SYM-{self.code}":
            raise ValueError(f"{self.code}: SymPy ID 必须为 SYM-{self.code}")


@dataclass(frozen=True)
class Volume:
    """一卷课程；卷号是所有知识对象编号的首字段。"""

    code: str
    slug: str
    title: str
    goal: str
    prerequisites: Tuple[str, ...]
    outcomes: Tuple[str, ...]
    chart: ChapterChart
    lessons: Tuple[Lesson, ...]
    sources: Tuple[str, ...]

    def __post_init__(self) -> None:
        for field in ("code", "slug", "title", "goal"):
            _require_nonblank(f"volume.{field}", getattr(self, field))
        if not re.fullmatch(r"\d{2}", self.code) or not 1 <= int(self.code) <= 35:
            raise ValueError(f"V{self.code}: 卷号必须在 01--35")
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", self.slug):
            raise ValueError(f"V{self.code}: slug 格式非法")
        _require_string_tuple(
            f"V{self.code}.prerequisites",
            self.prerequisites,
        )
        _require_string_tuple(f"V{self.code}.outcomes", self.outcomes)
        _require_string_tuple(f"V{self.code}.sources", self.sources)
        if not isinstance(self.chart, ChapterChart):
            raise ValueError(f"V{self.code}: chart 必须是 ChapterChart")
        if not isinstance(self.lessons, tuple) or len(self.lessons) != 5:
            raise ValueError(f"V{self.code}: 每卷必须恰有五个学习单元")
        if any(not isinstance(item, Lesson) for item in self.lessons):
            raise ValueError(f"V{self.code}: lessons 每项必须是 Lesson")
        expected = tuple(f"{self.code}.{idx:02d}" for idx in range(1, 6))
        actual = tuple(item.code for item in self.lessons)
        if actual != expected:
            raise ValueError(
                f"V{self.code}: 单元编号应为 {expected}，实际为 {actual}"
            )


def lesson(
    code: str,
    title: str,
    question: str,
    picture: Tuple[str, str, str],
    terms: Tuple[Term, ...],
    equation: str,
    equation_meaning: str,
    sympy_check: str,
    principle: str,
    derivation: Tuple[str, ...],
    algorithm: Tuple[str, ...],
    checks: Tuple[str, ...],
    exercise: str,
    solution: str,
    code_map: str,
    sources: Tuple[str, ...],
) -> Lesson:
    """提供较短的声明式构造器，并在导入时做局部完整性检查。"""

    if len(picture) != 3:
        raise ValueError(f"{code}: picture 必须恰有三个节点")
    if len(terms) < 3:
        raise ValueError(f"{code}: 至少需要三个术语")
    if len(derivation) < 3:
        raise ValueError(f"{code}: 至少需要三个推导步骤")
    if len(algorithm) < 4:
        raise ValueError(f"{code}: 至少需要四个算法步骤")
    if len(checks) < 2:
        raise ValueError(f"{code}: 至少需要两个独立检查")
    if not sources:
        raise ValueError(f"{code}: 来源不能为空")
    if sympy_check != f"SYM-{code}":
        raise ValueError(f"{code}: SymPy ID 必须为 SYM-{code}")
    return Lesson(
        code=code,
        title=title,
        question=question,
        picture=picture,
        terms=terms,
        equation=equation,
        equation_meaning=equation_meaning,
        sympy_check=sympy_check,
        principle=principle,
        derivation=derivation,
        algorithm=algorithm,
        checks=checks,
        exercise=exercise,
        solution=solution,
        code_map=code_map,
        sources=sources,
    )


def volume(
    code: str,
    slug: str,
    title: str,
    goal: str,
    prerequisites: Tuple[str, ...],
    outcomes: Tuple[str, ...],
    chart: ChapterChart,
    lessons: Tuple[Lesson, ...],
    sources: Tuple[str, ...],
) -> Volume:
    """建立一卷并保证固定为五个学习单元。"""

    if len(lessons) != 5:
        raise ValueError(f"V{code}: 每卷必须恰有五个学习单元")
    expected = tuple(f"{code}.{idx:02d}" for idx in range(1, 6))
    actual = tuple(item.code for item in lessons)
    if actual != expected:
        raise ValueError(f"V{code}: 单元编号应为 {expected}，实际为 {actual}")
    return Volume(
        code=code,
        slug=slug,
        title=title,
        goal=goal,
        prerequisites=prerequisites,
        outcomes=outcomes,
        chart=chart,
        lessons=lessons,
        sources=sources,
    )
