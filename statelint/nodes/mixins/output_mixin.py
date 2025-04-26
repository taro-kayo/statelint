from typing import List

from ...fields import OUTPUT, Field
from ..node import Node


class OutputMixin(Node):
    @property
    def optional_fields(self) -> List[Field]:
        return [*super().optional_fields, OUTPUT]
