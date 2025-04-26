import re
from typing import Any, Callable

from ..problem import ProblemPredicate, ProblemType
from .base import Field
from .common import to_json
from .str_field import StrField


class JSONataField(Field):

    def __init__(self, name: str, acceptable_field: Callable[[str], Field]) -> None:
        super().__init__(name)
        self._field = acceptable_field(name)
        self._str_field = StrField(name)

    def validate(self, value: Any) -> list[ProblemPredicate]:
        if not self._field.validate(value):
            return []
        if not self._str_field.validate(value):
            if re.match(r"\{%.+%\}", value):
                return []

        problem_type = ProblemType.JSONata
        return [
            ProblemPredicate(
                f" is {to_json(value)} but should be {problem_type}", problem_type
            )
        ]
