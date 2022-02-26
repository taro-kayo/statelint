from .mixins import NextXorEndMixin, ParametersMixin, ResultMixin, ResultPathMixin
from .state import State


class PassState(ResultPathMixin, ResultMixin, ParametersMixin, NextXorEndMixin, State):
    pass
