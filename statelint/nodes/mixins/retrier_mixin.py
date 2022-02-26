from typing import List

from ...fields import (
    BACKOFF_RATE,
    ERROR_EQUALS,
    INTERVAL_SECONDS,
    MAX_ATTEMPTS,
    RETRY,
    Field,
)
from ...problem import Problem
from ..node import Node
from .result_path_mixin import ResultPathMixin


class Retrier(ResultPathMixin, Node):
    @property
    def required_fields(self) -> List[Field]:
        return [*super().required_fields, ERROR_EQUALS]

    @property
    def optional_fields(self) -> List[Field]:
        return [*super().optional_fields, INTERVAL_SECONDS, MAX_ATTEMPTS, BACKOFF_RATE]


class RetryMixin(Node):
    @property
    def optional_fields(self) -> List[Field]:
        return [*super().optional_fields, RETRY]

    def validate(self) -> List[Problem]:
        state = self._state
        problems = super().validate()
        if not isinstance(state.get(RETRY.name), list):
            return problems
        return problems + [
            p
            for idx, element in enumerate(state[RETRY.name])
            if isinstance(element, dict)
            for p in Retrier(self.state_path.make_child(RETRY, idx), element).validate()
        ]
