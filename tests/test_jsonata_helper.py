import pytest

from statelint.utils.jsonata_helper import evaluate_jsonata


@pytest.mark.parametrize(
    "expr,variables,expected",
    [
        ("$value", {"value": "42"}, "42"),
        ("$value", {"value": 42}, 42),
        ("$number($value)", {"value": "42"}, 42),
        ("$number($value)", {"value": 42}, 42),
        ("$number($value)", {"value": "A"}, None),
        ("$value(42)", {"value": 42}, None),
    ],
)
def test_evaluate_jsonata(expr, variables, expected):
    result = evaluate_jsonata(expr, variables)
    assert result == expected
