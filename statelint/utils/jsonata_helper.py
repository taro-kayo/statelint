import re
from typing import Any

_PATTERN = r"\{% +(.+) +%\}"


def extract_jsonata_exp(value: str) -> str | None:
    match = re.match(_PATTERN, value)
    return match and match[1]


def is_jsonata_value(value: str) -> bool:
    return bool(extract_jsonata_exp(value))


def evaluate_jsonata(expr_str: str, variable: dict[str, Any]) -> Any:
    from jsonata import Jsonata  # type: ignore

    expr = Jsonata(expr_str)
    for k, v in variable.items():
        expr.assign(k, v)

    try:
        return expr.evaluate(variable)
    except Exception:
        return None
