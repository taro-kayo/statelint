from typing import Any, List

from ..problem import ProblemPredicate, ProblemType
from .base import Field, NonNullMixin


class BoolField(NonNullMixin, Field):
    def validate(self, value: Any) -> List[ProblemPredicate]:
        problems = super().validate(value)
        if problems:
            return problems
        return self.check_type(value, bool, ProblemType.BOOLEAN)
