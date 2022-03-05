from enum import Enum


class ProblemType(str, Enum):
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
