from .problem_type import ProblemType


class Problem:
    description: str
    type: ProblemType

    def __init__(self, description: str, _type: ProblemType = ProblemType.UNKNOWN):
        self.description = description
        self.type = _type

    def __str__(self) -> str:
        return self.description
