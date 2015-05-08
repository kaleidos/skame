import re

from gettext import gettext as _

from skame.schemas.base import Schema, Predicate
from skame.exceptions import SchemaError


class IsStrictPositive(Schema):
    """Validator for checking if a value is greater than zero."""
    message = _("Value must be a positive number")

    def __init__(self, message=None):
        if message:
            self.message = message

    def _check(self, data):
        return (data > 0)

    def validate(self, data: object) -> object:
        if not self._check(data):
            raise SchemaError(self.message)
        return data


class IsPositiveOrZero(Schema):
    """Validator for checking if a value is greater than or equal zero."""
    message = _("Value must be a positive number or 0")

    def __init__(self, message=None):
        if message:
            self.message = message

    def _check(self, data):
        return (data >= 0)

    def validate(self, data: object) -> object:
        if not self._check(data):
            raise SchemaError(self.message)
        return data


class MinValue(Schema):
    """Validator for checking if a value is greater or equal than some value."""
    message = _("Value must be greater or equal than {minValue}")

    def __init__(self, minValue, message=None):
        self.minValue = minValue
        if message:
            self.message = message

    def _check(self, data):
        return (data >= self.minValue)

    def validate(self, data: object) -> object:
        if not self._check(data):
            raise SchemaError(self.message.format(minValue = self.minValue))
        return data


class MaxValue(Schema):
    """Validator for checking if a value is lower or equal than some value."""
    message = _("Value must be lower or equal than {maxValue}")

    def __init__(self, maxValue, message=None):
        self.maxValue = maxValue
        if message:
            self.message = message

    def _check(self, data):
        return (data <= self.maxValue)

    def validate(self, data: object) -> object:
        if not self._check(data):
            raise SchemaError(self.message.format(maxValue = self.maxValue))
        return data

