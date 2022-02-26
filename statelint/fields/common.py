import json
from enum import Enum
from typing import Any


class Comparison(str, Enum):
    STRING_EQUALS = "StringEquals"
    STRING_LESS_THAN = "StringLessThan"
    STRING_GREATER_THAN = "StringGreaterThan"
    STRING_LESS_THAN_EQUALS = "StringLessThanEquals"
    STRING_GREATER_THAN_EQUALS = "StringGreaterThanEquals"
    NUMERIC_EQUALS = "NumericEquals"
    NUMERIC_LESS_THAN = "NumericLessThan"
    NUMERIC_GREATER_THAN = "NumericGreaterThan"
    NUMERIC_LESS_THAN_EQUALS = "NumericLessThanEquals"
    NUMERIC_GREATER_THAN_EQUALS = "NumericGreaterThanEquals"
    BOOLEAN_EQUALS = "BooleanEquals"
    TIMESTAMP_EQUALS = "TimestampEquals"
    TIMESTAMP_LESS_THAN = "TimestampLessThan"
    TIMESTAMP_GREATER_THAN = "TimestampGreaterThan"
    TIMESTAMP_LESS_THAN_EQUALS = "TimestampLessThanEquals"
    TIMESTAMP_GREATER_THAN_EQUALS = "TimestampGreaterThanEquals"
    STRING_EQUALS_PATH = "StringEqualsPath"
    STRING_LESS_THAN_PATH = "StringLessThanPath"
    STRING_GREATER_THAN_PATH = "StringGreaterThanPath"
    STRING_LESS_THAN_EQUALS_PATH = "StringLessThanEqualsPath"
    STRING_GREATER_THAN_EQUALS_PATH = "StringGreaterThanEqualsPath"
    NUMERIC_EQUALS_PATH = "NumericEqualsPath"
    NUMERIC_LESS_THAN_PATH = "NumericLessThanPath"
    NUMERIC_GREATER_THAN_PATH = "NumericGreaterThanPath"
    NUMERIC_LESS_THAN_EQUALS_PATH = "NumericLessThanEqualsPath"
    NUMERIC_GREATER_THAN_EQUALS_PATH = "NumericGreaterThanEqualsPath"
    BOOLEAN_EQUALS_PATH = "BooleanEqualsPath"
    TIMESTAMP_EQUALS_PATH = "TimestampEqualsPath"
    TIMESTAMP_LESS_THAN_PATH = "TimestampLessThanPath"
    TIMESTAMP_GREATER_THAN_PATH = "TimestampGreaterThanPath"
    TIMESTAMP_LESS_THAN_EQUALS_PATH = "TimestampLessThanEqualsPath"
    TIMESTAMP_GREATER_THAN_EQUALS_PATH = "TimestampGreaterThanEqualsPath"
    IS_NULL = "IsNull"
    IS_PRESENT = "IsPresent"
    IS_NUMERIC = "IsNumeric"
    IS_STRING = "IsString"
    IS_BOOLEAN = "IsBoolean"
    IS_TIMESTAMP = "IsTimestamp"
    STRING_MATCHES = "StringMatches"


class StateType(str, Enum):
    PASS = "Pass"
    SUCCEED = "Succeed"
    FAIL = "Fail"
    TASK = "Task"
    CHOICE = "Choice"
    WAIT = "Wait"
    PARALLEL = "Parallel"
    MAP = "Map"


def to_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False)
