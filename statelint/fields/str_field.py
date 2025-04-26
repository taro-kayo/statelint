from typing import Any

from ..problem import ProblemPredicate, ProblemType
from .base import Field, NonNullMixin


class NullableStrField(Field):
    @property
    def problem_type(self) -> ProblemType:
        return ProblemType.STRING

    def validate(self, value: Any) -> list[ProblemPredicate]:
        if value is None:
            return []
        return self.check_type(value, str, self.problem_type)


class StrField(NonNullMixin, NullableStrField):
    pass


class EnumStrField(StrField):
    def __init__(self, name: str, choices: list[str]):
        super().__init__(name)
        self.choices = choices

    def validate(self, value: Any) -> list[ProblemPredicate]:
        problems = super().validate(value)
        str_val = "" if value is None else str(value)
        if str_val not in self.choices:
            choices = ", ".join(f'"{c}"' for c in self.choices)
            problems += [
                ProblemPredicate(
                    f' is "{str_val}", not one of the allowed values [{choices}]'
                )
            ]

        return problems
