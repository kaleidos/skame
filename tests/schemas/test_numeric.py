import pytest

from skame.exceptions import SchemaError
from skame.schemas.numeric import (IsStrictPositive, IsPositiveOrZero,
                                   MinValue, MaxValue)


def test_is_strict_positive_schema_valid():
    assert IsStrictPositive().validate(10) == 10


def test_is_strict_positive_schema_invalid():
    with pytest.raises(SchemaError):
        IsStrictPositive().validate(0)
    with pytest.raises(SchemaError):
        IsStrictPositive().validate(-1)


def test_is_positive_or_zero_schema_valid():
    assert IsPositiveOrZero().validate(0) == 0
    assert IsPositiveOrZero().validate(10) == 10


def test_is_positive_or_zero_schema_invalid():
    with pytest.raises(SchemaError):
        IsPositiveOrZero().validate(-1)


def test_min_value_schema_valid():
    assert MinValue(10).validate(10) == 10
    assert MinValue(10).validate(20) == 20


def test_min_value_schema_invalid():
    with pytest.raises(SchemaError):
        MinValue(10).validate(1)


def test_max_value_schema_valid():
    assert MaxValue(10).validate(10) == 10
    assert MaxValue(10).validate(5) == 5


def test_max_value_schema_invalid():
    with pytest.raises(SchemaError):
        MaxValue(10).validate(20)

