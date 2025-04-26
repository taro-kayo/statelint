from ...fields import OUTPUT, Field, QueryLanguage
from ..node import Node


class OutputMixin(Node):
    @property
    def optional_fields(self) -> list[Field]:
        fields = super().optional_fields
        if self.query_language == QueryLanguage.JSONata:
            return [*fields, OUTPUT]
        return fields
