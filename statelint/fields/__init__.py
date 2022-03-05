from ..problem import ProblemPredicate
from .any_field import AnyField as _AnyField
from .base import Field
from .bool_field import BoolField as _BoolField
from .common import StateType
from .container import OneOfField
from .list_field import ListField as _ListField
from .list_field import NonEmptyListField as _NonEmptyListField
from .num_field import FloatField as _FloatField
from .num_field import IntegerField as _IntegerField
from .num_field import NumericField as _NumericField
from .object_field import ObjectField as _ObjectField
from .pattern_field import JsonPathField as _JsonPathField
from .pattern_field import NullableRefPathField as _NullableRefPathField
from .pattern_field import RefPathField as _RefPathField
from .pattern_field import UriField as _UriField
from .str_field import EnumStrField as _EnumStrField
from .str_field import NullableStrField as _NullableStrField
from .str_field import StrField as _StrField
from .timestamp_field import TimestampField as _TimestampField

VERSION = _StrField("Version")
COMMENT = _StrField("Comment")

SECONDS = _IntegerField("Seconds", 0, inclusive=False)
SECONDS_PATH = _RefPathField("SecondsPath")
TIMESTAMP = _TimestampField("Timestamp")
TIMESTAMP_PATH = _RefPathField("TimestampPath")

CAUSE = _StrField("Cause")
ERROR = _StrField("Error")

RESULT = _AnyField("Result")
RESULT_SELECTOR = _AnyField("ResultSelector")
RESULT_PATH = _NullableRefPathField("ResultPath")
PARAMETERS = _AnyField("Parameters")

NEXT = _StrField("Next")
END = _BoolField("End")

STATES = _ObjectField("States")
START_AT = _StrField("StartAt")

TIMEOUT_SECONDS = _IntegerField("TimeoutSeconds", 0, 99999999)
HEARTBEAT_SECONDS = _IntegerField("HeartbeatSeconds", 0, 99999999)
TIMEOUT_SECONDS_PATH = _RefPathField("TimeoutSecondsPath")
HEARTBEAT_SECONDS_PATH = _RefPathField("HeartbeatSecondsPath")

TYPE = _EnumStrField("Type", [t.value for t in StateType])

INPUT_PATH = _NullableStrField("InputPath")
OUTPUT_PATH = _NullableStrField("OutputPath")

RESOURCE = _UriField("Resource")

CATCH = _ListField("Catch", _ObjectField)
RETRY = _ListField("Retry", _ObjectField)
ERROR_EQUALS = _NonEmptyListField("ErrorEquals", _StrField)
INTERVAL_SECONDS = _IntegerField("IntervalSeconds", 0)
MAX_ATTEMPTS = _IntegerField("MaxAttempts", -1, 99999999)
BACKOFF_RATE = _FloatField("BackoffRate", 1, inclusive=False)


CHOICES = _NonEmptyListField("Choices", _ObjectField)
DEFAULT = _StrField("Default")

AND = _NonEmptyListField("And", _ObjectField)
OR = _NonEmptyListField("Or", _ObjectField)
NOT = _ObjectField("Not")

VARIABLE = _AnyField("Variable")

STRING_EQUALS = _StrField("StringEquals")
STRING_LESS_THAN = _StrField("StringLessThan")
STRING_GREATER_THAN = _StrField("StringGreaterThan")
STRING_LESS_THAN_EQUALS = _StrField("StringLessThanEquals")
STRING_GREATER_THAN_EQUALS = _StrField("StringGreaterThanEquals")
NUMERIC_EQUALS = _NumericField("NumericEquals")
NUMERIC_LESS_THAN = _NumericField("NumericLessThan")
NUMERIC_GREATER_THAN = _NumericField("NumericGreaterThan")
NUMERIC_LESS_THAN_EQUALS = _NumericField("NumericLessThanEquals")
NUMERIC_GREATER_THAN_EQUALS = _NumericField("NumericGreaterThanEquals")
BOOLEAN_EQUALS = _BoolField("BooleanEquals")
TIMESTAMP_EQUALS = _TimestampField("TimestampEquals")
TIMESTAMP_LESS_THAN = _TimestampField("TimestampLessThan")
TIMESTAMP_GREATER_THAN = _TimestampField("TimestampGreaterThan")
TIMESTAMP_LESS_THAN_EQUALS = _TimestampField("TimestampLessThanEquals")
TIMESTAMP_GREATER_THAN_EQUALS = _TimestampField("TimestampGreaterThanEquals")
STRING_EQUALS_PATH = _RefPathField("StringEqualsPath")
STRING_LESS_THAN_PATH = _RefPathField("StringLessThanPath")
STRING_GREATER_THAN_PATH = _RefPathField("StringGreaterThanPath")
STRING_LESS_THAN_EQUALS_PATH = _RefPathField("StringLessThanEqualsPath")
STRING_GREATER_THAN_EQUALS_PATH = _RefPathField("StringGreaterThanEqualsPath")
NUMERIC_EQUALS_PATH = _RefPathField("NumericEqualsPath")
NUMERIC_LESS_THAN_PATH = _RefPathField("NumericLessThanPath")
NUMERIC_GREATER_THAN_PATH = _RefPathField("NumericGreaterThanPath")
NUMERIC_LESS_THAN_EQUALS_PATH = _RefPathField("NumericLessThanEqualsPath")
NUMERIC_GREATER_THAN_EQUALS_PATH = _RefPathField("NumericGreaterThanEqualsPath")
BOOLEAN_EQUALS_PATH = _RefPathField("BooleanEqualsPath")
TIMESTAMP_EQUALS_PATH = _RefPathField("TimestampEqualsPath")
TIMESTAMP_LESS_THAN_PATH = _RefPathField("TimestampLessThanPath")
TIMESTAMP_GREATER_THAN_PATH = _RefPathField("TimestampGreaterThanPath")
TIMESTAMP_LESS_THAN_EQUALS_PATH = _RefPathField("TimestampLessThanEqualsPath")
TIMESTAMP_GREATER_THAN_EQUALS_PATH = _RefPathField("TimestampGreaterThanEqualsPath")
IS_NULL = _BoolField("IsNull")
IS_PRESENT = _BoolField("IsPresent")
IS_NUMERIC = _BoolField("IsNumeric")
IS_STRING = _BoolField("IsString")
IS_BOOLEAN = _BoolField("IsBoolean")
IS_TIMESTAMP = _BoolField("IsTimestamp")
STRING_MATCHES = _StrField("StringMatches")

BRANCHES = _ListField("Branches", _ObjectField)

ITERATOR = _ObjectField("Iterator")
ITEMS_PATH = _JsonPathField("ItemsPath")
MAX_CONCURRENCY = _NumericField("MaxConcurrency")
