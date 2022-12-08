
class FakePin(object):
    """This is a test class. Do NOT install this class on the MicroPython board."""

    def __init__(
        self,
        initialvalue
    ):
        self._value = int(initialvalue)
        pass

    def value(self,  value=None):
        if value is not None:
            self._value = int(value)
        return self._value
