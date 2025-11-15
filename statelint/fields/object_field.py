from ..problem import ProblemPredicate, ProblemType
from .base import Field, NonNullMixin
from .field_value import FieldValue


class ObjectField(NonNullMixin, Field):
    def validate(self, value: FieldValue) -> list[ProblemPredicate]:
        return self.check_type(value, dict, ProblemType.OBJECT)
