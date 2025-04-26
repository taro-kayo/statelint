from ...fields import ARGUMENTS, Field, QueryLanguage
from ..node import Node


class ArgumentsMixin(Node):
    @property
    def optional_fields(self) -> list[Field]:
        fields = super().optional_fields
        if self.query_language == QueryLanguage.JSONata:
            return [*fields, ARGUMENTS]
        return fields
