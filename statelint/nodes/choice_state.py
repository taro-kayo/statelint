from ..fields import DEFAULT, END, NEXT, Field
from .mixins import AssignMixin, ChoicesMixin, OutputMixin
from .state import State


class ChoiceState(ChoicesMixin, OutputMixin, AssignMixin, State):
    @property
    def optional_fields(self) -> list[Field]:
        return [*super().optional_fields, DEFAULT]

    @property
    def forbidden_fields(self) -> list[Field]:
        return [NEXT, END, *super().forbidden_fields]
