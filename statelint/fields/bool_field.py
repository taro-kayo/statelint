from typing import Any

from ..problem import ProblemPredicate, ProblemType
from .base import Field, NonNullMixin


class BoolField(NonNullMixin, Field):
    def validate(self, value: Any) -> list[ProblemPredicate]:
        problems = super().validate(value)
        if problems:
            return problems
        return self.check_type(value, bool, ProblemType.BOOLEAN)
