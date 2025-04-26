from ..fields import INPUT_PATH, OUTPUT_PATH, QUERY_LANGUAGE, TYPE, Field, QueryLanguage
from .node import Node


class State(Node):
    @property
    def required_fields(self) -> list[Field]:
        return [*super().required_fields, TYPE]

    @property
    def optional_fields(self) -> list[Field]:
        fields = [*super().optional_fields, QUERY_LANGUAGE]
        if self.query_language == QueryLanguage.JSONata:
            return fields
        return [*fields, INPUT_PATH, OUTPUT_PATH]
