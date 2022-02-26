from typing import Any, List

from ..problem import ProblemPredicate, ProblemType
from .base import Field, NonNullMixin


class ObjectField(NonNullMixin, Field):
    def validate(self, value: Any) -> List[ProblemPredicate]:
        return self.check_type(value, dict, ProblemType.OBJECT)
