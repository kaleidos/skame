class SchemaError(Exception):
    """Exception used to indicate that the validation of some value failed."""

    def __init__(self, error, error_code="invalid"):
        self.error = error
        self.error_code = error_code


class SchemaErrors(Exception):
    """Exception used to indicate that the validation of multiple values failed."""

    def __init__(self, errors):
        self.errors = errors
