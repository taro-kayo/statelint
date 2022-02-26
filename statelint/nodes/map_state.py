from typing import Any, Dict, List

from ..fields import ITEMS_PATH, ITERATOR, MAX_CONCURRENCY, Field
from ..problem import Problem
from .container_state import ContainerState
from .factory import NodeFactory
from .mixins import (
    CatchMixin,
    NextXorEndMixin,
    ParametersMixin,
    ResultPathMixin,
    ResultSelectorMixin,
    RetryMixin,
    TimeoutSecondsMixin,
)
from .node import NameAndPath, StatePath
from .state import State


class MapState(
    NextXorEndMixin,
    ResultPathMixin,
    ParametersMixin,
    ResultSelectorMixin,
    TimeoutSecondsMixin,
    CatchMixin,
    RetryMixin,
    State,
):
    def __init__(
        self, node_factory: NodeFactory, state_path: StatePath, state: Dict[str, Any]
    ) -> None:
        super().__init__(state_path, state)
        self._node_factory = node_factory
        iterator = state.get(ITERATOR.name)
        self._iterator = (
            ContainerState(
                self._node_factory, self.state_path.make_child(ITERATOR), iterator
            )
            if isinstance(iterator, dict)
            else None
        )

    @property
    def required_fields(self) -> List[Field]:
        return [*super().required_fields, ITERATOR]

    @property
    def optional_fields(self) -> List[Field]:
        return [*super().optional_fields, ITEMS_PATH, MAX_CONCURRENCY]

    def get_children(self) -> List[NameAndPath]:
        if not self._iterator:
            return []
        return list(self._iterator.get_children())

    def validate(self) -> List[Problem]:
        problems = super().validate()
        if self._iterator:
            return problems + self._iterator.validate()
        return problems
