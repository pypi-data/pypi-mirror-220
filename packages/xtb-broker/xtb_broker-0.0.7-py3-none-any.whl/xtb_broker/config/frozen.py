from config.exception import FrozenError


class Frozen(object):
    """
    Frozen class gives the ability to freeze the inheriting class attributes once an object is initialized

    Attributes
    ----------
    __frozen__: str
        attribute to freeze an object attributes after its initialization
    """
    __frozen__ = False

    def __setattr__(self, attr, value):
        if self.__frozen__ and not hasattr(self, attr):
            raise FrozenError(f"Can not set new attribute '{attr}'. "
                              f"{self.__class__.__name__} is an instance of a frozen class")
        object.__setattr__(self, attr, value)

    def _freeze(self):
        self.__frozen__ = True
