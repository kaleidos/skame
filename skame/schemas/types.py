from skame.schemas.base import Type, Is


class Int(Type):
    def __init__(self, message=None):
        super().__init__(int, message)

    def _check(self, data):
        if data is True or data is False:
            return False
        return super()._check(data)


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


class IsNone(Is):
    def __init__(self, message=None):
        super().__init__(None, message)
