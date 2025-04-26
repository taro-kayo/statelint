from typing import Any

from ..problem import ProblemPredicate
from .base import Field


class AnyField(Field):
    def validate(self, value: Any) -> list[ProblemPredicate]:
        return []
