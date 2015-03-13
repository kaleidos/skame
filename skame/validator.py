from .exceptions import SchemaErrors


def clean_data_or_raise(schema: "Schema", data: dict, exc_type: "Exception"=SchemaErrors) -> dict:
    """Clean a data dict by passing it through a specified schema definition.

    If the data is not valid, an exception of type `exc_type` is raised with the form errors dict
    as its message.
    """
    try:
        return schema.validate(data)
    except SchemaErrors as e:
        raise exc_type(e.errors)


def validate(schema: "Schema", data: dict) -> (dict, dict):
    """Helper method for validate an schema.

    It returns a tuple with first argument with cleaned data and second
    argument errors.

    The second argument can be None if no errors found.
    """

    try:
        cleaned_data = schema.validate(data)
        return cleaned_data, None
    except SchemaErrors as e:
        return None, e.errors
