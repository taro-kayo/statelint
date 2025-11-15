from abc import ABC

from ..problem import ProblemPredicate, ProblemType
from .common import to_json
from .field_value import FieldValue


class Field(ABC):
    name: str

    def __init__(self, name: str) -> None:
        self.name = name

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.name})"

    def validate(self, value: FieldValue) -> list[ProblemPredicate]:
        return []

    @staticmethod
    def check_type(
        field_value: FieldValue,
        _type: type | tuple[type, ...],
        problem_type: ProblemType,
    ) -> list[ProblemPredicate]:
        value = field_value.value
        if isinstance(value, _type):
            return []
        return [
            ProblemPredicate(
                f" is {to_json(value)} but should be {problem_type}", problem_type
            )
        ]

    def get_fields(self) -> list["Field"]:
        return [self]

    def validate_as_required(self, names: set[str]) -> list[ProblemPredicate]:
        if self.name in names:
            return []
        return [ProblemPredicate(f' does not have required field "{self.name}"')]

    def validate_as_optional(self, names: set[str]) -> list[ProblemPredicate]:
        return []


class NonNullMixin(Field):
    def validate(self, field_value: FieldValue) -> list[ProblemPredicate]:
        problems = super().validate(field_value)
        if problems:
            return problems
        value = field_value.value
        if value is None:
            return [ProblemPredicate(" should be non-null")]
        return []
