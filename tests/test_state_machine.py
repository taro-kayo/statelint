from unittest.mock import Mock

import pytest

from statelint.linter import Linter
from statelint.nodes.state_machine import StateMachine


def test_ok():
    assert Linter.validate({"States": {"x": {"Type": "Succeed"}}, "StartAt": "x"}) == []


def test_required_fields():
    assert Linter.validate({"Comment": "xxx", "Version": "yyy"}) == [
        'State Machine does not have required field "States"',
        'State Machine does not have required field "StartAt"',
    ]


def test_not_allowed_fields():
    statemachine = {"States": {"x": {"Type": "Succeed"}}, "StartAt": "x", "a": 1}
    assert Linter.validate(statemachine) == [
        'Field "a" not allowed in State Machine',
    ]


def test_type_error():
    statemachine = {"States": "1", "StartAt": {"x": 1}}
    assert Linter.validate(statemachine) == [
        'State Machine.States is "1" but should be an Object',
        'State Machine.StartAt is {"x": 1} but should be a String',
    ]


@pytest.mark.parametrize(
    "timeout_sec,expected",
    [
        (0, ["State Machine.TimeoutSeconds is 0 but allowed floor is 0"]),
        (1.2, ["State Machine.TimeoutSeconds is 1.2 but should be an Integer"]),
        (42, []),
        (
            99999999,
            [
                "State Machine.TimeoutSeconds is 99999999 but "
                "allowed ceiling is 99999999"
            ],
        ),
    ],
)
def test_positive_int_fields(timeout_sec, expected):
    statemachine = {
        "States": {"x": {"Type": "Succeed"}},
        "StartAt": "x",
        "TimeoutSeconds": timeout_sec,
    }
    assert Linter.validate(statemachine) == expected


def test_no_start_at():
    state_machine = {"States": {"x": {"Type": "Succeed"}, "y": 1}}
    assert Linter.validate(state_machine) == [
        'State Machine does not have required field "StartAt"',
        "No transition found to state State Machine.x",
        "No transition found to state State Machine.y",
    ]


def test_bad_start_at():
    state_machine = {"States": {"y": {"Type": "Succeed"}}, "StartAt": "x"}
    assert Linter.validate(state_machine) == [
        "StartAt value x not found in States field at State Machine",
        "No transition found to state State Machine.y",
    ]


def test_no_transion():
    state_machine = {"States": {"x": {"Type": "Succeed"}, "y": 1}, "StartAt": "x"}
    assert Linter.validate(state_machine) == [
        "No transition found to state State Machine.y"
    ]


def test_loop():
    state_machine = {
        "States": {
            "x": {"Type": "Pass", "Next": "y"},
            "y": {"Type": "Pass", "Next": "x"},
        },
        "StartAt": "x",
    }
    assert Linter.validate(state_machine) == [
        "No terminal state found in machine at State Machine.States"
    ]


def test_no_terminal_state():
    state_machine = {"States": {"x": 1}, "StartAt": "x"}
    assert Linter.validate(state_machine) == [
        "No terminal state found in machine at State Machine.States"
    ]


def test_null_state():
    state_machine = {"States": {"x": None}, "StartAt": "x"}
    assert Linter.validate(state_machine) == [
        "No terminal state found in machine at State Machine.States"
    ]


def test_repr():
    assert (
        f'{StateMachine(Mock(), {"x": 42})}' == "StateMachine(State Machine, {'x': 42})"
    )
