from ..fields import (
    CREDENTIALS,
    HEARTBEAT_SECONDS,
    HEARTBEAT_SECONDS_PATH,
    RESOURCE,
    TIMEOUT_SECONDS,
    TIMEOUT_SECONDS_PATH,
    Field,
    OneOfField,
    QueryLanguage,
)
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
from .state import State


class TaskState(
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
    @property
    def optional_fields(self) -> list[Field]:
        fields = [
            *super().optional_fields,
            RESOURCE,
            CREDENTIALS,
        ]
        if self.query_language == QueryLanguage.JSONata:
            return [*fields, TIMEOUT_SECONDS, HEARTBEAT_SECONDS]
        return [
            *fields,
            OneOfField(TIMEOUT_SECONDS, TIMEOUT_SECONDS_PATH),
            OneOfField(HEARTBEAT_SECONDS, HEARTBEAT_SECONDS_PATH),
        ]
