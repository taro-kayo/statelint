import json

import pytest

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


def test_ok_min():
    state_machine = {
        "States": {
            "x": {
                "Type": "Map",
                "ItemsPath": "$$.x",
                "Iterator": {"StartAt": "y", "States": {"y": {"Type": "Fail"}}},
                "End": True,
            },
        },
        "StartAt": "x",
    }
    assert Linter.validate(state_machine) == []


@pytest.mark.parametrize(
    "reader_config,item_batcher,max_concurrency,tf_count,tf_per",
    [
        (
            {"MaxItems": 1},
            {"MaxItemsPerBatch": 1, "MaxInputBytesPerBatch": 1},
            {"MaxConcurrency": 9999999999},
            {"ToleratedFailureCount": 42},
            {"ToleratedFailurePercentage": 42},
        ),
        (
            {"MaxItemsPath": "$.x"},
            {"MaxItemsPerBatchPath": "$.x", "MaxInputBytesPerBatchPath": "$.x"},
            {"MaxConcurrencyPath": "$.x"},
            {"ToleratedFailureCountPath": "$.x"},
            {"ToleratedFailurePercentagePath": "$.x"},
        ),
    ],
)
def test_ok_2022(reader_config, item_batcher, max_concurrency, tf_count, tf_per):
    state_machine = {
        "States": {
            "x": {
                "Type": "Map",
                "ResultPath": None,
                "ItemSelector": {},
                "ResultSelector": {},
                "ItemsPath": "$$.x",
                **max_concurrency,
                **tf_count,
                **tf_per,
                "Retry": [{"ErrorEquals": ["E"]}],
                "Catch": [{"ErrorEquals": ["E"], "Next": "y"}],
                "ItemProcessor": {
                    "ProcessorConfig": {
                        "Mode": "DISTRIBUTED",
                        "ExecutionType": "EXPRESS",
                    },
                    "StartAt": "z",
                    "States": {"z": {"Type": "Fail"}},
                },
                "ItemReader": {
                    "Resource": "arn:x",
                    "Parameters": {},
                    "ReaderConfig": reader_config,
                },
                "ResultWriter": {
                    "Resource": "arn:x",
                    "Parameters": {},
                },
                "ItemBatcher": {
                    "BatchInput": {},
                    **item_batcher,
                },
                "End": True,
            },
            "y": {"Type": "Succeed"},
        },
        "StartAt": "x",
    }
    assert Linter.validate(state_machine) == []


