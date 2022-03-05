import pytest

from statelint.linter import Linter


@pytest.mark.parametrize(
    "comparison,comparison_value",
    [
        ("StringEquals", "x"),
        ("StringLessThan", "x"),
        ("StringGreaterThan", "x"),
        ("StringLessThanEquals", "x"),
        ("StringGreaterThanEquals", "x"),
        ("NumericEquals", 1.2),
        ("NumericLessThan", -1),
        ("NumericGreaterThan", 0),
        ("NumericLessThanEquals", 0.0),
        ("NumericGreaterThanEquals", 999999999),
        ("BooleanEquals", False),
        ("TimestampEquals", "2001-01-01T12:00:00Z"),
        ("TimestampLessThan", "2001-01-01T12:00:00Z"),
        ("TimestampGreaterThan", "2001-01-01T12:00:00Z"),
        ("TimestampLessThanEquals", "2001-01-01T12:00:00Z"),
        ("TimestampGreaterThanEquals", "2001-01-01T12:00:00Z"),
        ("IsNull", True),
        ("IsPresent", True),
        ("IsNumeric", True),
        ("IsString", True),
        ("IsBoolean", True),
        ("IsTimestamp", True),
        ("StringMatches", "a*"),
        ("StringEqualsPath", "$"),
        ("StringLessThanPath", "$.x"),
        ("StringGreaterThanPath", "$"),
        ("StringLessThanEqualsPath", "$"),
        ("StringGreaterThanEqualsPath", "$"),
        ("NumericEqualsPath", "$"),
        ("NumericLessThanPath", "$"),
        ("NumericGreaterThanPath", "$"),
        ("NumericLessThanEqualsPath", "$"),
        ("NumericGreaterThanEqualsPath", "$"),
        ("BooleanEqualsPath", "$"),
        ("TimestampEqualsPath", "$"),
        ("TimestampLessThanPath", "$"),
        ("TimestampGreaterThanPath", "$"),
        ("TimestampLessThanEqualsPath", "$"),
        ("TimestampGreaterThanEqualsPath", "$"),
    ],
)
def test_ok(comparison, comparison_value):
    state_machine = {
        "States": {
            "x": {
                "Type": "Choice",
                "Comment": "aaa",
                "Choices": [
                    {
                        "Comment": "aaa",
                        "And": [
                            {
                                "Or": [
                                    {
                                        "Variable": "$",
                                        comparison: comparison_value,
                                        "Comment": "aaa",
                                    },
                                    {"Variable": "$", "IsNull": False},
                                ]
                            },
                            {
                                "Not": {
                                    "And": [
                                        {"Variable": "$", "IsNull": False},
                                        {"Variable": "$", "IsNull": True},
                                    ]
                                }
                            },
                        ],
                        "Next": "y",
                    }
                ],
                "Default": "z",
            },
            "y": {"Type": "Succeed"},
            "z": {"Type": "Succeed"},
        },
        "StartAt": "x",
    }
    assert Linter.validate(state_machine) == []


