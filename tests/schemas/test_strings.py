import pytest

from skame.exceptions import SchemaError
from skame.schemas.strings import EmailSchema, NotEmptySchema


def test_email_schema_valid():
    assert EmailSchema().validate("test@test.com") == "test@test.com"
    assert EmailSchema().validate("test+1@test.com") == "test+1@test.com"
    assert EmailSchema().validate("test.1@test.com") == "test.1@test.com"


def test_email_schema_invalid():
    with pytest.raises(SchemaError):
        EmailSchema().validate("email-without-at-sign")

    with pytest.raises(SchemaError):
        EmailSchema().validate("email@invalid-domain")

    with pytest.raises(SchemaError):
        EmailSchema().validate("email\"with-invalid-username@test.com")

    with pytest.raises(SchemaError):
        EmailSchema().validate("email@with-extra-at-sign.com@test.com")

    with pytest.raises(SchemaError):
        EmailSchema().validate("test@localhost")


def test_email_schema_change_error_message():
    with pytest.raises(SchemaError) as excinfo:
        EmailSchema(message="Test Message Change").validate("test@localhost")
    assert excinfo.value.error == "Test Message Change"


def test_email_schema_domain_whitelist():
    assert EmailSchema(domain_whitelist=["localhost"]).validate("test@localhost") == "test@localhost"


def test_schema_not_empty_valid():
    assert NotEmptySchema().validate("string") == "string"
    assert NotEmptySchema().validate(7) == 7
    assert NotEmptySchema().validate(3.2) == 3.2
    assert NotEmptySchema().validate(["test"]) == ["test"]
    assert NotEmptySchema().validate({"test": "test"}) == {"test": "test"}


def test_schema_not_empty_invalid():
    with pytest.raises(SchemaError):
        NotEmptySchema().validate("")
    with pytest.raises(SchemaError):
        NotEmptySchema().validate(0)
    with pytest.raises(SchemaError):
        NotEmptySchema().validate(0.0)
    with pytest.raises(SchemaError):
        NotEmptySchema().validate([])
    with pytest.raises(SchemaError):
        NotEmptySchema().validate({})

def test_schema_not_empty_change_error_message():
    with pytest.raises(SchemaError) as excinfo:
        NotEmptySchema(message="Test Message Change").validate("")
    assert excinfo.value.error == "Test Message Change"
