from collections import OrderedDict
from typing import Any, Dict, List, Optional, Set

from ..fields import END, NEXT, START_AT, STATES, TYPE, Field, StateType
from ..problem import Problem
from .factory import NodeFactory
from .node import NameAndPath, Node, StatePath


class ContainerState(Node):
    def __init__(
        self, node_factory: NodeFactory, state_path: StatePath, state: Dict[str, Any]
    ) -> None:
        super().__init__(state_path, state)
        self._node_factory = node_factory
        self._states = self._collect_states()

    def _collect_states(self) -> Dict[str, Node]:
        ret_dict = OrderedDict()
        states = self._state.get(STATES.name)
        if isinstance(states, dict):
            for state_name, state in states.items():
                validator = self._node_factory.get(
                    self.state_path.make_child(STATES, state_name), state
                )
                if validator:
                    ret_dict[state_name] = validator
        return ret_dict

    @property
    def required_fields(self) -> List[Field]:
        return [*super().required_fields, STATES, START_AT]

    def get_children(self) -> List[NameAndPath]:
        return [NameAndPath(n, s.state_path) for n, s in self._states.items()]

    def validate(self) -> List[Problem]:
        problems = super().validate()
        states = self._state.get(STATES.name)
        reachable_states = set()
        if isinstance(states, dict):
            all_states: Dict[str, StatePath] = {
                k: s.state_path for k, s in self._states.items()
            }
            for state in self._states.values():
                problems.extend(state.validate())
                _reachable_states = state.get_reachable_states()
                for s in (s for s in _reachable_states if s.name not in states):
                    problems.append(
                        Problem(
                            f'No state found named "{s.name}", referenced at {s.path}'
                        )
                    )
                reachable_states.update(_reachable_states)
                for child in state.get_children():
                    if child.name in all_states:
                        problems.append(
                            Problem(
                                f'State "{child.name}", defined at '
                                f"{child.path.parent}, is also defined at "
                                f"{all_states[child.name].parent}"
                            )
                        )
                    else:
                        all_states[child.name] = state.state_path

        problems += self._validate_transition(
            self._state.get(START_AT.name), states, reachable_states
        )
        return problems

    def _validate_transition(
        self, start_at: Optional[str], states: Any, reachable_states: Set[NameAndPath]
    ) -> List[Problem]:
        if not isinstance(states, dict):
            return []
        if start_at not in states:
            problems = [
                Problem(f"No transition found to state {self.state_path.make_child(s)}")
                for s in states
            ]
            if start_at:
                problems = [
                    Problem(
                        f"{START_AT.name} value {start_at} not found in "
                        f"{STATES.name} field at {self.state_path}"
                    )
                ] + problems
            return problems
        state_names = list(states)

        problems = []
        terminal_found = False
        for state_name in (start_at, *(s.name for s in reachable_states)):
            while True:
                if state_name not in state_names:
                    break  # checked already.
                state_names.remove(state_name)
                state = states[state_name]
                if not isinstance(state, dict):
                    break
                if _is_terminal(state):
                    terminal_found = True
                if NEXT.name not in state:
                    break
                next_state_name = state[NEXT.name]
                if next_state_name not in states:
                    assert state_name, "state_names contains None"
                    state_path = self.state_path.make_child(STATES, state_name, NEXT)
                    problems.append(
                        Problem(
                            f'No state found named "{next_state_name}", '
                            f"referenced at {state_path}"
                        )
                    )
                    break
                state_name = next_state_name

        if state_names:
            problems.extend(
                Problem(f"No transition found to state {self.state_path.make_child(s)}")
                for s in state_names
            )

        if not terminal_found:
            problems.append(
                Problem(
                    "No terminal state found in machine at "
                    f"{self.state_path.make_child(STATES)}"
                )
            )

        return problems


def _is_terminal(state: Dict[str, Any]) -> bool:
    if state.get(TYPE.name) in (StateType.SUCCEED.value, StateType.FAIL.value):
        return True
    if state.get(END.name):
        return True

    return False
