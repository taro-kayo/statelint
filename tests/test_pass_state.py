from statelint.linter import Linter


def test_ok_next():
    state_machine = {
        "States": {"x": {"Type": "Pass", "Next": "y"}, "y": {"Type": "Fail"}},
        "StartAt": "x",
    }
    assert Linter.validate(state_machine) == []


def test_ok_end():
    state_machine = {
        "States": {
            "x": {"Type": "Pass", "Parameters": {}, "Result": True, "End": True}
        },
        "StartAt": "x",
    }
    assert Linter.validate(state_machine) == []


def test_ok_result_path():
    state_machine = {
        "States": {"x": {"Type": "Pass", "End": True, "ResultPath": "$"}},
        "StartAt": "x",
    }
    assert Linter.validate(state_machine) == []


def test_both_next_and_end():
    state_machine = {
        "States": {"x": {"Type": "Pass", "Next": "y", "End": True}},
        "StartAt": "x",
    }
    assert Linter.validate(state_machine) == [
        'State Machine.States.x has forbidden field "Next"',
        'No state found named "y", referenced at State Machine.States.x.Next',
    ]


def test_empty():
    state_machine = {
        "States": {"x": {"Type": "Pass"}},
        "StartAt": "x",
    }
    assert Linter.validate(state_machine) == [
        'State Machine.States.x does not have required field "Next"',
        "No terminal state found in machine at State Machine.States",
    ]


def test_result_path():
    state_machine = {
        "States": {"x": {"Type": "Pass", "End": True, "ResultPath": "x"}},
        "StartAt": "x",
    }
    assert Linter.validate(state_machine) == [
        'State Machine.States.x.ResultPath is "x" but should be a Reference Path'
    ]
