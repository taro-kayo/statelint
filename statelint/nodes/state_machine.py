from typing import Any, Dict, List

from ..fields import VERSION, Field
from .container_state import ContainerState
from .factory import NodeFactory
from .mixins import TimeoutSecondsMixin
from .node import StatePath


class StateMachine(TimeoutSecondsMixin, ContainerState):
    def __init__(self, node_factory: NodeFactory, state: Dict[str, Any]) -> None:
        super().__init__(node_factory, StatePath("State Machine"), state)

    @property
    def optional_fields(self) -> List[Field]:
        return [*super().optional_fields, VERSION]
