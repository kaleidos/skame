import pytest

from skame.exceptions import SchemaError
from skame.schemas import types as t


def test_schema_int():
    assert t.IntSchema().validate(3) == 3
    assert t.IntSchema().validate(1) == 1
    assert t.IntSchema().validate(0) == 0

    with pytest.raises(SchemaError):
        t.IntSchema().validate("3")

    with pytest.raises(SchemaError):
        t.IntSchema().validate(None)

    with pytest.raises(SchemaError):
        t.IntSchema().validate(False)

    with pytest.raises(SchemaError):
        t.IntSchema().validate(True)

    with pytest.raises(SchemaError):
        t.IntSchema().validate({})

    with pytest.raises(SchemaError):
        t.IntSchema().validate([])


def test_schema_float():
    assert t.FloatSchema().validate(3.2) == 3.2
    assert t.FloatSchema().validate(3.0) == 3.0

    with pytest.raises(SchemaError):
        t.FloatSchema().validate(3)

    with pytest.raises(SchemaError):
        t.FloatSchema().validate("3.2")

    with pytest.raises(SchemaError):
        t.FloatSchema().validate(None)

    with pytest.raises(SchemaError):
        t.FloatSchema().validate(False)

    with pytest.raises(SchemaError):
        t.FloatSchema().validate(True)

    with pytest.raises(SchemaError):
        t.FloatSchema().validate({})

    with pytest.raises(SchemaError):
        t.FloatSchema().validate([])


def test_schema_complex():
    assert t.ComplexSchema().validate(3 + 2j) == 3 + 2j
    assert t.ComplexSchema().validate(2j) == 2j

    with pytest.raises(SchemaError):
        t.ComplexSchema().validate(3)

    with pytest.raises(SchemaError):
        t.ComplexSchema().validate(3.3)

    with pytest.raises(SchemaError):
        t.ComplexSchema().validate("3.2")

    with pytest.raises(SchemaError):
        t.ComplexSchema().validate(None)

    with pytest.raises(SchemaError):
        t.ComplexSchema().validate(False)

    with pytest.raises(SchemaError):
        t.ComplexSchema().validate(True)

    with pytest.raises(SchemaError):
        t.ComplexSchema().validate({})

    with pytest.raises(SchemaError):
        t.ComplexSchema().validate([])


def test_schema_string():
    assert t.StringSchema().validate("test") == "test"
    assert t.StringSchema().validate("") == ""

    with pytest.raises(SchemaError):
        t.StringSchema().validate(3)

    with pytest.raises(SchemaError):
        t.StringSchema().validate(3.3)

    with pytest.raises(SchemaError):
        t.StringSchema().validate(None)

    with pytest.raises(SchemaError):
        t.StringSchema().validate(False)

    with pytest.raises(SchemaError):
        t.StringSchema().validate(True)

    with pytest.raises(SchemaError):
        t.StringSchema().validate({})

    with pytest.raises(SchemaError):
        t.StringSchema().validate([])


def test_schema_list():
    assert t.ListSchema().validate(["test", "test2"]) == ["test", "test2"]
    assert t.ListSchema().validate([]) == []

    with pytest.raises(SchemaError):
        t.ListSchema().validate(3)

    with pytest.raises(SchemaError):
        t.ListSchema().validate("3.2")

    with pytest.raises(SchemaError):
        t.ListSchema().validate(3.3)

    with pytest.raises(SchemaError):
        t.ListSchema().validate(None)

    with pytest.raises(SchemaError):
        t.ListSchema().validate(False)

    with pytest.raises(SchemaError):
        t.ListSchema().validate(True)

    with pytest.raises(SchemaError):
        t.ListSchema().validate({})


def test_schema_dict():
    assert t.DictSchema().validate({"test": "test", "test2": "test2"}) == {"test": "test", "test2": "test2"}
    assert t.DictSchema().validate({}) == {}

    with pytest.raises(SchemaError):
        t.DictSchema().validate(3)

    with pytest.raises(SchemaError):
        t.DictSchema().validate("3.2")

    with pytest.raises(SchemaError):
        t.DictSchema().validate(3.3)

    with pytest.raises(SchemaError):
        t.DictSchema().validate(None)

    with pytest.raises(SchemaError):
        t.DictSchema().validate(False)

    with pytest.raises(SchemaError):
        t.DictSchema().validate(True)

    with pytest.raises(SchemaError):
        t.DictSchema().validate([])


def test_schema_bool():
    assert t.BoolSchema().validate(True) is True
    assert t.BoolSchema().validate(False) is False

    with pytest.raises(SchemaError):
        t.BoolSchema().validate(0)

    with pytest.raises(SchemaError):
        t.BoolSchema().validate(1)

    with pytest.raises(SchemaError):
        t.BoolSchema().validate(3)

    with pytest.raises(SchemaError):
        t.BoolSchema().validate("3.2")

    with pytest.raises(SchemaError):
        t.BoolSchema().validate(3.3)

    with pytest.raises(SchemaError):
        t.BoolSchema().validate(None)

    with pytest.raises(SchemaError):
        t.BoolSchema().validate([])

    with pytest.raises(SchemaError):
        t.BoolSchema().validate({})


def test_schema_none():
    assert t.NoneSchema().validate(None) is None

    with pytest.raises(SchemaError):
        t.NoneSchema().validate(3)

    with pytest.raises(SchemaError):
        t.NoneSchema().validate("3.2")

    with pytest.raises(SchemaError):
        t.NoneSchema().validate(3.3)

    with pytest.raises(SchemaError):
        t.NoneSchema().validate(False)

    with pytest.raises(SchemaError):
        t.NoneSchema().validate(True)

    with pytest.raises(SchemaError):
        t.NoneSchema().validate([])

    with pytest.raises(SchemaError):
        t.NoneSchema().validate({})
