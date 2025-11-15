import pytest

from statelint.config import Config
from statelint.fields.common import QueryLanguage
from statelint.fields.field_value import FieldValue


@pytest.mark.parametrize(
    "query_language,expected",
    [(QueryLanguage.JSONPath, "{% $x %}"), (QueryLanguage.JSONata, 42)],
)
def test_value_with_query_language(query_language, expected):
    field_value = FieldValue(
        raw_value="{% $x %}",
        variables={"x": 42},
        query_language=query_language,
        config=Config(evaluate_jsonata=True),
    )
    assert field_value.value == expected
