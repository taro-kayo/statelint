from ..problem import ProblemPredicate
from .base import Field
from .field_value import FieldValue


class AnyField(Field):
    def validate(self, value: FieldValue) -> list[ProblemPredicate]:
        return []