def test_ok_2022_min():
    state_machine = {
        "States": {
            "x": {
                "Type": "Map",
                "ItemsPath": "$$.x",
                "ItemProcessor": {
                    "StartAt": "z",
                    "States": {"z": {"Type": "Fail"}},
                },
                "ItemReader": {"Resource": "arn:x"},
                "ResultWriter": {"Resource": "arn:x"},
                "ItemBatcher": {},
                "End": True,
            },
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


@pytest.mark.parametrize(
    "config",
    ["ItemReader", "ResultWriter"],
)
def test_ok_arguments(config):
    state_machine = {
        "States": {
            "x": {
                "Type": "Map",
                "QueryLanguage": "JSONata",
                "Items": [1, 2, 3],
                "Iterator": {"StartAt": "y", "States": {"y": {"Type": "Fail"}}},
                config: {"Resource": "arn:x", "Arguments": "{% $foo.bar %}"},
                "End": True,
            },
        },
        "StartAt": "x",
    }
    assert Linter.validate(state_machine) == []


@pytest.mark.parametrize(
    "items",
    ["{% states.input.detail.shipped %}", [1, "{% $two %}", 3]],
)
def test_ok_items(items):
    state_machine = {
        "States": {
            "x": {
                "Type": "Map",
                "QueryLanguage": "JSONata",
                "Items": items,
                "Iterator": {"StartAt": "y", "States": {"y": {"Type": "Fail"}}},
                "End": True,
            },
        },
        "StartAt": "x",
    }
    assert Linter.validate(state_machine) == []


def test_empty():
    state_machine = {
        "States": {"x": {"Type": "Map"}},
        "StartAt": "x",
    }
    assert Linter.validate(state_machine) == [
        'State Machine.States.x does not have required field "Next"',
        "State Machine.States.x does not have required field from "
        '["Iterator", "ItemProcessor"]',
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


@pytest.mark.parametrize("key", ("Iterator", "ItemProcessor"))
def test_redefine_state(key):
    state_machine = {
        "States": {
            "x": {
                "Type": "Map",
                "ItemsPath": "$.x",
                key: {"StartAt": "x", "States": {"x": {"Type": "Fail"}}},
                "End": True,
            },
        },
        "StartAt": "x",
    }
    assert Linter.validate(state_machine) == [
        f'State "x", defined at State Machine.States.x.{key}.States, '
        "is also defined at State Machine.States",
    ]


def test_empty_item_reader():
    state_machine = {
        "States": {
            "x": {
                "Type": "Map",
                "ItemsPath": "$$.x",
                "ItemProcessor": {
                    "StartAt": "z",
                    "States": {"z": {"Type": "Fail"}},
                },
                "ItemReader": {},
                "End": True,
            },
        },
        "StartAt": "x",
    }
    assert Linter.validate(state_machine) == [
        'State Machine.States.x.ItemReader does not have required field "Resource"'
    ]


def test_non_object_item_reader():
    state_machine = {
        "States": {
            "x": {
                "Type": "Map",
                "ItemsPath": "$$.x",
                "ItemProcessor": {
                    "StartAt": "z",
                    "States": {"z": {"Type": "Fail"}},
                },
                "ItemReader": "x",
                "End": True,
            },
        },
        "StartAt": "x",
    }
    assert Linter.validate(state_machine) == [
        'State Machine.States.x.ItemReader is "x" but should be an Object'
    ]


def test_empty_reader_config():
    state_machine = {
        "States": {
            "x": {
                "Type": "Map",
                "ItemsPath": "$$.x",
                "ItemProcessor": {
                    "StartAt": "z",
                    "States": {"z": {"Type": "Fail"}},
                },
                "ItemReader": {"Resource": "arn:x", "ReaderConfig": {}},
                "End": True,
            },
        },
        "StartAt": "x",
    }
    assert Linter.validate(state_machine) == []


def test_max_items_zero():
    state_machine = {
        "States": {
            "x": {
                "Type": "Map",
                "ItemsPath": "$$.x",
                "ItemProcessor": {
                    "StartAt": "z",
                    "States": {"z": {"Type": "Fail"}},
                },
                "ItemReader": {"Resource": "arn:x", "ReaderConfig": {"MaxItems": 0}},
                "End": True,
            },
        },
        "StartAt": "x",
    }
    assert Linter.validate(state_machine) == [
        "State Machine.States.x.ItemReader.ReaderConfig.MaxItems is 0 but allowed "
        "floor is 0",
    ]


def test_invalid_max_items_path():
    state_machine = {
        "States": {
            "x": {
                "Type": "Map",
                "ItemsPath": "$$.x",
                "ItemProcessor": {
                    "StartAt": "z",
                    "States": {"z": {"Type": "Fail"}},
                },
                "ItemReader": {
                    "Resource": "arn:x",
                    "ReaderConfig": {"MaxItemsPath": "x"},
                },
                "End": True,
            },
        },
        "StartAt": "x",
    }
    assert Linter.validate(state_machine) == [
        'State Machine.States.x.ItemReader.ReaderConfig.MaxItemsPath is "x" but '
        "should be a Reference Path",
    ]


def test_both_max_items():
    state_machine = {
        "States": {
            "x": {
                "Type": "Map",
                "ItemsPath": "$$.x",
                "ItemProcessor": {
                    "StartAt": "z",
                    "States": {"z": {"Type": "Fail"}},
                },
                "ItemReader": {
                    "Resource": "arn:x",
                    "ReaderConfig": {"MaxItems": 1, "MaxItemsPath": "$.x"},
                },
                "End": True,
            },
        },
        "StartAt": "x",
    }
    assert Linter.validate(state_machine) == [
        "State Machine.States.x.ItemReader.ReaderConfig may have only one of "
        '["MaxItems", "MaxItemsPath"]',
    ]


def test_empty_result_writer():
    state_machine = {
        "States": {
            "x": {
                "Type": "Map",
                "ItemsPath": "$$.x",
                "ItemProcessor": {
                    "StartAt": "z",
                    "States": {"z": {"Type": "Fail"}},
                },
                "ResultWriter": {},
                "End": True,
            },
        },
        "StartAt": "x",
    }
    assert Linter.validate(state_machine) == [
        'State Machine.States.x.ResultWriter does not have required field "Resource"'
    ]


def test_non_object_result_writer():
    state_machine = {
        "States": {
            "x": {
                "Type": "Map",
                "ItemsPath": "$$.x",
                "ItemProcessor": {
                    "StartAt": "z",
                    "States": {"z": {"Type": "Fail"}},
                },
                "ResultWriter": "x",
                "End": True,
            },
        },
        "StartAt": "x",
    }
    assert Linter.validate(state_machine) == [
        'State Machine.States.x.ResultWriter is "x" but should be an Object'
    ]


def test_result_writer_with_reader_config():
    state_machine = {
        "States": {
            "x": {
                "Type": "Map",
                "ItemsPath": "$$.x",
                "ItemProcessor": {
                    "StartAt": "z",
                    "States": {"z": {"Type": "Fail"}},
                },
                "ResultWriter": {"Resource": "arn:x", "ReaderConfig": {"MaxItems": 1}},
                "End": True,
            },
        },
        "StartAt": "x",
    }
    assert Linter.validate(state_machine) == [
        'Field "ReaderConfig" not allowed in State Machine.States.x.ResultWriter'
    ]


def test_non_object_processor_config():
    state_machine = {
        "States": {
            "x": {
                "Type": "Map",
                "ItemsPath": "$$.x",
                "ItemProcessor": {
                    "ProcessorConfig": "x",
                    "StartAt": "z",
                    "States": {"z": {"Type": "Fail"}},
                },
                "End": True,
            },
        },
        "StartAt": "x",
    }
    assert Linter.validate(state_machine) == [
        'State Machine.States.x.ItemProcessor.ProcessorConfig is "x" '
        "but should be an Object"
    ]


def test_both_parameters_and_item_selector():
    state_machine = {
        "States": {
            "x": {
                "Type": "Map",
                "Parameters": {},
                "ItemSelector": {},
                "ItemsPath": "$$.x",
                "ItemProcessor": {
                    "StartAt": "z",
                    "States": {"z": {"Type": "Fail"}},
                },
                "End": True,
            },
        },
        "StartAt": "x",
    }
    assert Linter.validate(state_machine) == [
        'State Machine.States.x may have only one of ["Parameters", "ItemSelector"]',
    ]


def test_max_items_batcher_zero():
    state_machine = {
        "States": {
            "x": {
                "Type": "Map",
                "ItemsPath": "$$.x",
                "ItemProcessor": {
                    "StartAt": "z",
                    "States": {"z": {"Type": "Fail"}},
                },
                "ItemBatcher": {"MaxItemsPerBatch": 0, "MaxInputBytesPerBatch": 0},
                "End": True,
            },
        },
        "StartAt": "x",
    }
    assert Linter.validate(state_machine) == [
        "State Machine.States.x.ItemBatcher.MaxItemsPerBatch is 0 but allowed floor "
        "is 0",
        "State Machine.States.x.ItemBatcher.MaxInputBytesPerBatch is 0 but allowed "
        "floor is 0",
    ]


def test_max_items_batcher_invalid_uri():
    state_machine = {
        "States": {
            "x": {
                "Type": "Map",
                "ItemsPath": "$$.x",
                "ItemProcessor": {
                    "StartAt": "z",
                    "States": {"z": {"Type": "Fail"}},
                },
                "ItemBatcher": {
                    "MaxItemsPerBatchPath": "x",
                    "MaxInputBytesPerBatchPath": "x",
                },
                "End": True,
            },
        },
        "StartAt": "x",
    }
    assert Linter.validate(state_machine) == [
        'State Machine.States.x.ItemBatcher.MaxItemsPerBatchPath is "x" but should be '
        "a Reference Path",
        'State Machine.States.x.ItemBatcher.MaxInputBytesPerBatchPath is "x" but '
        "should be a Reference Path",
    ]


@pytest.mark.parametrize(
    "max_concurrency,errors",
    [
        ({"MaxConcurrency": 0}, []),
        (
            {"MaxConcurrency": -1},
            ["State Machine.States.x.MaxConcurrency is -1 but allowed floor is 0"],
        ),
        (
            {"MaxConcurrencyPath": "x"},
            [
                'State Machine.States.x.MaxConcurrencyPath is "x" but should be a '
                "Reference Path"
            ],
        ),
    ],
)
def test_max_concurrency(max_concurrency, errors):
    state_machine = {
        "States": {
            "x": {
                "Type": "Map",
                "ItemsPath": "$$.x",
                "Iterator": {"StartAt": "y", "States": {"y": {"Type": "Fail"}}},
                "End": True,
                **max_concurrency,
            },
        },
        "StartAt": "x",
    }
    assert Linter.validate(state_machine) == errors


@pytest.mark.parametrize(
    "tolerated_failure,errors",
    [
        (
            {"ToleratedFailureCount": -1},
            [
                "State Machine.States.x.ToleratedFailureCount is -1 but allowed floor "
                "is 0"
            ],
        ),
        (
            {"ToleratedFailureCount": "x"},
            [
                'State Machine.States.x.ToleratedFailureCount is "x" but should be an '
                "Integer"
            ],
        ),
        (
            {"ToleratedFailurePercentage": -1},
            [
                "State Machine.States.x.ToleratedFailurePercentage is -1 but allowed "
                "floor is 0",
            ],
        ),
        ({"ToleratedFailurePercentage": 100}, []),
        (
            {"ToleratedFailurePercentage": 101},
            [
                "State Machine.States.x.ToleratedFailurePercentage is 101 but allowed "
                "ceiling is 100",
            ],
        ),
        (
            {"ToleratedFailurePercentage": "x"},
            [
                'State Machine.States.x.ToleratedFailurePercentage is "x" but should '
                "be an Integer",
            ],
        ),
        (
            {"ToleratedFailureCount": 0, "ToleratedFailureCountPath": "$.x"},
            [
                'State Machine.States.x may have only one of ["ToleratedFailureCount", '
                '"ToleratedFailureCountPath"]',
            ],
        ),
        (
            {"ToleratedFailurePercentage": 0, "ToleratedFailurePercentagePath": "$.x"},
            [
                "State Machine.States.x may have only one of "
                '["ToleratedFailurePercentage", "ToleratedFailurePercentagePath"]',
            ],
        ),
    ],
)
def test_tolerated_failure(tolerated_failure, errors):
    state_machine = {
        "States": {
            "x": {
                "Type": "Map",
                "ItemsPath": "$$.x",
                "Iterator": {"StartAt": "y", "States": {"y": {"Type": "Fail"}}},
                "End": True,
                **tolerated_failure,
            },
        },
        "StartAt": "x",
    }
    assert Linter.validate(state_machine) == errors


@pytest.mark.parametrize(
    "config",
    ["ItemReader", "ResultWriter"],
)
def test_ng_arguments(config):
    state_machine = {
        "States": {
            "x": {
                "Type": "Map",
                "ItemsPath": "$$.x",
                "Iterator": {"StartAt": "y", "States": {"y": {"Type": "Fail"}}},
                config: {"Resource": "arn:x", "Arguments": "{% $foo.bar %}"},
                "End": True,
            },
        },
        "StartAt": "x",
    }
    assert Linter.validate(state_machine) == [
        f'Field "Arguments" not allowed in State Machine.States.x.{config}'
    ]


@pytest.mark.parametrize(
    "items",
    ["states.input.detail.shipped", {"bad": 42}],
)
def test_ng_items(items):
    state_machine = {
        "States": {
            "x": {
                "Type": "Map",
                "QueryLanguage": "JSONata",
                "Items": items,
                "Iterator": {"StartAt": "y", "States": {"y": {"Type": "Fail"}}},
                "End": True,
            },
        },
        "StartAt": "x",
    }
    assert Linter.validate(state_machine) == [
        f"State Machine.States.x.Items is {json.dumps(items)} but should be a JSONata"
    ]
