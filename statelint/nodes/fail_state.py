from ..fields import (
    CAUSE,
    CAUSE_PATH,
    ERROR,
    ERROR_PATH,
    INPUT_PATH,
    OUTPUT_PATH,
    Field,
    OneOfField,
    QueryLanguage,
)
from .mixins import EndMixin
from .state import State


class FailState(EndMixin, State):
    @property
    def optional_fields(self) -> list[Field]:
        fields = super().optional_fields
        if self.query_language == QueryLanguage.JSONata:
            return [*fields, CAUSE, ERROR]
        return [
            *fields,
            OneOfField(CAUSE, CAUSE_PATH),
            OneOfField(ERROR, ERROR_PATH),
        ]

    @property
    def forbidden_fields(self) -> list[Field]:
        return [INPUT_PATH, OUTPUT_PATH, *super().forbidden_fields]
