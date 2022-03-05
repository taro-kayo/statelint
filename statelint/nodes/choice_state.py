from typing import List

from ..fields import DEFAULT, END, NEXT, Field
from .mixins import ChoicesMixin
from .state import State


class ChoiceState(ChoicesMixin, State):
    @property
    def optional_fields(self) -> List[Field]:
        return [*super().optional_fields, DEFAULT]

    @property
    def forbidden_fields(self) -> List[Field]:
        return [NEXT, END, *super().forbidden_fields]
