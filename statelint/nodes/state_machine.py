from typing import Any

from ..fields import QUERY_LANGUAGE, VERSION, Field, QueryLanguage
from .container_state import ContainerState
from .factory import NodeFactory
from .mixins import TimeoutSecondsMixin
from .node import StatePath


class StateMachine(TimeoutSecondsMixin, ContainerState):
    def __init__(self, node_factory: NodeFactory, state: dict[str, Any]) -> None:
        super().__init__(
            node_factory, StatePath("State Machine"), state, QueryLanguage.JSONPath
        )

    @property
    def optional_fields(self) -> list[Field]:
        return [*super().optional_fields, VERSION, QUERY_LANGUAGE]
