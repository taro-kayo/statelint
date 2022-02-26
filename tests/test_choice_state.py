from statelint.linter import Linter


def test_ok():
    state_machine = {
        "States": {
            "x": {
                "Type": "Choice",
                "Choices": [{"Variable": "$", "IsNull": True, "Next": "y"}],
                "Default": "z",
            },
            "y": {"Type": "Succeed"},
            "z": {"Type": "Succeed"},
        },
        "StartAt": "x",
    }
    assert Linter.validate(state_machine) == []


def test_ok_without_default():
    state_machine = {
        "States": {
            "x": {
                "Type": "Choice",
                "Choices": [{"Variable": "$", "IsNull": True, "Next": "y"}],
            },
            "y": {"Type": "Succeed"},
        },
        "StartAt": "x",
    }
    assert Linter.validate(state_machine) == []


def test_empty_choices():
    state_machine = {
        "States": {
            "x": {
                "Type": "Choice",
                "Choices": [],
                "Default": "z",
            },
            "z": {"Type": "Succeed"},
        },
        "StartAt": "x",
    }
    assert Linter.validate(state_machine) == [
        "State Machine.States.x.Choices is empty, non-empty required"
    ]


def test_next_end():
    state_machine = {
        "States": {
            "x": {
                "Type": "Choice",
                "Choices": [{"Variable": "$", "IsNull": True, "Next": "y"}],
                "Next": "z",
                "End": True,
            },
            "y": {"Type": "Succeed"},
            "z": {"Type": "Succeed"},
        },
        "StartAt": "x",
    }
    assert Linter.validate(state_machine) == [
        'State Machine.States.x has forbidden field "Next"',
        'State Machine.States.x has forbidden field "End"',
    ]


def test_not_numeric():
    state_machine = {
        "States": {
            "x": {
                "Type": "Choice",
                "Choices": [{"Variable": "$", "NumericEquals": "1", "Next": "y"}, None],
                "Default": "z",
            },
            "y": {"Type": "Succeed"},
            "z": {"Type": "Succeed"},
        },
        "StartAt": "x",
    }
    assert Linter.validate(state_machine) == [
        "State Machine.States.x.Choices[1] is null but should be an Object",
        'State Machine.States.x.Choices[0].NumericEquals is "1" but should be numeric',
    ]


def test_non_list_choices():
    state_machine = {
        "States": {
            "x": {"Type": "Choice", "Choices": {}, "Default": "y"},
            "y": {"Type": "Succeed"},
        },
        "StartAt": "x",
    }
    assert Linter.validate(state_machine) == [
        "State Machine.States.x.Choices is {} but should be an Array"
    ]
