import re
from typing import Any

from ..problem import ProblemPredicate, ProblemType
from .base import Field
from .common import to_json
from .object_field import ObjectField
from .str_field import StrField


class JSONataField(Field):

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self._object_field = ObjectField(name)
        self._str_field = StrField(name)

    def validate(self, value: Any) -> list[ProblemPredicate]:
        if not self._object_field.validate(value):
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
