from typing import Any

from ...fields import ASSIGN, CATCH, ERROR_EQUALS, NEXT, Field
from ...problem import Problem
from ..node import NameAndPath, Node
from .assign_mixin import AssignMixin
from .output_mixin import OutputMixin
from .result_path_mixin import ResultPathMixin


class Catcher(ResultPathMixin, OutputMixin, AssignMixin, Node):
    @property
    def required_fields(self) -> list[Field]:
        return [*super().required_fields, ERROR_EQUALS, NEXT]

    @property
    def optional_fields(self) -> list[Field]:
        return [*super().optional_fields, ASSIGN]


class CatchMixin(Node):
    @property
    def optional_fields(self) -> list[Field]:
        return [*super().optional_fields, CATCH]

    def validate(self) -> list[Problem]:
        problems = super().validate()
        catchers = self._state.get(CATCH.name)
        if not isinstance(catchers, list):
            return problems
        return (
            problems
            + [
                p
                for idx, element in enumerate(catchers)
                if isinstance(element, dict)
                for p in Catcher(
                    self.state_path.make_child(CATCH, idx), element, self.query_language
                ).validate()
            ]
            + self._validate_error_equals(catchers)
        )

    def _validate_error_equals(self, catchers: list[Any]) -> list[Problem]:
        problems = []
        for idx, catcher in enumerate(catchers):
            if not isinstance(catcher, dict):
                continue
            error_equals = catcher.get(ERROR_EQUALS.name)
            if not isinstance(error_equals, list):
                continue

            if "States.ALL" in error_equals:
                if idx != len(catchers) - 1 or len(error_equals) != 1:
                    state_path = self.state_path.make_child(CATCH, idx)
                    problems.append(
                        Problem(
                            f"{state_path}: States.ALL can only "
                            "appear in the last element, and by itself."
                        ),
                    )

        return problems

    def get_reachable_states(self) -> list[NameAndPath]:
        states = super().get_reachable_states()
        state = self._state
        if not isinstance(state.get(CATCH.name), list):
            return states

        return states + [
            NameAndPath(element[NEXT.name], self.state_path.make_child(NEXT))
            for element in state[CATCH.name]
            if isinstance(element, dict) and isinstance(element.get(NEXT.name), str)
        ]
