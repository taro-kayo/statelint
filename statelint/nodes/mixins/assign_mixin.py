from typing import List

from ...fields import ASSIGN, Field
from ..node import Node


class AssignMixin(Node):
    @property
    def optional_fields(self) -> List[Field]:
        return [*super().optional_fields, ASSIGN]
