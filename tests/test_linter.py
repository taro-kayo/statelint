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


def test_invalid_jsonata_file():
    file_path = get_path("invalid-jsonata-1.json")
    assert Linter.validate(file_path) == [
        'Field "Output" not allowed in State Machine.States.FailState'
    ]


def test_null():
    assert Linter.validate("null") == []


@pytest.mark.parametrize(
    "filepath",
    [
        ("states-uuid-invocation.json"),
        ("jsonata-1.json"),
    ],
)
def test_valid_json(filepath):
    assert Linter().validate(get_path(filepath)) == []
