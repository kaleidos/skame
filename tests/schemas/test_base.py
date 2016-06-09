import pytest

from skame.schemas import base as b
from skame.exceptions import SchemaError, SchemaErrors
from skame.validator import clean_data_or_raise, validate


def test_schema_as_predicate():
    import os

    assert b.Predicate(os.path.exists).validate("./") == "./"
    assert b.Predicate(lambda n: n > 0).validate(123) == 123
    with pytest.raises(SchemaError):
        b.Predicate(lambda n: n > 0).validate(-123)


def test_schema_as_type():
    assert b.Type(object).validate("hai") == "hai"
    assert b.Type(int).validate(123) == 123
    with pytest.raises(SchemaError):
        b.Type(int).validate("123")


def test_schema_as_is():
    assert b.Is("hai").validate("hai") == "hai"
    assert b.Is(123).validate(123) == 123

    singleton = object()

    assert b.Is(singleton).validate(singleton) == singleton
    with pytest.raises(SchemaError):
        b.Is(singleton).validate(object())


def test_schema_as_pipe():
    assert b.Pipe(int).validate("123") == 123
    assert b.Pipe(int, str).validate(123.0) == "123"
    assert b.Pipe(int, str, lambda _: (42,)).validate(123.0) == (42,)
    with pytest.raises(SchemaError):
        b.Pipe(int).validate(None)


def test_schema_logic_and():
    assert b.And(b.Pipe(int), b.Predicate(lambda n: n == 42)).validate("42") == 42
    with pytest.raises(SchemaError):
        b.And(b.Pipe(str), b.Predicate(lambda n: n == 42)).validate("20")


def test_schema_logic_or():
    assert b.Or(b.Type(str), b.Predicate(lambda n: n == 42)).validate("20") == "20"
    assert b.Or(b.Type(str), b.Predicate(lambda n: n == 42)).validate(42) == 42
    with pytest.raises(SchemaError):
        b.Or(b.Type(str), b.Predicate(lambda n: n == 42)).validate(20)


def test_schema_as_map():
    schema = b.Map({"name": b.Predicate(lambda name: 0 < len(name) < 25)})
    assert schema.validate({"name": "First name", "age": "28"}) == {"name": "First name"}

    schema = b.Map({"name": b.And(b.Predicate(lambda name: 0 < len(name) < 25), b.Pipe(len))})
    assert schema.validate({"name": "First name", "age": "28"}) == {"name": 10}

    with pytest.raises(SchemaErrors):
        schema.validate({"name": ""})


def test_schema_as_map_required_fields():
    assert b.Map({"name": b.Pipe(str), "age": b.Pipe(int)}).required == {"name", "age"}
    assert b.Map({"name": b.Pipe(str), b.Optional("age"): b.Pipe(int)}).required == {"name"}
    with pytest.raises(SchemaErrors):
        b.Map({"name": b.Pipe(str), "age": b.Pipe(int)}).validate({"name": "Name"})


def test_schema_as_map_optional_fields():
    validator = b.Map({"name": b.Type(str), b.Optional("age"): b.Type(int)})
    assert validator.required == {"name"}

    validator = b.Map({})
    assert validator.validate({"name": "John", "age": 25}) == {}

    validator = b.Map({"name": b.Type(str), b.Optional("age"): b.Type(int)})
    assert validator.validate({"name": "John"}) == {"name": "John"}

    validator = b.Map({"name": b.Type(str), b.Optional("age"): b.Type(int)})
    assert validator.validate({"name": "John", "whatever": True}) == {"name": "John"}

    validator = b.Map({"name": b.Type(str), b.Optional("age"): b.Type(int)})
    with pytest.raises(SchemaErrors):
        validator.validate({"name": "John", "age": 1.2})


def test_schema_singledispatch():
    import os

    assert type(b.schema(int)) == b.Pipe
    assert type(b.schema(lambda: 3 < 2)) == b.Predicate
    assert type(b.schema(os.path.exists)) == b.Predicate
    assert type(b.schema({"age": b.Pipe("int")})) == b.Map


class TestCleanDataOrRaise:
    schema = b.schema({
        "name": b.Predicate(lambda name: len(name) > 0),
        "age": b.And(
            b.Pipe(int, message="User age must be an integer"),
            b.Predicate(lambda age: 18 <= age < 99, message="User has to be an adult")
        )
    })

    def test_valid(self):
        data = {"name": "skame", "age": "28"}
        assert clean_data_or_raise(self.schema, data) == {"name": "skame", "age": 28}

    def test_not_valid(self):
        with pytest.raises(SchemaErrors):
            clean_data_or_raise(self.schema, {})

    def test_custom_validation_error(self):
        try:
            clean_data_or_raise(self.schema, {"name": "skame", "age": "1"})
        except SchemaErrors as e:
            assert e.errors["age"] == "User has to be an adult"

        try:
            clean_data_or_raise(self.schema, {"name": "skame", "age": "skame"})
        except SchemaErrors as e:
            assert e.errors["age"] == "User age must be an integer"


class TestValidate:
    schema = b.schema({
        "name": b.Predicate(lambda name: len(name) > 0),
        "age": b.And(
            b.Pipe(int, message="User age must be an integer"),
            b.Predicate(lambda age: 18 <= age < 99, message="User has to be an adult")
        )
    })

    def test_valid(self):
        data = {"name": "skame", "age": "28"}
        assert validate(self.schema, data) == ({"name": "skame", "age": 28}, None)

    def test_not_valid(self):
        assert validate(self.schema, {}) == (None, {'name': 'Field `name` is required.', 'age': 'Field `age` is required.'})

    def test_custom_validation_error(self):
        data = {"name": "skame", "age": "1"}
        assert validate(self.schema, data) == (None, {"age": "User has to be an adult"})
        data = {"name": "skame", "age": ""}
        assert validate(self.schema, data) == (None, {"age": "User age must be an integer"})


def test_nested_map_errors():
    data = {
        "name": 1000,
        "amount": {
            "amount": 1000,
            "currency": 1000
        }
    }

    validator = b.schema({
        "c": b.Type(str),
        "amount": b.Map({
            "amount": b.Type(str),
            "currency": b.Type(str)
        })
    })

    with pytest.raises(SchemaErrors) as exc:
        validator.validate(data)

    expected = {
        'c': 'Field `c` is required.',
        'amount': {
            'amount': "Not of type `<class 'str'>`",
            'currency': "Not of type `<class 'str'>`"
        }
    }
    assert expected == exc.value.errors
