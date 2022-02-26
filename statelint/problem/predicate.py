from .problem_type import ProblemType


class ProblemPredicate:
    predicate: str
    type: ProblemType

    def __init__(
        self, predicate: str, _type: ProblemType = ProblemType.UNKNOWN
    ) -> None:
        self.predicate = predicate
        self.type = _type

    def __str__(self) -> str:
        return self.predicate
