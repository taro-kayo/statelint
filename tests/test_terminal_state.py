from statelint.linter import Linter


def test_end():
    state_machine = {"States": {"x": {"Type": "Succeed", "End": True}}, "StartAt": "x"}
    assert Linter.validate(state_machine) == [
        'Field "End" not allowed in State Machine.States.x'
    ]


def test_fail_state_fields():
    state_machine = {
        "States": {
            "x": {
                "Type": "Fail",
                "Cause": "c",
                "Error": "e",
                "InputPath": "$",
                "OutputPath": "$",
                "Next": "y",
            }
        },
        "StartAt": "x",
    }
    assert Linter.validate(state_machine) == [
        'State Machine.States.x has forbidden field "InputPath"',
        'State Machine.States.x has forbidden field "OutputPath"',
        'State Machine.States.x has forbidden field "Next"',
        'No state found named "y", referenced at State Machine.States.x.Next',
    ]


def test_succeed_state_fields():
    state_machine = {
        "States": {
            "x": {
                "Type": "Succeed",
                "Cause": "c",
                "Error": "e",
                "InputPath": "$",
                "OutputPath": "$",
                "Next": "y",
            }
        },
        "StartAt": "x",
    }
    assert Linter.validate(state_machine) == [
        'State Machine.States.x has forbidden field "Next"',
        'Field "Cause" not allowed in State Machine.States.x',
        'Field "Error" not allowed in State Machine.States.x',
        'No state found named "y", referenced at State Machine.States.x.Next',
    ]
