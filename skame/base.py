import functools
import types
import collections.abc
from abc import abstractmethod, ABCMeta

from gettext import gettext as _

from .exceptions import SchemaError, SchemaErrors
from .utils import compose


class Optional:
    """Special class to mark fields as optional."""
    __slots__ = ("name",)

    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if isinstance(other, str):
            return self.name == other
        return self.name == other.name


class Dependent:
    """Special class to mark fields as dependent."""
    __slots__ = ("name",)

    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if isinstance(other, str):
            return self.name == other
        return self.name == other.name


def is_field_optional(field: object) -> bool:
    """Utility function to check if a field is an optional field."""
    return isinstance(field, Optional)


def is_field_dependent(field: object) -> bool:
    """Utility function to check if a field is a dependent field."""
    return isinstance(field, Dependent)


@functools.singledispatch
def schema(definition: "callable") -> "Pipe":
    return Pipe(definition)


@schema.register(types.LambdaType)
def schema_callable(definition: "callable") -> "Predicate":
    return Predicate(definition)


@schema.register(collections.abc.Mapping)
def schema_map(definition: dict) -> "Map":
    return Map(definition)


class Schema(metaclass=ABCMeta):
    """Abstract base class for creating schema validators."""

    @abstractmethod
    def validate(self, data: object) -> object:
        """Validate the received data and return it sanitazed.

        If the data is not valid a `SchemaError` or `SchemaErrors` exception is raised depending on
        if the validation occurs on one or multiple values.
        """
        pass


class Type(Schema):
    """Validator for checking the type of a value."""
    message = _("Not of type `{type}`")

    def __init__(self, type, message=None):
        self.type = type

        if message:
            self.message = message

    def _check(self, data):
        return isinstance(data, self.type)

    def validate(self, data: object) -> object:
        if not self._check(data):
            message = self.message.format(type=self.type)
            raise SchemaError(message)
        return data


class Is(Type):
    """Validator for checking the identity of a value."""
    message = _("Is not `{type}`")

    def _check(self, data):
        return data is self.type


class PredicateBase(Schema):
    """Base class for define predicates."""

    message = _("`{predicate}({data})` should evaluate to True.")

    def __init__(self, message: str=None):
        if message:
            self.message = message

    def validate(self, data: object) -> object:
        if not self.predicate(data):
            message = self.message.format(predicate=self.predicate, data=data)
            raise SchemaError(message)
        return data


class Predicate(PredicateBase):
    """
    Validator for checking if a predicate accepts a value.

    This is concrete case of predicate that accept a callable
    as a parameter.
    """

    def __init__(self, predicate: "callable"=None, message: str=None):
        super().__init__(message)
        self.predicate = predicate


class Pipe(Schema):
    """Validator that tries to convert a value into another value."""

    message = None

    def __init__(self, pipe: "callable", *extra_pipes, message: str=None):
        self.message = message

        if extra_pipes:
            pipes = reversed((pipe,) + extra_pipes)
            self.pipe = compose(*pipes)
        else:
            self.pipe = pipe

    def validate(self, data: object,
                 watch_for_exceptions: Exception=(ValueError, TypeError)) -> object:
        try:
            return self.pipe(data)
        except watch_for_exceptions as e:
            message = str(e)
            raise SchemaError(self.message or message)


class And(Schema):
    """Validator to combine another validators and only succeeds if all succeed."""

    def __init__(self, condition1: "Schema", *extra_conditions):
        self.conditions = list(reversed((condition1,) + extra_conditions))

    def validate(self, data: object) -> object:
        validator = compose(*[condition.validate for condition in self.conditions])
        return validator(data)


class Map(Schema):
    """Validator that validates a map of field names to validators."""

    def __init__(self, mapping: dict):
        required = set()
        optional = set()
        dependent = set()

        for field in mapping:
            if is_field_optional(field):
                dest = optional
            elif is_field_dependent(field):
                dest = dependent
            else:
                dest = required
            dest.add(field)

        self.required = required
        self.optional = optional
        self.dependent = dependent
        self.mapping = mapping

    def _validate(self, data: dict, fields: dict, value_getter: "function") -> dict:
        errors = {}
        result = {}

        for field in fields:
            try:
                value = value_getter(data, field)
                cleaned_value = self.mapping[field].validate(value)
            except KeyError:
                errors[str(field)] = _("Field `{0}` is required.").format(field)
            except SchemaError as e:
                errors[str(field)] = e.error
            else:
                result[str(field)] = cleaned_value

        if errors:
            raise SchemaErrors(errors)

        return result

    def validate(self, data: dict) -> dict:
        # normal fields validation
        fields = self.required | self.optional & set(data.keys())

        result = self._validate(data, fields, dict.__getitem__)

        # dependent fields validation
        fields = self.dependent
        result.update(self._validate(data, fields, lambda data, field: data))

        return result
