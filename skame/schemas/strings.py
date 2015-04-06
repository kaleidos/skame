import re

from gettext import gettext as _

from skame.schemas.base import Schema, Predicate
from skame.exceptions import SchemaError


class NotEmpty(Schema):
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


class Regex(Schema):
    regex = ''
    message = _('Invalid text.')

    def __init__(self, message=None, regex=None):
        if regex is not None:
            self.regex = regex
        if message is not None:
            self.message = message

        if isinstance(self.regex, str):
            self.regex = re.compile(self.regex)

    def _check(self, data):
        """
        Validates that the input matches the regular expression
        """
        if self.regex.search(data) is None:
            return False
        return True

    def validate(self, data: object) -> object:
        if not self._check(data):
            raise SchemaError(self.message)
        return data


class URL(RegexSchema):
    regex = re.compile(
        r'^(?:[a-z0-9\.\-]*)://'  # scheme is validated separately
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}(?<!-)\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    message = _('Invalid URL.')
    schemes = ['http', 'https', 'ftp', 'ftps']

    def __init__(self, message=None, schemes=None):
        super().__init__(message=message)
        if schemes is not None:
            self.schemes = schemes

    def _validate_scheme(self, data):
        scheme = data.split('://')[0].lower()

        if scheme in self.schemes:
            return True

        return False

    def _check(self, data):
        if not self._validate_scheme(data):
            return False

        if not super()._check(data):
            return False

        return True


class Email(Schema):
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


class MaxLength(Predicate):
    message = _('Too long string')

    def __init__(self, max_length, message=None):
        if message is not None:
            self.message = message

        self.predicate = lambda data: len(data) <= max_length


class MinLength(Predicate):
    message = _('Too short string')

    def __init__(self, min_length, message=None):
        if message is not None:
            self.message = message

        self.predicate = lambda data: len(data) >= min_length
