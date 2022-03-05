from typing import Any, List

from ..problem import ProblemPredicate, ProblemType
from .base import Field, NonNullMixin


class NullableStrField(Field):
    @property
    def problem_type(self) -> ProblemType:
        return ProblemType.STRING

    def validate(self, value: Any) -> List[ProblemPredicate]:
        if value is None:
            return []
        return self.check_type(value, str, self.problem_type)


class StrField(NonNullMixin, NullableStrField):
    pass


class EnumStrField(StrField):
    def __init__(self, name: str, choices: List[str]):
        super().__init__(name)
        self.choices = choices

    def validate(self, value: Any) -> List[ProblemPredicate]:
        problems = super().validate(value)
        if problems:
            return problems
        if value not in self.choices:
            choices = ", ".join(f'"{c}"' for c in self.choices)
            return [
                ProblemPredicate(
                    f' is "{value}", not one of the allowed values [{choices}]'
                )
            ]

        return []
