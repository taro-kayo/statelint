from typing import List

from ..fields import SECONDS, SECONDS_PATH, TIMESTAMP, TIMESTAMP_PATH, Field, OneOfField
from .mixins import NextXorEndMixin, OutputMixin
from .state import State


class WaitState(NextXorEndMixin, OutputMixin, State):
    @property
    def required_fields(self) -> List[Field]:
        return [
            *super().required_fields,
            OneOfField(SECONDS, SECONDS_PATH, TIMESTAMP, TIMESTAMP_PATH),
        ]

    @property
    def optional_fields(self) -> List[Field]:
        return [*super().optional_fields]
