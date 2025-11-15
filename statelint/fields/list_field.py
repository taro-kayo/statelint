from typing import Type

from ..problem import ProblemPredicate, ProblemType
from .base import Field, NonNullMixin
from .field_value import FieldValue


class ListField(NonNullMixin, Field):
    def __init__(self, name: str, element_field_type: Type[Field]) -> None:
        super().__init__(name)
        self._element_field_type = element_field_type(name)

    def validate(self, field_value: FieldValue) -> list[ProblemPredicate]:
        problems = super().validate(field_value)
        if problems:
            return problems
        problems = self.check_type(field_value, list, ProblemType.ARRAY)
        if problems:
            return problems
        value = field_value.value
        return [
            ProblemPredicate(f"[{idx}]{problem}")
            for idx, element in enumerate(value)
            for problem in self._element_field_type.validate(field_value.of(element))
        ]


class NonEmptyListField(ListField):
    def validate(self, field_value: FieldValue) -> list[ProblemPredicate]:
        problems = super().validate(field_value)
        if problems:
            return problems
        value = field_value.value
        if len(value) == 0:
            return [ProblemPredicate(" is empty, non-empty required")]
        return []
