import itertools
import json
import os.path
from unittest import mock
from unittest.mock import call

import pytest

from statelint.cli import main


@pytest.mark.parametrize(
    "arg_0,expected_exit_code,problems",
    [
        ({"StartAt": "x", "States": {"x": {"Type": "Fail"}}}, 0, []),
        (
            {"StartAt": "x", "States": {}},
            1,
            [
                "One error:",
                " StartAt value x not found in States field at State Machine",
            ],
        ),
        (
            {"StartAt": "x", "States": {"x": {"Type": "Task"}}},
            1,
            [
                "2 errors:",
                ' State Machine.States.x does not have required field "Next"',
                " No terminal state found in machine at State Machine.States",
            ],
        ),
    ],
)
@mock.patch("builtins.print")
def test_main(mocked_print, arg_0, expected_exit_code, problems):
    exit_code = main([json.dumps(arg_0)])
    assert mocked_print.mock_calls == [call(p) for p in problems]
    assert exit_code == expected_exit_code


@pytest.mark.parametrize(
    "arg_1,problems",
    [
        (
            "--ignore=FLOAT",
            [
                "One error:",
                ' State Machine.States.x.Resource is "x" but should be A URI',
            ],
        ),
        (
            "--ignore=URI",
            [
                "One error:",
                " State Machine.States.x.Retry[0].BackoffRate is 1 but should be "
                "a Float",
            ],
        ),
        ("--ignore=FLOAT,URI", []),
        ("--ignore=URI,FLOAT", []),
    ],
)
@mock.patch("builtins.print")
def test_ignore(mocked_print, arg_1, problems):
    arg_0 = json.dumps(
        {
            "StartAt": "x",
            "States": {
                "x": {
                    "Type": "Task",
                    "Resource": "x",
                    "End": True,
                    "Retry": [{"ErrorEquals": ["e"], "BackoffRate": 1}],
                }
            },
        }
    )
    main([arg_0, arg_1])
    assert mocked_print.mock_calls == [call(p) for p in problems]


@pytest.mark.parametrize("ignore", ["", "ARRAY"])
def test_invalid_ignore(ignore):
    with pytest.raises(SystemExit):
        main(["{}", f"--ignore={ignore}"])


def test_yaml():
    yaml_path = os.path.join(
        os.path.dirname(__file__), "data", "batch-job-notification.yaml"
    )
    assert main([yaml_path, "--yaml"]) == 0


@mock.patch("builtins.print")
@mock.patch("statelint.cli.importlib.import_module")
def test_yaml_not_installed(import_module, *_):
    import_module.side_effect = ImportError()
    assert main(["{}", "--yaml"]) == 2


@mock.patch("statelint.cli.sys.argv", ["", "{}"])
@mock.patch("builtins.print")
def test_default_argv(mocked_print):
    assert main() == 1
    assert mocked_print.mock_calls == [
        call("2 errors:"),
        call(' State Machine does not have required field "States"'),
        call(' State Machine does not have required field "StartAt"'),
    ]


@mock.patch("builtins.print")
def test_multiple_input(mocked_print):
    args = ['{"Comment":"1"}', "{}"]
    assert main(args) == 1

    assert mocked_print.mock_calls == list(
        itertools.chain.from_iterable(
            [
                call(arg),
                call("2 errors:"),
                call(' State Machine does not have required field "States"'),
                call(' State Machine does not have required field "StartAt"'),
            ]
            for arg in args
        )
    )
