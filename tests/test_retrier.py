from statelint.linter import Linter


def test_ok():
    state_machine = {
        "States": {
            "x": {
                "Type": "Task",
                "End": True,
                "Resource": "arn:x",
                "Retry": [
                    {
                        "ErrorEquals": ["E"],
                        "IntervalSeconds": 99999999,
                        "MaxAttempts": 99999998,
                        "BackoffRate": 1.0,
                    }
                ],
            },
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
                "Resource": "arn:x",
                "Retry": [
                    {
                        "ErrorEquals": [],
                        "IntervalSeconds": -1,
                        "MaxAttempts": 0,
                        "BackoffRate": 1,
                    }
                ],
            },
        },
        "StartAt": "x",
    }
    assert Linter.validate(state_machine) == [
        "State Machine.States.x.Retry[0].ErrorEquals is empty, non-empty required",
        "State Machine.States.x.Retry[0].IntervalSeconds is -1 but allowed floor is 0",
        "State Machine.States.x.Retry[0].BackoffRate is 1 but should be a Float",
    ]
