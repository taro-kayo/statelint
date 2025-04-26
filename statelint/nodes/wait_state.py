from ..fields import SECONDS, SECONDS_PATH, TIMESTAMP, TIMESTAMP_PATH, Field, OneOfField
from .mixins import AssignMixin, NextXorEndMixin, OutputMixin
from .state import State


class WaitState(NextXorEndMixin, OutputMixin, AssignMixin, State):
    @property
    def required_fields(self) -> list[Field]:
        return [
            *super().required_fields,
            OneOfField(SECONDS, SECONDS_PATH, TIMESTAMP, TIMESTAMP_PATH),
        ]

    @property
    def optional_fields(self) -> list[Field]:
        return [*super().optional_fields]
