from typing import Any, Optional

from ...fields import TYPE, StateType
from ..choice_state import ChoiceState
from ..fail_state import FailState
from ..map_state import MapState
from ..node import Node, StatePath
from ..parallel_state import ParallelState
from ..pass_state import PassState
from ..succeed_state import SucceedState
from ..task_state import TaskState
from ..unknown_state import UnknownState
from ..wait_state import WaitState
from . import NodeFactory


class StateFactory(NodeFactory):
    def get(self, state_path: StatePath, state: Any) -> Optional[Node]:
        if not isinstance(state, dict):
            return None
        state_type = state.get(TYPE.name)
        if state_type == StateType.SUCCEED.value:
            return SucceedState(state_path, state)
        if state_type == StateType.FAIL.value:
            return FailState(state_path, state)
        if state_type == StateType.PASS.value:
            return PassState(state_path, state)
        if state_type == StateType.WAIT.value:
            return WaitState(state_path, state)
        if state_type == StateType.TASK.value:
            return TaskState(state_path, state)
        if state_type == StateType.CHOICE.value:
            return ChoiceState(state_path, state)
        if state_type == StateType.PARALLEL.value:
            return ParallelState(self, state_path, state)
        if state_type == StateType.MAP.value:
            return MapState(self, state_path, state)

        return UnknownState(state_path, state)