@pytest.mark.parametrize(
    "comparison,comparison_value,problems",
    [
        (
            "StringEquals",
            None,
            [
                "State Machine.States.x.Choices[0].And[0].Or[0].StringEquals "
                "should be non-null"
            ],
        ),
        (
            "StringLessThan",
            1,
            [
                "State Machine.States.x.Choices[0].And[0].Or[0].StringLessThan "
                "is 1 but should be a String"
            ],
        ),
        (
            "NumericEquals",
            None,
            [
                "State Machine.States.x.Choices[0].And[0].Or[0].NumericEquals "
                "should be non-null"
            ],
        ),
        (
            "NumericLessThan",
            "1",
            [
                "State Machine.States.x.Choices[0].And[0].Or[0].NumericLessThan "
                'is "1" but should be numeric'
            ],
        ),
        (
            "BooleanEquals",
            None,
            [
                "State Machine.States.x.Choices[0].And[0].Or[0].BooleanEquals "
                "should be non-null"
            ],
        ),
        (
            "TimestampEquals",
            None,
            [
                "State Machine.States.x.Choices[0].And[0].Or[0].TimestampEquals "
                "should be non-null"
            ],
        ),
        (
            "TimestampLessThan",
            "x",
            [
                "State Machine.States.x.Choices[0].And[0].Or[0].TimestampLessThan "
                'is "x" but should be an RFC3339 timestamp'
            ],
        ),
        (
            "IsNull",
            None,
            [
                "State Machine.States.x.Choices[0].And[0].Or[0].IsNull should be "
                "non-null"
            ],
        ),
        (
            "IsPresent",
            1,
            [
                "State Machine.States.x.Choices[0].And[0].Or[0].IsPresent is 1 "
                "but should be a Boolean"
            ],
        ),
        (
            "IsNumeric",
            "True",
            [
                "State Machine.States.x.Choices[0].And[0].Or[0].IsNumeric is "
                '"True" but should be a Boolean'
            ],
        ),
        (
            "StringMatches",
            None,
            [
                "State Machine.States.x.Choices[0].And[0].Or[0].StringMatches "
                "should be non-null"
            ],
        ),
        (
            "StringEqualsPath",
            None,
            [
                "State Machine.States.x.Choices[0].And[0].Or[0].StringEqualsPath "
                "should be non-null"
            ],
        ),
        (
            "StringLessThanPath",
            "x",
            [
                "State Machine.States.x.Choices[0].And[0].Or[0].StringLessThanPath is "
                '"x" but should be a Reference Path'
            ],
        ),
    ],
)
def test_ng(comparison, comparison_value, problems):
    state_machine = {
        "States": {
            "x": {
                "Type": "Choice",
                "Choices": [
                    {
                        "And": [
                            {"Or": [{"Variable": "$", comparison: comparison_value}]}
                        ],
                        "Next": "y",
                    }
                ],
            },
            "y": {"Type": "Succeed"},
        },
        "StartAt": "x",
    }
    assert Linter.validate(state_machine) == problems


def test_ok_all_of_or_not_and():
    state_machine = {
        "States": {
            "x": {
                "Type": "Choice",
                "Choices": [
                    {
                        "And": [{"Variable": "$", "IsNull": True}],
                        "Or": [{"Variable": "$", "IsNull": False}],
                        "Not": {"Variable": "$", "IsNull": False},
                        "Next": "y",
                    }
                ],
                "Default": "z",
            },
            "y": {"Type": "Succeed"},
            "z": {"Type": "Succeed"},
        },
        "StartAt": "x",
    }
    assert Linter.validate(state_machine) == []


def test_empty_at_deep_choice():
    state_machine = {
        "States": {
            "x": {
                "Type": "Choice",
                "Choices": [
                    {
                        "And": [
                            {
                                "Or": [
                                    {"Variable": "$", "IsNull": True, "Not": {}},
                                    {"Variable": "$", "IsNull": False},
                                ]
                            },
                            {"Not": {"And": []}},
                        ],
                        "Next": "y",
                    }
                ],
                "Default": "z",
            },
            "y": {"Type": "Succeed"},
            "z": {"Type": "Succeed"},
        },
        "StartAt": "x",
    }
    assert Linter.validate(state_machine) == [
        'State Machine.States.x.Choices[0].And[0].Or[0] has forbidden field "Not"',
        "State Machine.States.x.Choices[0].And[1].Not.And is empty, non-empty required",
    ]


def test_next_in_nested_rule():
    state_machine = {
        "States": {
            "x": {
                "Type": "Choice",
                "Choices": [
                    {
                        "And": [
                            {"Or": [{"Variable": "$", "IsNull": True, "Next": "y"}]},
                        ],
                        "Next": "y",
                    }
                ],
                "Default": "y",
            },
            "y": {"Type": "Succeed"},
        },
        "StartAt": "x",
    }
    assert Linter.validate(state_machine) == [
        'State Machine.States.x.Choices[0].And[0].Or[0] has forbidden field "Next"'
    ]
