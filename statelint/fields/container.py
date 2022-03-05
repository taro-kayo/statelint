from collections import OrderedDict
from typing import List, Set

from ..problem import ProblemPredicate
from .any_field import AnyField
from .base import Field
from .common import to_json


class OneOfField(AnyField):
    def __init__(self, *fields: Field) -> None:
        # use OrderedDict as set to preserve order
        self._fields = OrderedDict((f.name, f) for f in fields)
        fields_str = ", ".join(to_json(f) for f in self._fields)
        super().__init__(f"[{fields_str}]")

    def get_fields(self) -> List["Field"]:
        return [*super().get_fields(), *self._fields.values()]

    def validate_as_required(self, names: Set[str]) -> List[ProblemPredicate]:
        intersection_count = len(names & set(self._fields))
        if intersection_count == 0:
            return [ProblemPredicate(f" does not have required field from {self.name}")]
        return []

    def validate_as_optional(self, names: Set[str]) -> List[ProblemPredicate]:
        intersection_count = len(names & set(self._fields))
        if intersection_count > 1:
            return [ProblemPredicate(f" may have only one of {self.name}")]
        return []
