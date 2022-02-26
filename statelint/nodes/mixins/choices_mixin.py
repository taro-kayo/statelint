from abc import ABC
from collections import OrderedDict
from typing import Any, List

from ...fields import (
    AND,
    BOOLEAN_EQUALS,
    BOOLEAN_EQUALS_PATH,
    CHOICES,
    DEFAULT,
    IS_BOOLEAN,
    IS_NULL,
    IS_NUMERIC,
    IS_PRESENT,
    IS_STRING,
    IS_TIMESTAMP,
    NEXT,
    NOT,
    NUMERIC_EQUALS,
    NUMERIC_EQUALS_PATH,
    NUMERIC_GREATER_THAN,
    NUMERIC_GREATER_THAN_EQUALS,
    NUMERIC_GREATER_THAN_EQUALS_PATH,
    NUMERIC_GREATER_THAN_PATH,
    NUMERIC_LESS_THAN,
    NUMERIC_LESS_THAN_EQUALS,
    NUMERIC_LESS_THAN_EQUALS_PATH,
    NUMERIC_LESS_THAN_PATH,
    OR,
    STRING_EQUALS,
    STRING_EQUALS_PATH,
    STRING_GREATER_THAN,
    STRING_GREATER_THAN_EQUALS,
    STRING_GREATER_THAN_EQUALS_PATH,
    STRING_GREATER_THAN_PATH,
    STRING_LESS_THAN,
    STRING_LESS_THAN_EQUALS,
    STRING_LESS_THAN_EQUALS_PATH,
    STRING_LESS_THAN_PATH,
    STRING_MATCHES,
    TIMESTAMP_EQUALS,
    TIMESTAMP_EQUALS_PATH,
    TIMESTAMP_GREATER_THAN,
    TIMESTAMP_GREATER_THAN_EQUALS,
    TIMESTAMP_GREATER_THAN_EQUALS_PATH,
    TIMESTAMP_GREATER_THAN_PATH,
    TIMESTAMP_LESS_THAN,
    TIMESTAMP_LESS_THAN_EQUALS,
    TIMESTAMP_LESS_THAN_EQUALS_PATH,
    TIMESTAMP_LESS_THAN_PATH,
    VARIABLE,
    Field,
    OneOfField,
)
from ...problem import Problem
from ..node import NameAndPath, Node

COMPARISONS = OneOfField(
    STRING_EQUALS,
    STRING_LESS_THAN,
    STRING_GREATER_THAN,
    STRING_LESS_THAN_EQUALS,
    STRING_GREATER_THAN_EQUALS,
    NUMERIC_EQUALS,
    NUMERIC_LESS_THAN,
    NUMERIC_GREATER_THAN,
    NUMERIC_LESS_THAN_EQUALS,
    NUMERIC_GREATER_THAN_EQUALS,
    BOOLEAN_EQUALS,
    TIMESTAMP_EQUALS,
    TIMESTAMP_LESS_THAN,
    TIMESTAMP_GREATER_THAN,
    TIMESTAMP_LESS_THAN_EQUALS,
    TIMESTAMP_GREATER_THAN_EQUALS,
    STRING_EQUALS_PATH,
    STRING_LESS_THAN_PATH,
    STRING_GREATER_THAN_PATH,
    STRING_LESS_THAN_EQUALS_PATH,
    STRING_GREATER_THAN_EQUALS_PATH,
    NUMERIC_EQUALS_PATH,
    NUMERIC_LESS_THAN_PATH,
    NUMERIC_GREATER_THAN_PATH,
    NUMERIC_LESS_THAN_EQUALS_PATH,
    NUMERIC_GREATER_THAN_EQUALS_PATH,
    BOOLEAN_EQUALS_PATH,
    TIMESTAMP_EQUALS_PATH,
    TIMESTAMP_LESS_THAN_PATH,
    TIMESTAMP_GREATER_THAN_PATH,
    TIMESTAMP_LESS_THAN_EQUALS_PATH,
    TIMESTAMP_GREATER_THAN_EQUALS_PATH,
    IS_NULL,
    IS_PRESENT,
    IS_NUMERIC,
    IS_STRING,
    IS_BOOLEAN,
    IS_TIMESTAMP,
    STRING_MATCHES,
)


class BaseChoiceRule(Node, ABC):
    @property
    def optional_fields(self) -> List[Field]:
        fields = super().optional_fields
        if VARIABLE.name in self._state:
            return [*fields, VARIABLE, COMPARISONS]
        return [*fields, AND, OR, NOT]

    @property
    def forbidden_fields(self) -> List[Field]:
        fields = [f for f in super().forbidden_fields]
        if VARIABLE.name in self._state:
            return [*fields, AND, OR, NOT]
        return fields

    def validate(self) -> List[Problem]:
        problems = list(super().validate())
        for field in (AND.name, OR.name):
            if isinstance(self._state.get(field), list):
                for idx, child in enumerate(self._state[field]):
                    problems.extend(self._validate_child(f"{field}[{idx}]", child))

        problems.extend(self._validate_child(NOT.name, self._state.get(NOT.name)))

        return problems

    def _validate_child(self, field_name: str, child: Any) -> List[Problem]:
        if isinstance(child, dict):
            return NestedChoiceRule(
                self.state_path.make_child(field_name), child
            ).validate()
        return []


class ChoiceRule(BaseChoiceRule):
    @property
    def required_fields(self) -> List[Field]:
        return [*super().required_fields, NEXT]


class NestedChoiceRule(BaseChoiceRule):
    @property
    def forbidden_fields(self) -> List[Field]:
        return [NEXT, *super().forbidden_fields]


class ChoicesMixin(Node):
    @property
    def required_fields(self) -> List[Field]:
        return [*super().required_fields, CHOICES]

    def validate(self) -> List[Problem]:
        problems = super().validate()
        if not isinstance(self._state.get(CHOICES.name), list):
            return problems
        return problems + [
            p
            for idx, element in enumerate(self._state[CHOICES.name])
            if isinstance(element, dict)
            for p in ChoiceRule(
                self.state_path.make_child(CHOICES.name, idx), element
            ).validate()
        ]

    def get_reachable_states(self) -> List[NameAndPath]:
        # use OrderedDict as set to preserve order
        reachable_states = OrderedDict({s: 0 for s in super().get_reachable_states()})
        if isinstance(self._state.get(DEFAULT.name), str):
            name = self._state[DEFAULT.name]
            reachable_states[NameAndPath(name, self.state_path.make_child(DEFAULT))] = 0
        if isinstance(self._state.get(CHOICES.name), list):
            for idx, choice in enumerate(self._state[CHOICES.name]):
                if isinstance(choice, dict) and isinstance(choice.get(NEXT.name), str):
                    state_path = self.state_path.make_child(CHOICES, idx, NEXT)
                    reachable_states[NameAndPath(choice[NEXT.name], state_path)] = 0
        return list(reachable_states)
