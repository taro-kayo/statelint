from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any

from ..config import Config
from .common import QueryLanguage


@dataclass
class FieldValue:
    value: Any
    query_language: QueryLanguage
    variables: dict[str, Any]
    config: Config

    def of(self, value: Any) -> FieldValue:
        return replace(self, value=value)
