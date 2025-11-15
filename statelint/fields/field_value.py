from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any

from ..config import Config
from ..utils.jsonata_helper import evaluate_jsonata, extract_jsonata_exp
from .common import QueryLanguage


@dataclass
class FieldValue:
    raw_value: Any
    query_language: QueryLanguage
    variables: dict[str, Any]
    config: Config

    def of(self, value: Any) -> FieldValue:
        return replace(self, raw_value=value)

    @property
    def value(self) -> Any:
        value = self.raw_value
        if not self.config.evaluate_jsonata:
            return value

        if self.query_language != QueryLanguage.JSONata:
            return value

        if not isinstance(value, str):
            return value

        exp = extract_jsonata_exp(value)
        if not exp:
            return value

        # TODO: Ideally, when correctly evaluated, we should return None.
        # However, since we are too lazy to handle that properly, we currently
        # just return the original value in all cases.
        return evaluate_jsonata(exp, self.variables) or value
