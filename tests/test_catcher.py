from statelint.linter import Linter


def test_ok():
    state_machine = {
        "States": {
            "x": {
                "Type": "Task",
                "End": True,
                "Resource": "arn:x",
                "Catch": [
                    {
                        "ErrorEquals": ["States.ALL"],
                        "ResultPath": None,
                        "Next": "y",
                    }
                ],
            },
            "y": {"Type": "Succeed"},
        },
        "StartAt": "x",
    }
    assert Linter.validate(state_machine) == []


def test_empty_error_equals():
    state_machine = {
        "States": {
            "x": {
                "Type": "Task",
                "End": True,
                "Resource": "arn:x",
                "Catch": [{"ErrorEquals": [], "Next": "x"}],
            }
        },
        "StartAt": "x",
    }
    assert Linter.validate(state_machine) == [
        "State Machine.States.x.Catch[0].ErrorEquals is empty, non-empty required"
    ]


def test_empty():
    state_machine = {
        "States": {
            "x": {
                "Type": "Task",
                "End": True,
                "Resource": "arn:x",
                "Catch": [{}],
            }
        },
        "StartAt": "x",
    }
    assert Linter.validate(state_machine) == [
        'State Machine.States.x.Catch[0] does not have required field "ErrorEquals"',
        'State Machine.States.x.Catch[0] does not have required field "Next"',
    ]


def test_states_all_not_by_itself():
    state_machine = {
        "States": {
            "x": {
                "Type": "Task",
                "End": True,
                "Resource": "arn:x",
                "Catch": [
                    {
                        "ErrorEquals": ["ValueError", "States.ALL", "KeyError"],
                        "ResultPath": None,
                        "Next": "y",
                    }
                ],
            },
            "y": {"Type": "Succeed"},
        },
        "StartAt": "x",
    }
    assert Linter.validate(state_machine) == [
        "State Machine.States.x.Catch[0]: States.ALL can only "
        "appear in the last element, and by itself."
    ]


def test_states_all_not_last():
    state_machine = {
        "States": {
            "x": {
                "Type": "Task",
                "End": True,
                "Resource": "arn:x",
                "Catch": [
                    {
                        "ErrorEquals": ["States.ALL"],
                        "ResultPath": None,
                        "Next": "y",
                    },
                    {
                        "ErrorEquals": ["ValueError", "KeyError"],
                        "ResultPath": None,
                        "Next": "y",
                    },
                ],
            },
            "y": {"Type": "Succeed"},
        },
        "StartAt": "x",
    }
    assert Linter.validate(state_machine) == [
        "State Machine.States.x.Catch[0]: States.ALL can only "
        "appear in the last element, and by itself."
    ]
