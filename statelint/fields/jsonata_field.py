import re
from typing import Callable

from ..problem import ProblemPredicate, ProblemType
from .base import Field
from .common import to_json
from .field_value import FieldValue
from .str_field import StrField


class JSONataField(Field):

    def __init__(self, name: str, acceptable_field: Callable[[str], Field]) -> None:
        super().__init__(name)
        self._field = acceptable_field(name)
        self._str_field = StrField(name)

    def validate(self, field_value: FieldValue) -> list[ProblemPredicate]:
        if not self._field.validate(field_value):
            return []
        value = field_value.value
        if not self._str_field.validate(field_value):
            if re.match(r"\{%.+%\}", value):
                return []

        problem_type = ProblemType.JSONata
        return [
            ProblemPredicate(
                f" is {to_json(value)} but should be {problem_type}", problem_type
            )
        ]
