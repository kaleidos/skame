from skame.schemas.base import Schema, SchemaError
from gettext import gettext as _


class ChoicesSchema(Schema):
    message = _("Value not in the valid choices ({choices})")

    def __init__(self, choices, message=None):
        self.choices = choices
        if message:
            self.message = message

    def validate(self, data: object) -> object:
        if not data in self.choices:
            message = self.message.format(choices=", ".join(map(str, self.choices)))
            raise SchemaError(message)
        return data
