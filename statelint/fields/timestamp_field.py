from typing import Any, List

from dateutil import parser

from ..problem import ProblemPredicate
from .base import Field, NonNullMixin
from .common import to_json


class TimestampField(NonNullMixin, Field):
    def validate(self, value: Any) -> List[ProblemPredicate]:
        problems = super().validate(value)
        if problems:
            return problems
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
