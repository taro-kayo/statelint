from typing import Any

import pytest

from statelint.config import Config
from statelint.fields.common import QueryLanguage
from statelint.fields.field_value import FieldValue
from statelint.fields.pattern_field import JsonPathField, RefPathField


def as_field_value(value: Any) -> FieldValue:
    return FieldValue(
        raw_value=value,
        variables={},
        query_language=QueryLanguage.JSONPath,
        config=Config(),
    )


@pytest.mark.parametrize(
    "text,is_ok",
    [
        # should allow default paths
        ("$", True),
        # should reject obvious botches
        ("x", False),
        (".x", False),
        ("x.y.z", False),
        ("$.~.bar", False),
        # should allow reference paths
        ("$.foo.bar", True),
        ("$..x", True),
        ("$.foo.bar.baz.biff..blecch", True),
        ("$.café_au_lait", True),
        ("$['foo']['bar']", True),
        ("$['foo']['bar']['baz']['biff']..blecch", True),
        ("$['café_au_lait']", True),
        ("$..author", True),
        ("$..book[2]", True),
        ("$['豆柴']", True),
        # should distinguish between non-paths, paths, and reference paths
        ("$.store.book[*].author", False),
        ("$..author", True),
        ("$.store.*", False),
        ("$..book[2]", True),
        ("$..book[0,1]", False),
        ("$..book[:2]", False),
        ("$..book[1:2]", False),
        ("$..book[-2:]", False),
        ("$..book[2:]", False),
        ("$..*", False),
    ],
)
def test_ref_field(text, is_ok):
    field = RefPathField("test")
    assert (not field.validate(as_field_value(text))) == is_ok


@pytest.mark.parametrize(
    "text,is_ok",
    [
        # should allow default paths
        ("$", True),
        # should do simple paths
        ("$.foo.bar", True),
        ("$..x", True),
        ("$.foo.bar.baz.biff..blecch", True),
        ("$.café_au_lait", True),
        ("$['foo']", True),
        ("$[3]", True),
        # should reject obvious botches
        ("x", False),
        (".x", False),
        ("x.y.z", False),
        ("$.~.bar", False),
        # should accept paths with bracket notation
        ("$['foo']['bar']", True),
        ("$['foo']['bar']['baz']['biff']..blecch", True),
        ("$['café_au_lait']", True),
        # should accept some Jayway JsonPath examples
        ("$.store.book[*].author", True),
        ("$..author", True),
        ("$.store.*", True),
        ("$..book[2]", True),
        ("$..book[0,1]", True),
        ("$..book[:2]", True),
        ("$..book[1:2]", True),
        ("$..book[-2:]", True),
        ("$..book[2:]", True),
        ("$..*", True),
        # should distinguish between non-paths, paths, and reference paths
        ("$.store.book[*].author", True),
        ("$..author", True),
        ("$.store.*", True),
        ("$..book[2]", True),
        ("$..book[0,1]", True),
        ("$..book[:2]", True),
        ("$..book[1:2]", True),
        ("$..book[-2:]", True),
        ("$..book[2:]", True),
        ("$..*", True),
    ],
)
def test_main(text, is_ok):
    field = JsonPathField("test")
    assert (not field.validate(as_field_value(text))) == is_ok


def test_message():
    field = JsonPathField("test")
    assert [p.predicate for p in field.validate(as_field_value("x"))] == [
        ' is "x" but should be a JSONPath'
    ]


def test_repr():
    assert repr(JsonPathField("x")) == "JsonPathField(x)"
