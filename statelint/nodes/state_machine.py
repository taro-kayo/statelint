from typing import Any

from ..config import Config
from ..fields import QUERY_LANGUAGE, VERSION, Field
from .container_state import ContainerState
from .factory import NodeFactory
from .mixins import TimeoutSecondsMixin
from .node import StatePath


class StateMachine(TimeoutSecondsMixin, ContainerState):
    def __init__(
        self, node_factory: NodeFactory, state: dict[str, Any], config: Config
    ) -> None:
        super().__init__(node_factory, StatePath("State Machine"), state, None, config)

    @property
    def optional_fields(self) -> list[Field]:
        return [*super().optional_fields, VERSION, QUERY_LANGUAGE]
