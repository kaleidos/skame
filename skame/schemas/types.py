from skame.schemas.base import Type, StrictType, Is

import datetime

class Int(StrictType):
    def __init__(self, message=None):
        super().__init__(int, message)


class Float(Type):
    def __init__(self, message=None):
        super().__init__(float, message)


class Complex(Type):
    def __init__(self, message=None):
        super().__init__(complex, message)


class String(Type):
    def __init__(self, message=None):
        super().__init__(str, message)


class List(Type):
    def __init__(self, message=None):
        super().__init__(list, message)


class Dict(Type):
    def __init__(self, message=None):
        super().__init__(dict, message)


class Bool(Type):
    def __init__(self, message=None):
        super().__init__(bool, message)


class Date(Type):
    def __init__(self, message=None):
        super().__init__(datetime.date, message)


class DateTime(Type):
    def __init__(self, message=None):
        super().__init__(datetime.datetime, message)


class IsNone(Is):
    def __init__(self, message=None):
        super().__init__(None, message)
