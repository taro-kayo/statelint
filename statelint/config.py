from typing import Optional

from .problem import ProblemType


class Config:
    ignored_problem_types: set[ProblemType]
    is_yaml: bool

    @property
    def input_type(self) -> str:
        return "YAML" if self.is_yaml else "JSON"

    def __init__(
        self,
        ignored_problem_types: Optional[set[ProblemType]] = None,
        yaml: bool = False,
    ):
        self.ignored_problem_types = ignored_problem_types or set()
        self.is_yaml = yaml
