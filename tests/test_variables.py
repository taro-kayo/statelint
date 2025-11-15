from statelint.config import Config
from statelint.nodes.factory.factory import StateFactory
from statelint.nodes.map_state import MapState
from statelint.nodes.state_machine import StateMachine


def test_no_variable():
    sm = StateMachine(
        StateFactory(), {"States": {"x": {"Type": "Succeed"}}, "StartAt": "x"}, Config()
    )
    assert sm.validate() == []
    assert sm.variable_scopes == [{}]


def test_child_variable():
    variables = {"v1": 42, "v2": "str", "v3": {"v4": None}}
    sm = StateMachine(
        StateFactory(),
        {
            "QueryLanguage": "JSONata",
            "States": {
                "x": {"Type": "Pass", "Assign": variables, "Next": "y"},
                "y": {"Type": "Succeed"},
            },
            "StartAt": "x",
        },
        Config(),
    )
    assert sm.validate() == []
    assert sm.variable_scopes == [variables]


def test_nest():
    variables_in_parent = {"v1": 42}
    variables_in_child = {"v2": True}
    sm = StateMachine(
        StateFactory(),
        {
            "QueryLanguage": "JSONata",
            "States": {
                "x": {"Type": "Pass", "Assign": variables_in_parent, "Next": "y"},
                "y": {
                    "Type": "Map",
                    "Iterator": {
                        "StartAt": "y1",
                        "States": {
                            "y1": {
                                "Type": "Pass",
                                "Assign": variables_in_child,
                                "Next": "y2",
                            },
                            "y2": {"Type": "Fail"},
                        },
                    },
                    "End": True,
                },
            },
            "StartAt": "x",
        },
        Config(),
    )
    assert sm.validate() == []
    assert sm.variable_scopes == [variables_in_parent]
    map_state = sm._states["y"]
    assert isinstance(map_state, MapState)
    assert map_state.variable_scopes == [variables_in_parent]
    assert map_state._iterator
    assert map_state._iterator.variable_scopes == [
        variables_in_parent,
        variables_in_child,
    ]
