import itertools
from typing import Any

from ...fields import (
    BATCH_INPUT,
    ITEM_SELECTOR,
    PARAMETERS,
    RESULT_SELECTOR,
    Field,
    OneOfField,
    QueryLanguage,
)
from ...problem import Problem
from ...utils.re_helper import is_intrinsic_invocation, is_path
from ..node import Node, StatePath


class ParametersMixin(Node):
    @property
    def optional_fields(self) -> list[Field]:
        fields = super().optional_fields
        if self.query_language == QueryLanguage.JSONata:
            return fields
        return [*fields, PARAMETERS]

    def validate(self) -> list[Problem]:
        problems = [*super().validate()]
        if not isinstance(self._state.get(PARAMETERS.name), dict):
            return problems

        return problems + _validate_payload(
            PARAMETERS, self.state_path, self._state[PARAMETERS.name]
        )


class ItemSelectorMixin(Node):
    @property
    def optional_fields(self) -> list[Field]:
        return [*super().optional_fields, OneOfField(PARAMETERS, ITEM_SELECTOR)]

    def validate(self) -> list[Problem]:
        problems = [*super().validate()]
        for field in (PARAMETERS, ITEM_SELECTOR):
            if isinstance(self._state.get(field.name), dict):
                problems += _validate_payload(
                    field, self.state_path, self._state[field.name]
                )

        return problems


class ResultSelectorMixin(Node):
    @property
    def optional_fields(self) -> list[Field]:
        fields = super().optional_fields
        if self.query_language == QueryLanguage.JSONata:
            return fields
        return [*fields, RESULT_SELECTOR]

    def validate(self) -> list[Problem]:
        problems = [*super().validate()]
        if not isinstance(self._state.get(RESULT_SELECTOR.name), dict):
            return problems

        return problems + _validate_payload(
            RESULT_SELECTOR, self.state_path, self._state[RESULT_SELECTOR.name]
        )


class BatchInputMixin(Node):
    @property
    def optional_fields(self) -> list[Field]:
        return [*super().optional_fields, BATCH_INPUT]

    def validate(self) -> list[Problem]:
        problems = super().validate()
        batch_input = self._state.get(BATCH_INPUT.name)
        if not isinstance(batch_input, dict):
            return problems

        return problems + _validate_payload(BATCH_INPUT, self.state_path, batch_input)


def _validate_payload(
    field: Field, current_path: StatePath, param: Any
) -> list[Problem]:
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
