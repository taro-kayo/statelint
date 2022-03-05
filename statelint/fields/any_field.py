from typing import Any, List

from ..problem import ProblemPredicate
from .base import Field


class AnyField(Field):
    def validate(self, value: Any) -> List[ProblemPredicate]:
        return []
