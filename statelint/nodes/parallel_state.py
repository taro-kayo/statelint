import itertools
from typing import Any

from ..fields import BRANCHES, Field, QueryLanguage
from ..problem import Problem
from .container_state import ContainerState
from .factory import NodeFactory
from .mixins import (
    ArgumentsMixin,
    AssignMixin,
    CatchMixin,
    NextXorEndMixin,
    OutputMixin,
    ParametersMixin,
    ResultPathMixin,
    ResultSelectorMixin,
    RetryMixin,
    TimeoutSecondsMixin,
)
from .node import NameAndPath, StatePath
from .state import State


class ParallelState(
    NextXorEndMixin,
    ResultPathMixin,
    ParametersMixin,
    ResultSelectorMixin,
    TimeoutSecondsMixin,
    CatchMixin,
    RetryMixin,
    OutputMixin,
    AssignMixin,
    ArgumentsMixin,
    State,
):
    def __init__(
        self,
        node_factory: NodeFactory,
        state_path: StatePath,
        state: dict[str, Any],
        current_query_language: QueryLanguage,
    ) -> None:
        super().__init__(state_path, state, current_query_language)
        self._node_factory = node_factory
        self._branches = self._get_branches(state)

    def _get_branches(self, state: dict[str, Any]) -> list[ContainerState]:
        branches = state.get(BRANCHES.name)
        if not isinstance(branches, list):
            return []
        return [
            ContainerState(
                self._node_factory,
                self.state_path.make_child(BRANCHES, idx),
                element,
                self.query_language,
            )
            for idx, element in enumerate(state[BRANCHES.name])
            if isinstance(element, dict)
        ]

    @property
    def required_fields(self) -> list[Field]:
        return [*super().required_fields, BRANCHES]

    def get_children(self) -> list[NameAndPath]:
        return list(
            itertools.chain.from_iterable(b.get_children() for b in self._branches)
        )

    def validate(self) -> list[Problem]:
        return super().validate() + [
            p for branch in self._branches for p in branch.validate()
        ]
