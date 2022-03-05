import os.path

import pytest
from statelint.linter import Linter


@pytest.mark.parametrize(
    "filepath,expected",
    [
        ("choice-with-context-object.json", []),
        (
            "choice-with-parameters.json",
            ['Field "Parameters" not allowed in State Machine.States.p'],
        ),
        (
            "choice-with-resultpath.json",
            ['Field "ResultPath" not allowed in State Machine.States.p'],
        ),
        (
            "choice-with-resultselector.json",
            ['Field "ResultSelector" not allowed in State Machine.States.p'],
        ),
        (
            "empty-error-equals-on-catch.json",
            [
                "State Machine.States.p.Catch[0].ErrorEquals is empty, "
                "non-empty required"
            ],
        ),
        (
            "empty-error-equals-on-retry.json",
            [
                "State Machine.States.p.Retry[0].ErrorEquals is empty, "
                "non-empty required"
            ],
        ),
        (
            "fail-with-parameters.json",
            ['Field "Parameters" not allowed in State Machine.States.p'],
        ),
        (
            "fail-with-resultpath.json",
            ['Field "ResultPath" not allowed in State Machine.States.p'],
        ),
        (
            "fail-with-resultselector.json",
            ['Field "ResultSelector" not allowed in State Machine.States.p'],
        ),
        (
            "has-dupes.json",
            [
                'State "Sub2_1", defined at State Machine.States.A.Branches[1].States, '
                "is also defined at State Machine.States"
            ],
        ),
        (
            "invalid-function-invocation.json",
            [
                'Field "abc.$" of ResultSelector at "State Machine.States.p" is not '
                "a JSONPath or intrinsic function expression"
            ],
        ),
        (
            "linked-parallel.json",
            [
                'No state found named "Sub2_1", referenced at '
                "State Machine.States.A.Branches[0].States.Sub1_1.Next",
                "No terminal state found in machine at "
                "State Machine.States.A.Branches[0].States",
                'No state found named "Sub1_1", referenced at '
                "State Machine.States.X.Default",
                'No state found named "Sub1_1", referenced at '
                "State Machine.States.X.Choices[0].Next",
            ],
        ),
        ("map-with-itemspath-context-object.json", []),
        (
            "map-with-null-itemspath.json",
            # TODO
            # ['Field "ItemsPath" defined at "State Machine.m" should be non-null'],
            ["State Machine.States.m.ItemsPath should be non-null"],
        ),
        ("map-with-parameters.json", []),
        ("map-with-resultselector.json", []),
        ("minimal-fail-state.json", []),
        (
            "no-terminal.json",
            ["No terminal state found in machine at State Machine.States"],
        ),
        ("parallel-with-parameters.json", []),
        ("parallel-with-resultpath.json", []),
        ("parallel-with-resultselector.json", []),
        (
            "parameter-path-problems.json",
            [
                'Field "bad1.$" of Parameters at "State Machine.States.FNORD" is not '
                "a JSONPath or intrinsic function expression",
                'Field "bad2.$" of Parameters at "State Machine.States.FNORD" is not '
                "a JSONPath or intrinsic function expression",
                'Field "bad3.$" of Parameters at "State Machine.States.FNORD.f3" '
                "is not a JSONPath or intrinsic function expression",
                'Field "bad4.$" of Parameters at '
                '"State Machine.States.FNORD.f3.f5[1].f7" is not a JSONPath or '
                "intrinsic function expression",
                'Field "bad5.$" of Parameters at "State Machine.States.FNORD" is not '
                "a JSONPath or intrinsic function expression",
            ],
        ),
        ("pass-with-intrinsic-function-inputpath.json", []),
        ("pass-with-io-path-context-object.json", []),
        ("pass-with-null-inputpath.json", []),
        ("pass-with-null-outputpath.json", []),
        ("pass-with-parameters.json", []),
        ("pass-with-resultpath.json", []),
        (
            "pass-with-resultselector.json",
            ['Field "ResultSelector" not allowed in State Machine.States.p'],
        ),
        (
            "states-array-invocation-leftpad.json",
            [
                'Field "abc.$" of ResultSelector at "State Machine.States.p" is not '
                "a JSONPath or intrinsic function expression"
            ],
        ),
        ("states-array-invocation.json", []),
        ("states-format-invocation.json", []),
        ("states-jsontostring-invocation.json", []),
        ("states-stringtojson-invocation.json", []),
        (
            "succeed-with-parameters.json",
            ['Field "Parameters" not allowed in State Machine.States.p'],
        ),
        (
            "succeed-with-resultpath.json",
            ['Field "ResultPath" not allowed in State Machine.States.p'],
        ),
        (
            "succeed-with-resultselector.json",
            ['Field "ResultSelector" not allowed in State Machine.States.p'],
        ),
        ("task-with-dynamic-timeouts.json", []),
        ("task-with-parameters.json", []),
        ("task-with-resultpath.json", []),
        ("task-with-resultselector.json", []),
        (
            "task-with-static-and-dynamic-heartbeat.json",
            [
                "State Machine.States.p may have only one of "
                '["HeartbeatSeconds", "HeartbeatSecondsPath"]'
            ],
        ),
        (
            "task-with-static-and-dynamic-timeout.json",
            [
                "State Machine.States.p may have only one of "
                '["TimeoutSeconds", "TimeoutSecondsPath"]'
            ],
        ),
        (
            "wait-with-parameters.json",
            ['Field "Parameters" not allowed in State Machine.States.p'],
        ),
        (
            "wait-with-resultpath.json",
            ['Field "ResultPath" not allowed in State Machine.States.p'],
        ),
        (
            "wait-with-resultselector.json",
            ['Field "ResultSelector" not allowed in State Machine.States.p'],
        ),
    ],
)
def test_main(filepath, expected):
    assert Linter().validate(get_path(filepath)) == expected


def get_path(data_file_name):
    return os.path.join(os.path.dirname(__file__), "data", data_file_name)
