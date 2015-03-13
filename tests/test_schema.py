import pytest

from skame import schemas as s
from skame.validator import clean_data_or_raise, validate


def test_schema_as_predicate():
    import os

    assert s.Predicate(os.path.exists).validate("./") == "./"
    assert s.Predicate(lambda n: n > 0).validate(123) == 123
    with pytest.raises(s.SchemaError):
        s.Predicate(lambda n: n > 0).validate(-123)


def test_schema_as_type():
    assert s.Type(object).validate("hai") == "hai"
    assert s.Type(int).validate(123) == 123
    with pytest.raises(s.SchemaError):
        s.Type(int).validate("123")


def test_schema_as_pipe():
    assert s.Pipe(int).validate("123") == 123
    assert s.Pipe(int, str).validate(123.0) == "123"
    assert s.Pipe(int, str, lambda s: (42,)).validate(123.0) == (42,)
    with pytest.raises(s.SchemaError):
        s.Pipe(int).validate(None)


def test_schema_logic_and():
    assert s.And(s.Pipe(int), s.Predicate(lambda n: n == 42)).validate("42") == 42
    with pytest.raises(s.SchemaError):
        s.And(s.Pipe(str), s.Predicate(lambda n: n == 42)).validate("20")


def test_schema_as_map():
    schema = s.Map({"name": s.Predicate(lambda name: 0 < len(name) < 25)})

    assert schema.validate({"name": "First name", "age": "28"}) == {"name": "First name"}
    with pytest.raises(s.SchemaErrors):
        schema.validate({"name": ""})


def test_schema_as_map_required_fields():
    assert s.Map({"name": s.Pipe(str), "age": s.Pipe(int)}).required == {"name", "age"}
    assert s.Map({"name": s.Pipe(str), s.Optional("age"): s.Pipe(int)}).required == {"name"}
    with pytest.raises(s.SchemaErrors):
        s.Map({"name": s.Pipe(str), "age": s.Pipe(int)}).validate({"name": "Name"})


def test_schema_as_map_optional_fields():
    validator = s.Map({"name": s.Type(str), s.Optional("age"): s.Type(int)})
    assert validator.required == {"name"}

    validator = s.Map({})
    assert validator.validate({"name": "John", "age": 25}) == {}

    validator = s.Map({"name": s.Type(str), s.Optional("age"): s.Type(int)})
    assert validator.validate({"name": "John"}) == {"name": "John"}

    validator = s.Map({"name": s.Type(str), s.Optional("age"): s.Type(int)})
    assert validator.validate({"name": "John", "whatever": True}) == {"name": "John"}

    validator = s.Map({"name": s.Type(str), s.Optional("age"): s.Type(int)})
    with pytest.raises(s.SchemaErrors):
        validator.validate({"name": "John", "age": 1.2})


def test_schema_singledispatch():
    import os

    assert type(s.schema(int)) == s.Pipe
    assert type(s.schema(lambda: 3 < 2)) == s.Predicate
    assert type(s.schema(os.path.exists)) == s.Predicate
    assert type(s.schema({"age": s.Pipe("int")})) == s.Map


class TestCleanDataOrRaise:
    schema = s.schema({
        "name": s.Predicate(lambda name: len(name) > 0),
        "age": s.And(
            s.Pipe(int, message="User age must be an integer"),
            s.Predicate(lambda age: 18 <= age < 99, message="User has to be an adult")
        )
    })

    def test_valid(self):
        data = {"name": "skame", "age": "28"}
        assert clean_data_or_raise(self.schema, data) == {"name": "skame", "age": 28}

    def test_not_valid(self):
        with pytest.raises(s.SchemaErrors):
            clean_data_or_raise(self.schema, {})

    def test_custom_validation_error(self):
        try:
            clean_data_or_raise(self.schema, {"name": "skame", "age": "1"})
        except s.SchemaErrors as e:
            assert e.errors["age"] == "User has to be an adult"

        try:
            clean_data_or_raise(self.schema, {"name": "skame", "age": "skame"})
        except s.SchemaErrors as e:
            assert e.errors["age"] == "User age must be an integer"


class TestValidate:
    schema = s.schema({
        "name": s.Predicate(lambda name: len(name) > 0),
        "age": s.And(
            s.Pipe(int, message="User age must be an integer"),
            s.Predicate(lambda age: 18 <= age < 99, message="User has to be an adult")
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
