from typing import Any, List, Type

from ..problem import ProblemPredicate, ProblemType
from .base import Field, NonNullMixin


class ListField(NonNullMixin, Field):
    def __init__(self, name: str, element_field_type: Type[Field]) -> None:
        super().__init__(name)
        self._element_field_type = element_field_type(name)

    def validate(self, value: Any) -> List[ProblemPredicate]:
        problems = super().validate(value)
        if problems:
            return problems
        problems = self.check_type(value, list, ProblemType.ARRAY)
        if problems:
            return problems
        return [
            ProblemPredicate(f"[{idx}]{problem}")
            for idx, element in enumerate(value)
            for problem in self._element_field_type.validate(element)
        ]


class NonEmptyListField(ListField):
    def validate(self, value: Any) -> List[ProblemPredicate]:
        problems = super().validate(value)
        if problems:
            return problems
        if len(value) == 0:
            return [ProblemPredicate(" is empty, non-empty required")]
        return []
