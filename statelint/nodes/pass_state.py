from .mixins import (
    AssignMixin,
    NextXorEndMixin,
    OutputMixin,
    ParametersMixin,
    ResultMixin,
    ResultPathMixin,
)
from .state import State


class PassState(
    ResultPathMixin,
    ResultMixin,
    ParametersMixin,
    NextXorEndMixin,
    OutputMixin,
    AssignMixin,
    State,
):
    pass
