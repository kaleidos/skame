import pytest

from skame.exceptions import SchemaError
from skame.schemas import types as t


def test_schema_int():
    assert t.Int().validate(3) == 3
    assert t.Int().validate(1) == 1
    assert t.Int().validate(0) == 0

    with pytest.raises(SchemaError):
        t.Int().validate("3")

    with pytest.raises(SchemaError):
        t.Int().validate(None)

    with pytest.raises(SchemaError):
        t.Int().validate(False)

    with pytest.raises(SchemaError):
        t.Int().validate(True)

    with pytest.raises(SchemaError):
        t.Int().validate({})

    with pytest.raises(SchemaError):
        t.Int().validate([])


def test_schema_float():
    assert t.Float().validate(3.2) == 3.2
    assert t.Float().validate(3.0) == 3.0

    with pytest.raises(SchemaError):
        t.Float().validate(3)

    with pytest.raises(SchemaError):
        t.Float().validate("3.2")

    with pytest.raises(SchemaError):
        t.Float().validate(None)

    with pytest.raises(SchemaError):
        t.Float().validate(False)

    with pytest.raises(SchemaError):
        t.Float().validate(True)

    with pytest.raises(SchemaError):
        t.Float().validate({})

    with pytest.raises(SchemaError):
        t.Float().validate([])


def test_schema_complex():
    assert t.Complex().validate(3 + 2j) == 3 + 2j
    assert t.Complex().validate(2j) == 2j

    with pytest.raises(SchemaError):
        t.Complex().validate(3)

    with pytest.raises(SchemaError):
        t.Complex().validate(3.3)

    with pytest.raises(SchemaError):
        t.Complex().validate("3.2")

    with pytest.raises(SchemaError):
        t.Complex().validate(None)

    with pytest.raises(SchemaError):
        t.Complex().validate(False)

    with pytest.raises(SchemaError):
        t.Complex().validate(True)

    with pytest.raises(SchemaError):
        t.Complex().validate({})

    with pytest.raises(SchemaError):
        t.Complex().validate([])


def test_schema_string():
    assert t.String().validate("test") == "test"
    assert t.String().validate("") == ""

    with pytest.raises(SchemaError):
        t.String().validate(3)

    with pytest.raises(SchemaError):
        t.String().validate(3.3)

    with pytest.raises(SchemaError):
        t.String().validate(None)

    with pytest.raises(SchemaError):
        t.String().validate(False)

    with pytest.raises(SchemaError):
        t.String().validate(True)

    with pytest.raises(SchemaError):
        t.String().validate({})

    with pytest.raises(SchemaError):
        t.String().validate([])


def test_schema_list():
    assert t.List().validate(["test", "test2"]) == ["test", "test2"]
    assert t.List().validate([]) == []

    with pytest.raises(SchemaError):
        t.List().validate(3)

    with pytest.raises(SchemaError):
        t.List().validate("3.2")

    with pytest.raises(SchemaError):
        t.List().validate(3.3)

    with pytest.raises(SchemaError):
        t.List().validate(None)

    with pytest.raises(SchemaError):
        t.List().validate(False)

    with pytest.raises(SchemaError):
        t.List().validate(True)

    with pytest.raises(SchemaError):
        t.List().validate({})


def test_schema_dict():
    assert t.Dict().validate({"test": "test", "test2": "test2"}) == {"test": "test", "test2": "test2"}
    assert t.Dict().validate({}) == {}

    with pytest.raises(SchemaError):
        t.Dict().validate(3)

    with pytest.raises(SchemaError):
        t.Dict().validate("3.2")

    with pytest.raises(SchemaError):
        t.Dict().validate(3.3)

    with pytest.raises(SchemaError):
        t.Dict().validate(None)

    with pytest.raises(SchemaError):
        t.Dict().validate(False)

    with pytest.raises(SchemaError):
        t.Dict().validate(True)

    with pytest.raises(SchemaError):
        t.Dict().validate([])


def test_schema_bool():
    assert t.Bool().validate(True) is True
    assert t.Bool().validate(False) is False

    with pytest.raises(SchemaError):
        t.Bool().validate(0)

    with pytest.raises(SchemaError):
        t.Bool().validate(1)

    with pytest.raises(SchemaError):
        t.Bool().validate(3)

    with pytest.raises(SchemaError):
        t.Bool().validate("3.2")

    with pytest.raises(SchemaError):
        t.Bool().validate(3.3)

    with pytest.raises(SchemaError):
        t.Bool().validate(None)

    with pytest.raises(SchemaError):
        t.Bool().validate([])

    with pytest.raises(SchemaError):
        t.Bool().validate({})


def test_schema_date():
    from datetime import date, datetime

    assert t.Date().validate(date(2015, 4, 8)) == date(2015, 4, 8)

    # NOTE: a python datetime is also a date (is type compatible)
    assert t.Date().validate(datetime(2015, 4, 8, 12, 50, 0)) == datetime(2015, 4, 8, 12, 50, 0)

    with pytest.raises(SchemaError):
        t.Date().validate(0)

    with pytest.raises(SchemaError):
        t.Date().validate("")

    with pytest.raises(SchemaError):
        t.Date().validate("3.2")

    with pytest.raises(SchemaError):
        t.Date().validate(3.3)

    with pytest.raises(SchemaError):
        t.Date().validate(None)

    with pytest.raises(SchemaError):
        t.Date().validate([])

    with pytest.raises(SchemaError):
        t.Date().validate({})


def test_schema_datetime():
    from datetime import date, datetime
    assert t.DateTime().validate(datetime(2015, 4, 8, 12, 50, 0)) == datetime(2015, 4, 8, 12, 50, 0)

    with pytest.raises(SchemaError):
        t.DateTime().validate(date(2015, 4, 8))

    with pytest.raises(SchemaError):
        t.DateTime().validate(0)

    with pytest.raises(SchemaError):
        t.DateTime().validate("")

    with pytest.raises(SchemaError):
        t.DateTime().validate("3.2")

    with pytest.raises(SchemaError):
        t.DateTime().validate(3.3)

    with pytest.raises(SchemaError):
        t.DateTime().validate(None)

    with pytest.raises(SchemaError):
        t.DateTime().validate([])

    with pytest.raises(SchemaError):
        t.DateTime().validate({})


def test_schema_none():
    assert t.IsNone().validate(None) is None

    with pytest.raises(SchemaError):
        t.IsNone().validate(3)

    with pytest.raises(SchemaError):
        t.IsNone().validate("3.2")

    with pytest.raises(SchemaError):
        t.IsNone().validate(3.3)

    with pytest.raises(SchemaError):
        t.IsNone().validate(False)

    with pytest.raises(SchemaError):
        t.IsNone().validate(True)

    with pytest.raises(SchemaError):
        t.IsNone().validate([])

    with pytest.raises(SchemaError):
        t.IsNone().validate({})
