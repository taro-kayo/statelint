import operator
from abc import ABC, abstractmethod
from typing import Any, List, Optional, Tuple, Union

from ..problem import ProblemPredicate, ProblemType
from .base import Field, NonNullMixin


class BaseNumericField(NonNullMixin, Field, ABC):
    _floor: Optional[int]
    _ceiling: Optional[int]

    def __init__(
        self, name: str, floor: int = None, ceiling: int = None, inclusive: bool = True
    ) -> None:
        super().__init__(name)
        self._floor = floor
        self._ceiling = ceiling
        self._inclusive = inclusive

    @property
    @abstractmethod
    def problem_type(self) -> ProblemType:
        pass  # pragma: no cover

    @property
    @abstractmethod
    def raw_type(self) -> Union[type, Tuple[type, ...]]:
        pass  # pragma: no cover

    def validate(self, value: Any) -> List[ProblemPredicate]:
        problems = super().validate(value)
        if problems:
            return problems
        problems = self.check_type(value, self.raw_type, self.problem_type)
        if problems:
            return problems

        ope = operator.le if self._inclusive else operator.lt
        if isinstance(self._floor, int) and ope(value, self._floor):
            return [ProblemPredicate(f" is {value} but allowed floor is {self._floor}")]
        ope = operator.ge if self._inclusive else operator.gt
        if isinstance(self._ceiling, int) and ope(value, self._ceiling):
            return [
                ProblemPredicate(f" is {value} but allowed ceiling is {self._ceiling}")
            ]
        return []


class IntegerField(BaseNumericField):
    @property
    def problem_type(self) -> ProblemType:
        return ProblemType.INTEGER

    @property
    def raw_type(self) -> Union[type, Tuple[type, ...]]:
        return int


class FloatField(BaseNumericField):
    @property
    def problem_type(self) -> ProblemType:
        return ProblemType.FLOAT

    @property
    def raw_type(self) -> Union[type, Tuple[type, ...]]:
        return float


class NumericField(BaseNumericField):
    @property
    def problem_type(self) -> ProblemType:
        return ProblemType.NUMERIC

    @property
    def raw_type(self) -> Union[type, Tuple[type, ...]]:
        return int, float
