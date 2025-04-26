from .mixins import EndMixin, OutputMixin
from .state import State


class SucceedState(EndMixin, OutputMixin, State):
    pass
