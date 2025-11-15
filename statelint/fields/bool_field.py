from ..problem import ProblemPredicate, ProblemType
from .base import Field, NonNullMixin
from .field_value import FieldValue


class BoolField(NonNullMixin, Field):
    def validate(self, value: FieldValue) -> list[ProblemPredicate]:
        problems = super().validate(value)
        if problems:
            return problems
        return self.check_type(value, bool, ProblemType.BOOLEAN)
