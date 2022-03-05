import itertools
from typing import Any, List

from ...fields import PARAMETERS, RESULT_SELECTOR, Field
from ...problem import Problem
from ...utils.re_helper import is_intrinsic_invocation, is_path
from ..node import Node, StatePath


class ParametersMixin(Node):
    @property
    def optional_fields(self) -> List[Field]:
        return [*super().optional_fields, PARAMETERS]

    def validate(self) -> List[Problem]:
        problems = [*super().validate()]
        if not isinstance(self._state.get(PARAMETERS.name), dict):
            return problems

        return problems + _validate_payload(
            PARAMETERS, self.state_path, self._state[PARAMETERS.name]
        )


class ResultSelectorMixin(Node):
    @property
    def optional_fields(self) -> List[Field]:
        return [*super().optional_fields, RESULT_SELECTOR]

    def validate(self) -> List[Problem]:
        problems = [*super().validate()]
        if not isinstance(self._state.get(RESULT_SELECTOR.name), dict):
            return problems

        return problems + _validate_payload(
            RESULT_SELECTOR, self.state_path, self._state[RESULT_SELECTOR.name]
        )


def _validate_payload(
    field: Field, current_path: StatePath, param: Any
) -> List[Problem]:
    problems = []
    if isinstance(param, list):
        return list(
            itertools.chain.from_iterable(
                _validate_payload(field, current_path.make_child(i), p)
                for i, p in enumerate(param)
            )
        )
    if not isinstance(param, dict):
        return []

    for key, value in param.items():
        if not key.endswith(".$"):
            problems.extend(
                _validate_payload(field, current_path.make_child(key), value)
            )
            continue

        if isinstance(value, str) and _is_valid_parameter(value):
            continue
        problems.append(
            Problem(
                f'Field "{key}" of {field} at "{current_path}" is not '
                "a JSONPath or intrinsic function expression"
            )
        )
    return problems


def _is_valid_parameter(value: str) -> bool:
    return is_path(value, True) or is_intrinsic_invocation(value)
