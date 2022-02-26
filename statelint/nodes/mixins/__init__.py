from typing import List

from ...fields import END, NEXT, RESULT, TIMEOUT_SECONDS, Field
from ..node import Node
from .catcher_mixin import CatchMixin
from .choices_mixin import ChoicesMixin
from .payload_template_mixin import ParametersMixin, ResultSelectorMixin
from .result_path_mixin import ResultPathMixin
from .retrier_mixin import RetryMixin


class ResultMixin(Node):
    @property
    def optional_fields(self) -> List[Field]:
        return [*super().optional_fields, RESULT]


class TimeoutSecondsMixin(Node):
    @property
    def optional_fields(self) -> List[Field]:
        return [*super().optional_fields, TIMEOUT_SECONDS]


class NextXorEndMixin(Node):
    @property
    def required_fields(self) -> List[Field]:
        required_field = END if END.name in self._state else NEXT
        return [*super().required_fields, required_field]

    @property
    def optional_fields(self) -> List[Field]:
        return [*super().optional_fields, NEXT, END]

    @property
    def forbidden_fields(self) -> List[Field]:
        if END.name in self._state:
            return [NEXT]
        return [END]


class NextMixin(Node):
    @property
    def optional_fields(self) -> List[Field]:
        return [*super().optional_fields, NEXT]


class EndMixin(Node):
    @property
    def forbidden_fields(self) -> List[Field]:
        return [NEXT]
