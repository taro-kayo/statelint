from typing import List

from ..fields import INPUT_PATH, OUTPUT_PATH, TYPE, Field
from .node import Node


class State(Node):
    @property
    def required_fields(self) -> List[Field]:
        return [*super().required_fields, TYPE]

    @property
    def optional_fields(self) -> List[Field]:
        return [*super().optional_fields, INPUT_PATH, OUTPUT_PATH]
