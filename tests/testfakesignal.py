class FakeSignal(object):
    """
    This is a test class. Do NOT install this class on the MicroPython board.
    Required because signal is in the machine package -- seems silly
    """

    def __init__(self, pin, invert=False):
        self._pin = pin
        self._invert = invert
        self._value = 0

    def __str__(self) -> str:
        return "%s Inverted:%s" % (self._pin, str(self._invert))

    def value(self, value=None):
        """Cover for Signal/Pin value(). value is an int"""
        if value is not None:
            self._value = int(value)
            if self._invert:
                if self._value == 0:
                    self._pin.value(1)
                else:
                    self._pin.value(0)
            else:
                self._pin.value(self._value)
        return self._value

    def on(self):
        if self._invert:
            self._pin.value(0)
        else:
            self._pin.value(1)

    def off(self):
        if self._invert:
            self._pin.value(1)
        else:
            self._pin.value(0)
