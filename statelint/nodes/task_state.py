from typing import List

from ..fields import (
    HEARTBEAT_SECONDS,
    HEARTBEAT_SECONDS_PATH,
    RESOURCE,
    TIMEOUT_SECONDS,
    TIMEOUT_SECONDS_PATH,
    Field,
    OneOfField,
)
from .mixins import (
    CatchMixin,
    NextXorEndMixin,
    ParametersMixin,
    ResultPathMixin,
    ResultSelectorMixin,
    RetryMixin,
    TimeoutSecondsMixin,
)
from .state import State


class TaskState(
    NextXorEndMixin,
    ResultPathMixin,
    ParametersMixin,
    ResultSelectorMixin,
    TimeoutSecondsMixin,
    CatchMixin,
    RetryMixin,
    State,
):
    @property
    def optional_fields(self) -> List[Field]:
        return [
            *super().optional_fields,
            RESOURCE,
            OneOfField(TIMEOUT_SECONDS, TIMEOUT_SECONDS_PATH),
            OneOfField(HEARTBEAT_SECONDS, HEARTBEAT_SECONDS_PATH),
        ]
