from abc import ABC
from typing import Any, Union

from ..problem import ProblemPredicate, ProblemType
from .common import to_json


class Field(ABC):
    name: str

    def __init__(self, name: str) -> None:
        self.name = name

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.name})"

    def validate(self, value: Any) -> list[ProblemPredicate]:
        return []

    @staticmethod
    def check_type(
        value: Any, _type: Union[type, tuple[type, ...]], problem_type: ProblemType
    ) -> list[ProblemPredicate]:
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
    def validate(self, value: Any) -> list[ProblemPredicate]:
        problems = super().validate(value)
        if problems:
            return problems
        if value is None:
            return [ProblemPredicate(" should be non-null")]
        return []
