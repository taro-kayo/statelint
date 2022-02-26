from typing import Any, List

from .base import Field
from ..problem import ProblemPredicate


class AnyField(Field):
    def validate(self, value: Any) -> List[ProblemPredicate]:
        return []
