from ...fields import ASSIGN, Field, QueryLanguage
from ..node import Node


class AssignMixin(Node):
    @property
    def optional_fields(self) -> list[Field]:
        fields = super().optional_fields
        if self.query_language == QueryLanguage.JSONata:
            return [*fields, ASSIGN]
        return fields
