## Skame Schema validation system

[![Build Status](http://img.shields.io/travis/kaleidos/skame.svg?branch=master)](https://travis-ci.org/kaleidos/skame)
[![Coveralls Status](http://img.shields.io/coveralls/kaleidos/skame/master.svg)](https://coveralls.io/r/kaleidos/skame)

Modular pythonic library for validating python objects such as dicts, strings and the like. It's built on top
of well-defined, easy-to-use, reusable components.

<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc/generate-toc again -->
**Table of Contents**

- [Motivation](#motivation)
- [Features](#features)
- [Validators](#validators)
    - [Base validators](#base-validators)
        - [Predicate](#predicate)
        - [Type](#type)
        - [Is](#is)
        - [Pipe](#pipe)
    - [Combinators](#combinators)
        - [And](#and)
        - [Or](#or)
        - [Map](#map)

<!-- markdown-toc end -->

## Motivation

This library comes from the frustration with [schema](https://github.com/keleshev/schema/) library due to its
[validation design rule](https://github.com/keleshev/schema/issues/8)

## Features

- Built on top of a common protocol: `callable` which lets you base your validation rules on predicates that can be easily reused.
- `Map` validator validates all data at once and returns the errors grouped by fieldname.
- `Map` validator lets you define fields that depend on other fields.

## Validators

A validator is any class that inherits from `skame.base.Schema` which enforces the implementation of a `validate` method.

### Base validators ###

These are the most basic validators that are available and they validate one value at a time. They can and should be combined to create more complex validators if the one you're looking for is not included yet in the library.

#### Predicate ####

This the keystone of the validation system. Its philosophy is: give a predicate function and I'll hook it in the validation system.

Signature: `Predicate(<callable>[, message=<message>]).validate(<data>)`

Returns: `<data>` if `<callable>(<data>)` returns `True`. Raises `SchemaError(<message>)` otherwise.

Example:
```python
import os
import pytest
from skame.schemas.base import Predicate

assert Predicate(os.path.exists).validate("./") == "./"
assert Predicate(lambda n: n > 0).validate(123) == 123
with pytest.raises(SchemaError):
    Predicate(lambda n: n > 0).validate(-123)
```

#### Type ####

This is a specific kind of predicate that checks if the data is an instance of the specified type.

Signature: `Type(<type>[, message=<message>]).validate(<data>)`

Returns: `<data>` if `isinstance(<data>, <type>)` returns `True`. Raises `SchemaError(<message>)` otherwise.

Example:
```python
import pytest
from skame.schemas.base import Type

assert Type(object).validate("hai") == "hai"
assert Type(int).validate(123) == 123
with pytest.raises(SchemaError):
    Type(int).validate("123")
```

#### Is ####

This is a specific kind of predicate that checks if the data is **the same specified object**.

Signature: `Is(<obj>[, message=<message>]).validate(<data>)`

Returns: `<data>` if `<data> is <obj>` returns `True`. Raises `SchemaError(<message>)` otherwise.

Example:
```python
import pytest
from skame.schemas.base import Is

assert Is("hai").validate("hai") == "hai"
assert Is(123).validate(123) == 123

singleton = object()
assert Is(singleton).validate(singleton) == singleton

with pytest.raises(SchemaError):
    Is(singleton).validate(object())
```

#### Pipe ####

This is a specific kind of predicate that checks if the data can travel through a pipe without causing an error.

Signature: `Pipe(<callable>[, *<callable>, message=<message>]).validate(<data>)`

Returns: `<callable>(<data>)` if `callable(<data>)` raises no exception. Raises `SchemaError(<message>)` otherwise.

Example:
```python
import pytest
from skame.schemas.base import Pipe

assert Pipe(int).validate("123") == 123
assert Pipe(int, str).validate(123.0) == "123"
assert Pipe(int, str, lambda _: (42,)).validate(123.0) == (42,)
with pytest.raises(SchemaError):
    Pipe(int).validate(None)
```

### Combinators ###

In order to combine simple validators we use combinators.

#### And ####

This combinator runs all specified validators in order and succeeds if all validators succeed.

Signature: `And(<validator>[, <validator>...]).validate(<data>)`

Returns: The value returned by the last validator if `<validator>(<data>)` is successful for each validator. Raises `SchemaError` or `SchemaErrors` depending on the validator that failed.

Example:
```python
import pytest
from skame.schemas.base import And, Pipe, Predicate, Is

assert And(Pipe(int), Predicate(lambda n: n == 42)).validate("42") == 42

with pytest.raises(SchemaError):
    And(Pipe(str), Is(42)).validate("20")
```

#### Or ####

This combinator runs all specified validators in order and succeeds if any validator succeeds.

Signature: `Or(<validator>[, <validator>...]).validate(<data>)`

Returns: The value returned by the last validator if `<validator>(<data>)` is successful for any validator. Raises `SchemaError` or `SchemaErrors` depending on the validator that failed.

Example:
```python
import pytest
from skame.schemas.base import Or, Pipe, Predicate, Is

assert Or(b.Type(str), b.Predicate(lambda n: n == 42)).validate("20") == "20"
assert Or(b.Type(str), b.Predicate(lambda n: n == 42)).validate(42) == 42
with pytest.raises(SchemaError):
    Or(b.Type(str), b.Predicate(lambda n: n == 42)).validate(20)
```

#### Map ####

This combinator maps validators to names, runs all validators (without any specific order) and succeeds if all validators succeed.

Signature: `Map({ <name>: <validator> }).validate(<data>)`

Note: `<data>` must be a dict or dict-like object.

Returns: The value returned by the last validator if `<validator>(<data>)` is successful for any validator. Raises `SchemaErrors` where the message is a dict with the form `{ <name>: <error msg>}`.

Example:
```python
import pytest
from skame.schemas.base import Map, Pipe, Predicate

schema = Map({
    "name": Predicate(lambda name: 0 < len(name) < 25)
})
assert schema.validate({"name": "First name", "age": "28"}) == {"name": "First name"}

schema = Map({
    "name": And(Predicate(lambda name: 0 < len(name) < 25), Pipe(len))
})
assert schema.validate({"name": "First name", "age": "28"}) == {"name": 10}


with pytest.raises(SchemaErrors):
    schema.validate({"name": ""})
```

##### Marking fields as optional #####

In the map validator you can mark fields as optional, that is, they are validated only if present and not required, for example:

```python
assert Map({"name": Pipe(str), "age": Pipe(int)}).required == {"name", "age"}
assert Map({"name": Pipe(str), Optional("age"): Pipe(int)}).required == {"name"}

validator = Map({"name": Type(str), Optional("age"): Type(int)})
assert validator.validate({"name": "John"}) == {"name": "John"}
with pytest.raises(SchemaErrors):
    validator.validate({"name": "John", "age": 1.2})  # age must be an int
```

##### Marking fields as dependent #####

In the map validator you can mark fields as dependent on others fields already validated, for example:

```python
def uk_postalcode_or_none(data):
    if data.get("country") == "GBR":
        validator = is_uk_postalcode
    else:
        validator = is_none
    return validator.validate(data.get("postalcode", ""))


LivelocationValidator = Map({
    "country": And(Type(str), Predicate(lambda x: len(x) == 3)),
    Dependent("postalcode"): Pipe(uk_postalcode_or_none)
})
```
