from ..problem import ProblemPredicate, ProblemType
from .base import Field, NonNullMixin
from .field_value import FieldValue


class NullableStrField(Field):
    @property
    def problem_type(self) -> ProblemType:
        return ProblemType.STRING

    def validate(self, field_value: FieldValue) -> list[ProblemPredicate]:
        value = field_value.value
        if value is None:
            return []
        return self.check_type(field_value, str, self.problem_type)


class StrField(NonNullMixin, NullableStrField):
    pass


class EnumStrField(StrField):
    def __init__(self, name: str, choices: list[str]):
        super().__init__(name)
        self.choices = choices

    def validate(self, field_value: FieldValue) -> list[ProblemPredicate]:
        problems = super().validate(field_value)
        value = field_value.value
        str_val = "" if value is None else str(value)
        if str_val not in self.choices:
            choices = ", ".join(f'"{c}"' for c in self.choices)
            problems += [
                ProblemPredicate(
                    f' is "{str_val}", not one of the allowed values [{choices}]'
                )
            ]

        return problems
