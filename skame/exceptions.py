class SchemaError(Exception):
    """Exception used to indicate that the validation of some value failed."""

    def __init__(self, error):
        self.error = error


class SchemaErrors(Exception):
    """Exception used to indicate that the validation of multiple values failed."""

    def __init__(self, errors):
        self.errors = errors
