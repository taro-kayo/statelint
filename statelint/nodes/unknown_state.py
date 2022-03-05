from .mixins import NextMixin
from .state import State


class UnknownState(NextMixin, State):
    pass
