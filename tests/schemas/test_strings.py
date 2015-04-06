import pytest

from skame.exceptions import SchemaError
from skame.schemas.strings import (Email, NotEmpty,
                                   MaxLength, MinLength, URL,
                                   Regex)


def test_email_schema_valid():
    assert Email().validate("test@test.com") == "test@test.com"
    assert Email().validate("test+1@test.com") == "test+1@test.com"
    assert Email().validate("test.1@test.com") == "test.1@test.com"


def test_email_schema_invalid():
    with pytest.raises(SchemaError):
        Email().validate("email-without-at-sign")

    with pytest.raises(SchemaError):
        Email().validate("email@invalid-domain")

    with pytest.raises(SchemaError):
        Email().validate("email\"with-invalid-username@test.com")

    with pytest.raises(SchemaError):
        Email().validate("email@with-extra-at-sign.com@test.com")

    with pytest.raises(SchemaError):
        Email().validate("test@localhost")


def test_email_schema_change_error_message():
    with pytest.raises(SchemaError) as excinfo:
        Email(message="Test Message Change").validate("test@localhost")
    assert excinfo.value.error == "Test Message Change"


def test_email_schema_domain_whitelist():
    assert Email(domain_whitelist=["localhost"]).validate("test@localhost") == "test@localhost"


def test_url_schema_valid():
    assert URL().validate("ftp://ftp.is.co.za/rfc/rfc1808.txt") == "ftp://ftp.is.co.za/rfc/rfc1808.txt"
    assert URL().validate("http://www.ietf.org/rfc/rfc2396.txt") == "http://www.ietf.org/rfc/rfc2396.txt"
    assert URL().validate("http://[2001:db8::7]/c=GB?objectClass?one") == "http://[2001:db8::7]/c=GB?objectClass?one"


def test_url_schema_invalid():
    with pytest.raises(SchemaError):
        URL().validate("without-protocol.com")

    with pytest.raises(SchemaError):
        URL().validate("http://without-dot-part")

    with pytest.raises(SchemaError):
        URL().validate("with://invalid-protocol")

def test_url_schema_change_error_message():
    with pytest.raises(SchemaError) as excinfo:
        URL(message="Test Message Change").validate("without-protocol")
    assert excinfo.value.error == "Test Message Change"


def test_url_schema_changing_schemas():
    assert URL(schemes=["new"]).validate("new://www.test.com") == "new://www.test.com"


def test_url_regex_valid():
    assert Regex(regex=r"^test$").validate("test") == "test"
    assert Regex(regex=r"^[A-Z]{2,}").validate("TEST") == "TEST"


def test_url_regex_invalid():
    with pytest.raises(SchemaError):
        Regex(regex=r"^test$").validate("bad-test")

    with pytest.raises(SchemaError):
        Regex(regex=r"^[A-Z]{2,}").validate("B")

    with pytest.raises(SchemaError):
        Regex(regex=r"^[A-Z]{2,}").validate("bad")

def test_url_regex_change_error_message():
    with pytest.raises(SchemaError) as excinfo:
        Regex(regex=r"^test$", message="Test Message Change").validate("bad-test")
    assert excinfo.value.error == "Test Message Change"


def test_not_empty_schema_valid():
    assert NotEmpty().validate("string") == "string"
    assert NotEmpty().validate(7) == 7
    assert NotEmpty().validate(3.2) == 3.2
    assert NotEmpty().validate(["test"]) == ["test"]
    assert NotEmpty().validate({"test": "test"}) == {"test": "test"}


def test_not_empty_schema_invalid():
    with pytest.raises(SchemaError):
        NotEmpty().validate("")
    with pytest.raises(SchemaError):
        NotEmpty().validate(0)
    with pytest.raises(SchemaError):
        NotEmpty().validate(0.0)
    with pytest.raises(SchemaError):
        NotEmpty().validate([])
    with pytest.raises(SchemaError):
        NotEmpty().validate({})


def test_not_empty_schema_change_error_message():
    with pytest.raises(SchemaError) as excinfo:
        NotEmpty(message="Test Message Change").validate("")
    assert excinfo.value.error == "Test Message Change"


def test_max_length_schema_valid():
    assert MaxLength(10).validate("test") == "test"

def test_max_length_schema_invalid():
    with pytest.raises(SchemaError):
        MaxLength(1).validate("test")

def test_max_length_schema_change_error_message():
    with pytest.raises(SchemaError) as excinfo:
        MaxLength(1, message="Test Message Change").validate("test")
    assert excinfo.value.error == "Test Message Change"

def test_min_length_schema_valid():
    assert MinLength(1).validate("test") == "test"

def test_min_length_schema_invalid():
    with pytest.raises(SchemaError):
        MinLength(10).validate("test")

def test_min_length_schema_change_error_message():
    with pytest.raises(SchemaError) as excinfo:
        MinLength(10, message="Test Message Change").validate("test")
    assert excinfo.value.error == "Test Message Change"
