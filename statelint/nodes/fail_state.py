from typing import List

from ..fields import CAUSE, ERROR, INPUT_PATH, OUTPUT_PATH, Field
from .mixins import EndMixin
from .state import State


class FailState(EndMixin, State):
    @property
    def optional_fields(self) -> List[Field]:
        return [*super().optional_fields, CAUSE, ERROR]

    @property
    def forbidden_fields(self) -> List[Field]:
        return [INPUT_PATH, OUTPUT_PATH, *super().forbidden_fields]
