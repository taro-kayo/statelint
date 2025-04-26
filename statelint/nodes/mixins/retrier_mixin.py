from ...fields import (
    BACKOFF_RATE,
    ERROR_EQUALS,
    INTERVAL_SECONDS,
    JITTER_STRATEGY,
    MAX_ATTEMPTS,
    MAX_DELAY_SECONDS,
    RETRY,
    Field,
)
from ...problem import Problem
from ..node import Node
from .result_path_mixin import ResultPathMixin


class Retrier(ResultPathMixin, Node):
    @property
    def required_fields(self) -> list[Field]:
        return [*super().required_fields, ERROR_EQUALS]

    @property
    def optional_fields(self) -> list[Field]:
        return [
            *super().optional_fields,
            INTERVAL_SECONDS,
            MAX_ATTEMPTS,
            BACKOFF_RATE,
            MAX_DELAY_SECONDS,
            JITTER_STRATEGY,
        ]


class RetryMixin(Node):
    @property
    def optional_fields(self) -> list[Field]:
        return [*super().optional_fields, RETRY]

    def validate(self) -> list[Problem]:
        state = self._state
        problems = super().validate()
        if not isinstance(state.get(RETRY.name), list):
            return problems
        return problems + [
            p
            for idx, element in enumerate(state[RETRY.name])
            if isinstance(element, dict)
            for p in Retrier(
                self.state_path.make_child(RETRY, idx), element, self.query_language
            ).validate()
        ]
