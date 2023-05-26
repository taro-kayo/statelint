import pytest

from statelint.linter import Linter

from .common import get_path


def test_invalid_json_str():
    assert Linter.validate("a") == [
        "Problem reading/parsing JSON: Expecting value: line 1 column 1 (char 0)"
    ]


def test_invalid_json_file():
    file_path = get_path("invalid.json")
    assert Linter.validate(file_path) == [
        "Problem reading/parsing JSON: Expecting ',' delimiter: line 2 "
        "column 11 (char 12)"
    ]


def test_null():
    assert Linter.validate("null") == []


@pytest.mark.parametrize(
    "filepath",
    [
        ("states-uuid-invocation.json"),
    ],
)
def test_valid_json(filepath):
    assert Linter().validate(get_path(filepath)) == []
