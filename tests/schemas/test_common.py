import pytest

from skame.exceptions import SchemaError
from skame.schemas import common as c


def test_schema_choices():
    assert c.Choices([1,2,3]).validate(1) == 1
    assert c.Choices([1,2,3]).validate(2) == 2
    assert c.Choices([1,2,3]).validate(3) == 3

    with pytest.raises(SchemaError):
        c.Choices([1,2,3]).validate(4)

    with pytest.raises(SchemaError):
        c.Choices([1,2,3]).validate("3")

    with pytest.raises(SchemaError):
        c.Choices([1,2,3]).validate(None)

    with pytest.raises(SchemaError):
        c.Choices([1,2,3]).validate(False)

    # TODO: Check by type and by value
    # with pytest.raises(SchemaError):
    #     c.Choices([1,2,3]).validate(True)

    with pytest.raises(SchemaError):
        c.Choices([1,2,3]).validate({})

    with pytest.raises(SchemaError):
        c.Choices([1,2,3]).validate([])
