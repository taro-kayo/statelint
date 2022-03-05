import json
import os.path
from typing import Any, Callable, Dict, List, Union

from .config import Config
from .nodes.factory.factory import StateFactory
from .nodes.state_machine import StateMachine


class ParseError(ValueError):
    def __init__(self, root_cause: Exception) -> None:
        super().__init__()
        self.root_cause = root_cause


class Linter:
    @staticmethod
    def validate(
        json_str_or_dict_or_file_path: Union[str, Dict[str, Any]], config: Config = None
    ) -> List[str]:
        if not config:
            config = Config()

        parse_text = _parse_yaml if config.is_yaml else _parse_json
        try:
            parsed = _parse_to_dict(json_str_or_dict_or_file_path, parse_text)
        except ParseError as err:
            return [f"Problem reading/parsing {config.input_type}: {err.root_cause}"]

        if not isinstance(parsed, dict):
            return []

        problems = [
            p
            for p in StateMachine(StateFactory(), parsed).validate()
            if p.type not in config.ignored_problem_types
        ]

        return [str(p) for p in problems]


def _parse_to_dict(
    json_str_or_dict_or_file_path: Union[str, Any],
    parse_text: Callable[[str], Dict[str, Any]],
) -> Any:
    if isinstance(json_str_or_dict_or_file_path, dict):
        return json_str_or_dict_or_file_path

    if os.path.isfile(json_str_or_dict_or_file_path):
        with open(json_str_or_dict_or_file_path) as file:
            text = file.read()
    else:
        text = json_str_or_dict_or_file_path

    return parse_text(text)


def _parse_json(text: str) -> Any:
    try:
        return json.loads(text)
    except json.JSONDecodeError as err:
        raise ParseError(err)


def _parse_yaml(text: str) -> Any:
    import yaml

    return yaml.safe_load(text)
