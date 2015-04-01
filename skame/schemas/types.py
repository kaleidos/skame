from skame.schemas.base import Type, Is


class IntSchema(Type):
    def __init__(self, message=None):
        super().__init__(int, message)

    def _check(self, data):
        if data is True or data is False:
            return False
        return super()._check(data)


class FloatSchema(Type):
    def __init__(self, message=None):
        super().__init__(float, message)


class ComplexSchema(Type):
    def __init__(self, message=None):
        super().__init__(complex, message)


class StringSchema(Type):
    def __init__(self, message=None):
        super().__init__(str, message)


class ListSchema(Type):
    def __init__(self, message=None):
        super().__init__(list, message)


class DictSchema(Type):
    def __init__(self, message=None):
        super().__init__(dict, message)


class BoolSchema(Type):
    def __init__(self, message=None):
        super().__init__(bool, message)


class NoneSchema(Is):
    def __init__(self, message=None):
        super().__init__(None, message)
