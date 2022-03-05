from statelint.linter import Linter


def test_ok():
    state_machine = {
        "States": {
            "x": {
                "Type": "Parallel",
                "ResultPath": None,
                "Parameters": {},
                "ResultSelector": {},
                "Retry": [{"ErrorEquals": ["E"]}],
                "Catch": [{"ErrorEquals": ["E"], "Next": "y"}],
                "Branches": [{"StartAt": "z", "States": {"z": {"Type": "Fail"}}}],
                "End": True,
            },
            "y": {"Type": "Succeed"},
        },
        "StartAt": "x",
    }
    assert Linter.validate(state_machine) == []


def test_empty():
    state_machine = {
        "States": {"x": {"Type": "Parallel"}},
        "StartAt": "x",
    }
    assert Linter.validate(state_machine) == [
        'State Machine.States.x does not have required field "Next"',
        'State Machine.States.x does not have required field "Branches"',
        "No terminal state found in machine at State Machine.States",
    ]


def test_empty_branches():
    state_machine = {
        "States": {
            "x": {
                "Type": "Parallel",
                "Branches": [],
                "End": True,
            },
        },
        "StartAt": "x",
    }
    assert Linter.validate(state_machine) == []


def test_no_transition():
    state_machine = {
        "States": {
            "x": {
                "Type": "Parallel",
                "ResultPath": None,
                "Parameters": {},
                "ResultSelector": {},
                "Retry": [{"ErrorEquals": ["E"]}],
                "Catch": [{"ErrorEquals": ["E"], "Next": "y"}],
                "Branches": [
                    {
                        "StartAt": "z",
                        "States": {"z": {"Type": "Fail"}, "z2": {"Type": "Fail"}},
                    }
                ],
                "End": True,
            },
            "y": {"Type": "Succeed"},
        },
        "StartAt": "x",
    }
    assert Linter.validate(state_machine) == [
        "No transition found to state State Machine.States.x.Branches[0].z2"
    ]
