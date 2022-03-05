import pytest

from statelint.linter import Linter


@pytest.mark.parametrize(
    "parameters,expected",
    [
        (None, []),
        ([], []),
        ("x", []),
        (
            {
                "a": {
                    "b.$": "$[0].c",
                    "d.$": "States.Format('{}_{}', $$.Execution.Name, $.e)",
                }
            },
            [],
        ),
        (
            {
                "a": {
                    "b.$": "States.Format('{}_{}', $$.Execution.Name, $.e",
                }
            },
            [
                'Field "b.$" of Parameters at "State Machine.States.x.a" is not '
                "a JSONPath or intrinsic function expression"
            ],
        ),
        (
            {"a": [{"b.$": "c", "d.$": "e"}]},
            [
                # TODO: awslabs' output doesn't contain `.States`.
                'Field "b.$" of Parameters at "State Machine.States.x.a[0]" is not '
                "a JSONPath or intrinsic function expression",
                'Field "d.$" of Parameters at "State Machine.States.x.a[0]" is not '
                "a JSONPath or intrinsic function expression",
            ],
        ),
        (
            {"a": [{"b": [{}, {"c": {"d.$": "x"}}]}]},
            [
                'Field "d.$" of Parameters at "State Machine.States.x.a[0].b[1].c" '
                "is not a JSONPath or intrinsic function expression",
            ],
        ),
        (
            {"a.$": None},
            [
                'Field "a.$" of Parameters at "State Machine.States.x" is not '
                "a JSONPath or intrinsic function expression",
            ],
        ),
    ],
)
def test_main(parameters, expected):
    state_machine = {
        "States": {"x": {"Type": "Pass", "End": True, "Parameters": parameters}},
        "StartAt": "x",
    }
    assert Linter.validate(state_machine) == expected
