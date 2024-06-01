import pytest

from statelint.linter import Linter


@pytest.mark.parametrize(
    "error,cause",
    [
        ({}, {}),
        ({"Error": "error"}, {"Cause": "cause"}),
        ({"ErrorPath": "$.x"}, {"CausePath": "$.x"}),
        (
            {"ErrorPath": "States.Format('{} {}', 1, 2)"},
            {"CausePath": "States.Format('{} {}', 1, 2)"},
        ),
    ],
)
def test_ok(error, cause):
    state_machine = {
        "States": {"x": {"Type": "Fail", **error, **cause}},
        "StartAt": "x",
    }
    assert Linter.validate(state_machine) == []


@pytest.mark.parametrize(
    "props,errors",
    [
        (
            {"Error": 42, "Cause": 42},
            [
                "State Machine.States.x.Error is 42 but should be a String",
                "State Machine.States.x.Cause is 42 but should be a String",
            ],
        ),
        (
            {"ErrorPath": "x", "CausePath": "x"},
            [
                'State Machine.States.x.ErrorPath is "x" but should be a Reference '
                "Path or an Intrinsic Function",
                'State Machine.States.x.CausePath is "x" but should be a Reference '
                "Path or an Intrinsic Function",
            ],
        ),
        (
            {"Error": "error", "ErrorPath": "$.x"},
            ['State Machine.States.x may have only one of ["Error", "ErrorPath"]'],
        ),
        (
            {"Cause": "error", "CausePath": "$.x"},
            ['State Machine.States.x may have only one of ["Cause", "CausePath"]'],
        ),
    ],
)
def test_ng(props, errors):
    state_machine = {
        "States": {"x": {"Type": "Fail", **props}},
        "StartAt": "x",
    }
    assert Linter.validate(state_machine) == errors
