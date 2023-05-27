from enum import Enum


class ProblemType(str, Enum):
    def __str__(self) -> str:
        return self.value

    # type check
    FLOAT = "a Float"
    STRING = "a String"
    NUMERIC = "numeric"
    BOOLEAN = "a Boolean"
    OBJECT = "an Object"
    ARRAY = "an Array"
    INTEGER = "an Integer"
    # pattern check
    URI = "A URI"
    REFERENCE_PATH = "a Reference Path"
    JSON_PATH = "a JSONPath"

    UNKNOWN = "unknown"
