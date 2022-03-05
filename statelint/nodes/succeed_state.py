from .mixins import EndMixin
from .state import State


class SucceedState(EndMixin, State):
    pass
