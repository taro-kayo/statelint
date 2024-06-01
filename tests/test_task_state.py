import pytest

from statelint.linter import Linter


def test_ok():
    state_machine = {
        "States": {
            "x": {
                "Type": "Task",
                "End": True,
                "ResultPath": None,
                "Resource": "arn:x",
                "TimeoutSeconds": 1,
                "ResultSelector": {},
                "Parameters": {},
                "Credentials": {},
                "Catch": [],
            }
        },
        "StartAt": "x",
    }
    assert Linter.validate(state_machine) == []


def test_ok_min():
    state_machine = {
        "States": {
            "x": {
                "Type": "Task",
                "End": True,
                "Resource": "arn:x",
            }
        },
        "StartAt": "x",
    }
    assert Linter.validate(state_machine) == []


def test_bad_fields():
    state_machine = {
        "States": {
            "x": {
                "Type": "Task",
                "End": True,
                "ResultPath": ".x",
                "Resource": "xxx",
                "TimeoutSeconds": 0,
                "ResultSelector": None,
                "Parameters": "x",
            }
        },
        "StartAt": "x",
    }
    assert Linter.validate(state_machine) == [
        'State Machine.States.x.ResultPath is ".x" but should be a Reference Path',
        'State Machine.States.x.Resource is "xxx" but should be A URI',
        "State Machine.States.x.TimeoutSeconds is 0 but allowed floor is 0",
    ]


@pytest.mark.parametrize("name", ["TimeoutSeconds", "HeartbeatSeconds"])
def test_one_of_fields(name):
    state_machine = {
        "States": {
            "x": {
                "Type": "Task",
                "End": True,
                "Resource": "arn:x",
                name: 1,
                f"{name}Path": "$",
            }
        },
        "StartAt": "x",
    }
    assert Linter.validate(state_machine) == [
        f'State Machine.States.x may have only one of ["{name}", "{name}Path"]',
    ]


def test_catch():
    state_machine = {
        "States": {"x": {"Type": "Task", "End": True, "Resource": "arn:x", "Catch": 1}},
        "StartAt": "x",
    }
    assert Linter.validate(state_machine) == [
        "State Machine.States.x.Catch is 1 but should be an Array"
    ]


def test_catch_null():
    state_machine = {
        "States": {
            "x": {"Type": "Task", "End": True, "Resource": "arn:x", "Catch": None}
        },
        "StartAt": "x",
    }
    assert Linter.validate(state_machine) == [
        "State Machine.States.x.Catch should be non-null"
    ]


def test_catch_element():
    state_machine = {
        "States": {
            "x": {
                "Type": "Task",
                "End": True,
                "Resource": "arn:x",
                "Catch": [1, "x"],
            },
        },
        "StartAt": "x",
    }
    assert Linter.validate(state_machine) == [
        "State Machine.States.x.Catch[0] is 1 but should be an Object",
        'State Machine.States.x.Catch[1] is "x" but should be an Object',
    ]
