from ...fields import RESULT_PATH, Field, QueryLanguage
from ..node import Node


class ResultPathMixin(Node):
    @property
    def optional_fields(self) -> list[Field]:
        fields = super().optional_fields
        if self.query_language == QueryLanguage.JSONata:
            return fields
        return [*fields, RESULT_PATH]
