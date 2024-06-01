import pytest

from statelint.linter import Linter


@pytest.mark.parametrize(
    "props",
    [
        {"IntervalSeconds": 1, "MaxAttempts": 0, "JitterStrategy": "FULL"},
        {
            "IntervalSeconds": 99999999,
            "MaxAttempts": 99999998,
            "JitterStrategy": "NONE",
        },
    ],
)
def test_ok(props):
    state_machine = {
        "States": {
            "x": {
                "Type": "Task",
                "End": True,
                "Resource": "arn:x",
                "Retry": [
                    {
                        "ErrorEquals": ["E"],
                        "BackoffRate": 1.0,
                        "MaxDelaySeconds": 4,
                        **props,
                    }
                ],
            },
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
                "Retry": [{"ErrorEquals": ["E"]}],
            },
        },
        "StartAt": "x",
    }
    assert Linter.validate(state_machine) == []


@pytest.mark.parametrize(
    "props,errors",
    [
        (
            {"ErrorEquals": []},
            [
                "State Machine.States.x.Retry[0].ErrorEquals is empty, non-empty "
                "required",
            ],
        ),
        (
            {"IntervalSeconds": 0},
            [
                "State Machine.States.x.Retry[0].IntervalSeconds is 0 but allowed "
                "floor is 0",
            ],
        ),
        (
            {"MaxAttempts": -1},
            [
                "State Machine.States.x.Retry[0].MaxAttempts is -1 but allowed floor "
                "is -1",
            ],
        ),
        (
            {"MaxAttempts": 99999999},
            [
                "State Machine.States.x.Retry[0].MaxAttempts is 99999999 but allowed "
                "ceiling is 99999999",
            ],
        ),
        (
            {"BackoffRate": 1},
            [
                "State Machine.States.x.Retry[0].BackoffRate is 1 but should be a "
                "Float",
            ],
        ),
        (
            {"MaxDelaySeconds": 0},
            [
                "State Machine.States.x.Retry[0].MaxDelaySeconds is 0 but allowed "
                "floor is 0",
            ],
        ),
        (
            {"JitterStrategy": None},
            [
                "State Machine.States.x.Retry[0].JitterStrategy should be non-null",
                'State Machine.States.x.Retry[0].JitterStrategy is "", not one of the '
                'allowed values ["FULL", "NONE"]',
            ],
        ),
        (
            {"JitterStrategy": "SAMPLE"},
            [
                'State Machine.States.x.Retry[0].JitterStrategy is "SAMPLE", not one '
                'of the allowed values ["FULL", "NONE"]',
            ],
        ),
    ],
)
def test_bad_fields(props, errors):
    state_machine = {
        "States": {
            "x": {
                "Type": "Task",
                "End": True,
                "Resource": "arn:x",
                "Retry": [{"ErrorEquals": ["E"], **props}],
            },
        },
        "StartAt": "x",
    }
    assert Linter.validate(state_machine) == errors
