import functools
from collections import OrderedDict
from typing import Any, NamedTuple, Optional, Union

from ..fields import COMMENT, QUERY_LANGUAGE, Field, ProblemPredicate, QueryLanguage
from ..problem import Problem

StatePathType = Union[str, int, Field]


class NameAndPath(NamedTuple):
    name: str
    path: "StatePath"


class StatePath:
    _root: str
    _paths: list[StatePathType]

    def __init__(self, root: str, *paths: StatePathType):
        self._root = root
        self._paths = list(paths)

    def __str__(self) -> str:
        return functools.reduce(
            lambda x, y: x + self._path_to_str(y), self._paths, self._root
        )

    @staticmethod
    def _path_to_str(path: StatePathType) -> str:
        if isinstance(path, int):
            return f"[{path}]"
        if isinstance(path, Field):
            path = path.name
        return f".{path}"

    @property
    def parent(self) -> "StatePath":
        return StatePath(self._root, *self._paths[:-1])

    def make_child(self, *paths: StatePathType) -> "StatePath":
        return StatePath(self._root, *self._paths, *paths)

    def make_problem(self, predicate: ProblemPredicate) -> Problem:
        return Problem(f"{self}{predicate}", predicate.type)


def _get_query_language(state: dict[str, Any]) -> Optional[QueryLanguage]:
    raw_query_language = state.get(QUERY_LANGUAGE.name)
    if raw_query_language:
        return QueryLanguage.of(raw_query_language)
    return None


class Node:
    state_path: StatePath
    _state: dict[str, Any]
    _query_language: QueryLanguage

    def __init__(
        self,
        state_path: StatePath,
        state: dict[str, Any],
        current_query_language: QueryLanguage,
    ) -> None:
        self.state_path = state_path
        self._state = state
        self._query_language = _get_query_language(state) or current_query_language

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.state_path}, {self._state})"

    @property
    def required_fields(self) -> list[Field]:
        return []

    @property
    def optional_fields(self) -> list[Field]:
        return [COMMENT]

    @property
    def query_language(self) -> QueryLanguage:
        return self._query_language

    @property
    def forbidden_fields(self) -> list[Field]:
        # If we just want to validate extra fields, it's enough to put
        # allowed fields to required_fields/optional_fields.
        # Because we want to make our output error messages to be as same to
        # original statelint's as possible, we need this property.
        return []

    def get_reachable_states(self) -> list[NameAndPath]:
        return []

    def get_children(self) -> list[NameAndPath]:
        return []

    def validate(self) -> list[Problem]:
        allowed_fields = OrderedDict(
            (f2.name, f2)
            for f1 in (self.required_fields + self.optional_fields)
            for f2 in f1.get_fields()
        )
        return [
            *self._validate_fields(allowed_fields),
            *self._validate_forbidden_fields(),
            *self._validate_not_allowed_fields(allowed_fields),
            *self._validate_optional_fields(allowed_fields),
            *self._validate_required_fields(),
        ]

    def _validate_fields(self, fields: dict[str, Field]) -> list[Problem]:
        return [
            self.state_path.make_child(field).make_problem(problem)
            for field, value in self._state.items()
            if field in fields
            for problem in fields[field].validate(value)
        ]

    def _validate_forbidden_fields(self) -> list[Problem]:
        return [
            Problem(f'{self.state_path} has forbidden field "{field}"')
            for field in self.forbidden_fields
            if field.name in self._state
        ]

    def _validate_not_allowed_fields(
        self, allowed_fields: dict[str, Field]
    ) -> list[Problem]:
        forbidden_fields = set(f.name for f in self.forbidden_fields)
        return [
            Problem(f'Field "{field}" not allowed in {self.state_path}')
            for field in self._state
            if field not in allowed_fields and field not in forbidden_fields
        ]

    def _validate_optional_fields(
        self, allowed_fields: dict[str, Field]
    ) -> list[Problem]:
        all_fields = set(self._state)
        return [
            self.state_path.make_problem(problem)
            for field in allowed_fields.values()
            for problem in field.validate_as_optional(all_fields)
        ]

    def _validate_required_fields(self) -> list[Problem]:
        all_fields = set(self._state)
        return [
            self.state_path.make_problem(problem)
            for field in self.required_fields
            for problem in field.validate_as_required(all_fields)
        ]
