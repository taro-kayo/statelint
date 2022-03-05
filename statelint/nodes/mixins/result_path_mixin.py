from typing import List

from ...fields import RESULT_PATH, Field
from ..node import Node


class ResultPathMixin(Node):
    @property
    def optional_fields(self) -> List[Field]:
        return [*super().optional_fields, RESULT_PATH]
