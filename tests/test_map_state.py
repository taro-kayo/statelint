from statelint.linter import Linter


def test_ok():
    state_machine = {
        "States": {
            "x": {
                "Type": "Map",
                "ResultPath": None,
                "Parameters": {},
                "ResultSelector": {},
                "ItemsPath": "$$.x",
                "MaxConcurrency": 9999999999,
                "Retry": [{"ErrorEquals": ["E"]}],
                "Catch": [{"ErrorEquals": ["E"], "Next": "y"}],
                "Iterator": {"StartAt": "z", "States": {"z": {"Type": "Fail"}}},
                "End": True,
            },
            "y": {"Type": "Succeed"},
        },
        "StartAt": "x",
    }
    assert Linter.validate(state_machine) == []


def test_iterator_is_not_dict():
    state_machine = {
        "States": {
            "x": {
                "Type": "Map",
                "ResultPath": None,
                "Parameters": {},
                "ResultSelector": {},
                "Retry": [{"ErrorEquals": ["E"]}],
                "Catch": [{"ErrorEquals": ["E"], "Next": "y"}],
                "Iterator": [],
                "End": True,
            },
            "y": {"Type": "Succeed"},
        },
        "StartAt": "x",
    }
    assert Linter.validate(state_machine) == [
        "State Machine.States.x.Iterator is [] but should be an Object"
    ]


def test_empty():
    state_machine = {
        "States": {"x": {"Type": "Map"}},
        "StartAt": "x",
    }
    assert Linter.validate(state_machine) == [
        'State Machine.States.x does not have required field "Next"',
        'State Machine.States.x does not have required field "Iterator"',
        "No terminal state found in machine at State Machine.States",
    ]


def test_empty_iterator():
    state_machine = {
        "States": {
            "x": {
                "Type": "Map",
                "Iterator": {},
                "End": True,
            },
        },
        "StartAt": "x",
    }
    assert Linter.validate(state_machine) == [
        'State Machine.States.x.Iterator does not have required field "States"',
        'State Machine.States.x.Iterator does not have required field "StartAt"',
    ]


def test_redefine_state():
    state_machine = {
        "States": {
            "x": {
                "Type": "Map",
                "ItemsPath": "$.x",
                "Iterator": {"StartAt": "x", "States": {"x": {"Type": "Fail"}}},
                "End": True,
            },
        },
        "StartAt": "x",
    }
    assert Linter.validate(state_machine) == [
        'State "x", defined at State Machine.States.x.Iterator.States, '
        "is also defined at State Machine.States",
    ]
