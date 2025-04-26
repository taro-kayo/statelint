import pytest

from statelint.linter import Linter


def test_null_type():
    state_machine = {"StartAt": "x", "States": {"x": {"Type": None, "End": True}}}
    assert Linter.validate(state_machine) == [
        "State Machine.States.x.Type should be non-null",
        'State Machine.States.x.Type is "", not one of the allowed values '
        '["Pass", "Succeed", "Fail", "Task", "Choice", "Wait", "Parallel", "Map"]',
        'Field "End" not allowed in State Machine.States.x',
    ]


def test_illegal_type():
    state_machine = {"StartAt": "x", "States": {"x": {"Type": "?", "End": True}}}
    assert Linter.validate(state_machine) == [
        'State Machine.States.x.Type is "?", not one of the allowed values '
        '["Pass", "Succeed", "Fail", "Task", "Choice", "Wait", "Parallel", "Map"]',
        'Field "End" not allowed in State Machine.States.x',
    ]


def test_null_resource():
    state_machine = {
        "StartAt": "x",
        "States": {"x": {"Type": "Task", "Resource": 1, "End": True}},
    }
    assert Linter.validate(state_machine) == [
        "State Machine.States.x.Resource is 1 but should be A URI"
    ]


@pytest.mark.parametrize(
    "seconds,problems",
    [
        (0, []),
        (-1, ["State Machine.States.x.Seconds is -1 but allowed floor is 0"]),
        (1, []),
    ],
)
def test_zero_seconds(seconds, problems):
    state_machine = {
        "StartAt": "x",
        "States": {"x": {"Type": "Wait", "Seconds": seconds, "End": True}},
    }
    assert Linter.validate(state_machine) == problems


@pytest.mark.parametrize("value,expected", [(42, 42), ("xyz", '"xyz"')])
def test_invalid_jsonata(value, expected):
    state_machine = {
        "StartAt": "x",
        "States": {
            "x": {
                "Type": "Task",
                "QueryLanguage": "JSONata",
                "Arguments": value,
                "End": True,
            }
        },
    }
    assert Linter.validate(state_machine) == [
        f"State Machine.States.x.Arguments is {expected} but should be a JSONata"
    ]


def test_unknown_query_language():
    state_machine = {
        "StartAt": "x",
        "QueryLanguage": "Yaml",
        "States": {
            "x": {
                "Type": "Fail",
            }
        },
    }
    assert Linter.validate(state_machine) == [
        'State Machine.QueryLanguage is "Yaml", not one of the allowed values '
        '["JSONPath", "JSONata"]',
    ]
