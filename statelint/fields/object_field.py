from typing import Any

from ..problem import ProblemPredicate, ProblemType
from .base import Field, NonNullMixin


class ObjectField(NonNullMixin, Field):
    def validate(self, value: Any) -> list[ProblemPredicate]:
        return self.check_type(value, dict, ProblemType.OBJECT)
