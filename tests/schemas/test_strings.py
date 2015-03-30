import pytest

from skame.exceptions import SchemaError
from skame.schemas.strings import (EmailSchema, NotEmptySchema,
                                   MaxLengthSchema, MinLengthSchema, URLSchema,
                                   RegexSchema)


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


def test_url_schema_valid():
    assert URLSchema().validate("ftp://ftp.is.co.za/rfc/rfc1808.txt") == "ftp://ftp.is.co.za/rfc/rfc1808.txt"
    assert URLSchema().validate("http://www.ietf.org/rfc/rfc2396.txt") == "http://www.ietf.org/rfc/rfc2396.txt"
    assert URLSchema().validate("http://[2001:db8::7]/c=GB?objectClass?one") == "http://[2001:db8::7]/c=GB?objectClass?one"


def test_url_schema_invalid():
    with pytest.raises(SchemaError):
        URLSchema().validate("without-protocol.com")

    with pytest.raises(SchemaError):
        URLSchema().validate("http://without-dot-part")

    with pytest.raises(SchemaError):
        URLSchema().validate("with://invalid-protocol")

def test_url_schema_change_error_message():
    with pytest.raises(SchemaError) as excinfo:
        URLSchema(message="Test Message Change").validate("without-protocol")
    assert excinfo.value.error == "Test Message Change"


def test_url_schema_changing_schemas():
    assert URLSchema(schemes=["new"]).validate("new://www.test.com") == "new://www.test.com"


def test_url_regex_valid():
    assert RegexSchema(regex=r"^test$").validate("test") == "test"
    assert RegexSchema(regex=r"^[A-Z]{2,}").validate("TEST") == "TEST"


def test_url_regex_invalid():
    with pytest.raises(SchemaError):
        RegexSchema(regex=r"^test$").validate("bad-test")

    with pytest.raises(SchemaError):
        RegexSchema(regex=r"^[A-Z]{2,}").validate("B")

    with pytest.raises(SchemaError):
        RegexSchema(regex=r"^[A-Z]{2,}").validate("bad")

def test_url_regex_change_error_message():
    with pytest.raises(SchemaError) as excinfo:
        RegexSchema(regex=r"^test$", message="Test Message Change").validate("bad-test")
    assert excinfo.value.error == "Test Message Change"


def test_not_empty_schema_valid():
    assert NotEmptySchema().validate("string") == "string"
    assert NotEmptySchema().validate(7) == 7
    assert NotEmptySchema().validate(3.2) == 3.2
    assert NotEmptySchema().validate(["test"]) == ["test"]
    assert NotEmptySchema().validate({"test": "test"}) == {"test": "test"}


def test_not_empty_schema_invalid():
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


def test_not_empty_schema_change_error_message():
    with pytest.raises(SchemaError) as excinfo:
        NotEmptySchema(message="Test Message Change").validate("")
    assert excinfo.value.error == "Test Message Change"


def test_max_length_schema_valid():
    assert MaxLengthSchema(10).validate("test") == "test"

def test_max_length_schema_invalid():
    with pytest.raises(SchemaError):
        MaxLengthSchema(1).validate("test")

def test_max_length_schema_change_error_message():
    with pytest.raises(SchemaError) as excinfo:
        MaxLengthSchema(1, message="Test Message Change").validate("test")
    assert excinfo.value.error == "Test Message Change"

def test_min_length_schema_valid():
    assert MinLengthSchema(1).validate("test") == "test"

def test_min_length_schema_invalid():
    with pytest.raises(SchemaError):
        MinLengthSchema(10).validate("test")

def test_min_length_schema_change_error_message():
    with pytest.raises(SchemaError) as excinfo:
        MinLengthSchema(10, message="Test Message Change").validate("test")
    assert excinfo.value.error == "Test Message Change"
