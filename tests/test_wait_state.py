from statelint.linter import Linter


def test_ok():
    state_machine = {
        "States": {"x": {"Type": "Wait", "End": True, "Seconds": 1}},
        "StartAt": "x",
    }
    assert Linter.validate(state_machine) == []


def test_empty():
    state_machine = {
        "States": {"x": {"Type": "Wait", "End": True}},
        "StartAt": "x",
    }
    assert Linter.validate(state_machine) == [
        "State Machine.States.x does not have required field from "
        '["Seconds", "SecondsPath", "Timestamp", "TimestampPath"]',
    ]


def test_null_seconds_path():
    state_machine = {
        "States": {"x": {"Type": "Wait", "SecondsPath": None, "End": True}},
        "StartAt": "x",
    }
    assert Linter.validate(state_machine) == [
        "State Machine.States.x.SecondsPath should be non-null",
    ]


def test_2_out_of_4():
    state_machine = {
        "States": {
            "x": {"Type": "Wait", "End": True, "Seconds": 1, "TimestampPath": "$"}
        },
        "StartAt": "x",
    }
    assert Linter.validate(state_machine) == [
        "State Machine.States.x may have only one of "
        '["Seconds", "SecondsPath", "Timestamp", "TimestampPath"]'
    ]


def test_bad_timestamp():
    state_machine = {
        "States": {"x": {"Type": "Wait", "End": True, "Timestamp": 1}},
        "StartAt": "x",
    }
    assert Linter.validate(state_machine) == [
        "State Machine.States.x.Timestamp is 1 but should be an RFC3339 timestamp"
    ]


def test_null_timestamp():
    state_machine = {
        "States": {"x": {"Type": "Wait", "End": True, "Timestamp": None}},
        "StartAt": "x",
    }
    assert Linter.validate(state_machine) == [
        "State Machine.States.x.Timestamp should be non-null"
    ]
