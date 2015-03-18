import re

from gettext import gettext as _

from skame.schemas.base import Schema
from skame.exceptions import SchemaError


class NotEmptySchema(Schema):
    """Validator for checking if a value is not empty (boolean false)."""
    message = _("Empty value")

    def __init__(self, message=None):
        if message:
            self.message = message

    def _check(self, data):
        return bool(data)

    def validate(self, data: object) -> object:
        if not self._check(data):
            raise SchemaError(self.message)
        return data


class EmailSchema(Schema):
    """Validator for checking if a value is an email."""
    message = _("Invalid email format")
    user_regex = re.compile(
        r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*$"  # dot-atom
        r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-\011\013\014\016-\177])*"$)',  # quoted-string
        re.IGNORECASE)
    domain_regex = re.compile(
        r'(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}|[A-Z0-9-]{2,}(?<!-))$',
        re.IGNORECASE)
    domain_whitelist = []

    def __init__(self, message=None, domain_whitelist=None):
        if message:
            self.message = message

        if domain_whitelist:
            self.domain_whitelist = domain_whitelist

    def _validate_user_part(self, username):
        return self.user_regex.match(username) is not None

    def _validate_domain_part(self, domain):
        if domain in self.domain_whitelist:
            return True

        if self.domain_regex.match(domain) is not None:
            return True

        return False

    def _check(self, data):
        if not data or '@' not in data:
            return False

        user_part, domain_part = data.rsplit('@', 1)

        if not self._validate_user_part(user_part):
            return False

        if not self._validate_domain_part(domain_part):
            return False

        return True

    def validate(self, data: object) -> object:
        if not self._check(data):
            raise SchemaError(self.message)
        return data
