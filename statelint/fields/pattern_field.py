import re
from abc import ABC, abstractmethod
from typing import Any, Callable, List

from ..problem import ProblemPredicate, ProblemType
from ..utils.re_helper import is_path, is_reference_path
from .base import NonNullMixin
from .str_field import NullableStrField


class PatternField(NullableStrField, ABC):
    def __init__(self, name: str, is_match: Callable[[str], bool]) -> None:
        super().__init__(name)
        self._is_match = is_match

    @property
    @abstractmethod
    def problem_type(self) -> ProblemType:
        pass  # pragma: no cover

    def validate(self, value: Any) -> List[ProblemPredicate]:
        problems = super().validate(value)
        if problems:
            return problems
        if isinstance(value, str) and not self._is_match(value):
            return [
                ProblemPredicate(
                    f' is "{value}" but should be {self.problem_type}',
                    self.problem_type,
                )
            ]
        return []


class UriField(NonNullMixin, PatternField):
    def __init__(self, name: str) -> None:
        super().__init__(name, lambda x: bool(re.compile(r"^[a-z]+:").match(x)))

    @property
    def problem_type(self) -> ProblemType:
        return ProblemType.URI


class NullableRefPathField(PatternField):
    def __init__(self, name: str) -> None:
        super().__init__(name, is_reference_path)

    @property
    def problem_type(self) -> ProblemType:
        return ProblemType.REFERENCE_PATH


class RefPathField(NonNullMixin, NullableRefPathField):
    pass


class JsonPathField(NonNullMixin, PatternField):
    def __init__(self, name: str) -> None:
        super().__init__(name, lambda x: is_path(x, True))

    @property
    def problem_type(self) -> ProblemType:
        return ProblemType.JSON_PATH
