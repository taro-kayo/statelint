from dateutil import parser

from ..problem import ProblemPredicate
from .base import Field, NonNullMixin
from .common import to_json
from .field_value import FieldValue


class TimestampField(NonNullMixin, Field):
    def validate(self, field_value: FieldValue) -> list[ProblemPredicate]:
        problems = super().validate(field_value)
        if problems:
            return problems
        value = field_value.value
        if isinstance(value, str) and _is_rfc3339_format(value):
            return []

        return [
            ProblemPredicate(f" is {to_json(value)} but should be an RFC3339 timestamp")
        ]


def _is_rfc3339_format(value: str) -> bool:
    # ISO8601/RFC3339
    try:
        parser.isoparse(value)
    except ValueError:
        return False
    return True
