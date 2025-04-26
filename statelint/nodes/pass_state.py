from .mixins import (
    NextXorEndMixin,
    OutputMixin,
    ParametersMixin,
    ResultMixin,
    ResultPathMixin,
)
from .state import State


class PassState(
    ResultPathMixin, ResultMixin, ParametersMixin, NextXorEndMixin, OutputMixin, State
):
    pass
