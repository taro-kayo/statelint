import functools
from typing import List, Pattern

import regex as re  # for unicode codepoint (\p{})

INITIAL_NAME_CLASSES = ["Lu", "Ll", "Lt", "Lm", "Lo", "Nl"]
NON_INITIAL_NAME_CLASSES = ["Mn", "Mc", "Nd", "Pc"]
FOLLOWING_NAME_CLASSES = [*INITIAL_NAME_CLASSES, *NON_INITIAL_NAME_CLASSES]
DOT_SEPARATOR = r"\.\.?"

INTRINSIC_INVOCATION_PATTERN = re.compile(
    r"^States\.(JsonToString|Format|StringToJson|Array)\(.+\)$"
)


def is_reference_path(value: str) -> bool:
    return bool(_compile_reference_path_pattern().match(value))


def is_path(value: str, is_context_object_ok: bool = False) -> bool:
    if is_context_object_ok:
        value = re.sub(r"^\$\$", "$", value)
    return bool(_compile_path_pattern().match(value))


def is_intrinsic_invocation(value: str) -> bool:
    return isinstance(value, str) and bool(INTRINSIC_INVOCATION_PATTERN.match(value))


@functools.lru_cache()  # TODO
def _compile_reference_path_pattern() -> Pattern[str]:
    name_re = _make_name_re()
    rp_dot_step = DOT_SEPARATOR + name_re
    bracket_step = rf"\['{name_re}']"
    rp_num_index = r"\[\d+]"
    rp_step = f"(({rp_dot_step})|({bracket_step}))({rp_num_index})?"
    reference_path = rf"^\$({rp_step})*$"

    return re.compile(reference_path)


@functools.lru_cache()  # TODO
def _compile_path_pattern() -> Pattern[str]:
    name_re = _make_name_re()
    bracket_step = _make_bracket_step(name_re)

    dot_step = rf"{DOT_SEPARATOR}(({name_re})|(\*))"
    num_index = r"\[\d+(, *\d+)?]"
    star_index = r"\[\*]"
    colon_index = r"\[(-?\d+)?:(-?\d+)?]"
    index = rf"(({num_index})|({star_index})|({colon_index}))"
    step = f"(({dot_step})|({bracket_step})|({index}))({index})?"
    path = rf"^\$({step})*$"
    return re.compile(path)


def _make_name_re() -> str:
    return (
        _classes_to_re(INITIAL_NAME_CLASSES)
        + _classes_to_re(FOLLOWING_NAME_CLASSES)
        + "*"
    )


def _make_bracket_step(name_re: str) -> str:
    return rf"\['{name_re}']"


def _classes_to_re(classes: List[str]) -> str:
    joined = "".join(rf"\p{{{c}}}" for c in classes)
    return f"[{joined}]"
