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


def test_invalid_jsonata_1_file():
    file_path = get_path("invalid-jsonata-1.json")
    assert Linter.validate(file_path) == [
        'Field "Output" not allowed in State Machine.States.FailState'
    ]


@pytest.mark.parametrize(
    "filename",
    [
        ("invalid-jsonata-2.json"),
        ("invalid-jsonata-3.json"),
    ],
)
def test_invalid_jsonata_2_3_file(filename):
    file_path = get_path(filename)
    assert Linter.validate(file_path) == [
        'Field "Assign" not allowed in State Machine.States.JSONPath state',
        'Field "Output" not allowed in State Machine.States.JSONPath state',
        'State Machine.States.JSONata state.Assign is "XXX" but should be an Object',
    ]


def test_null():
    assert Linter.validate("null") == []


@pytest.mark.parametrize(
    "filepath",
    [
        ("states-uuid-invocation.json"),
        ("jsonata-1.json"),
        ("jsonata-2.json"),
        ("jsonata-3.json"),
        ("jsonata-4.json"),
        ("jsonata-5.json"),
    ],
)
def test_valid_json(filepath):
    assert Linter().validate(get_path(filepath)) == []
