
class FakePin(object):
    """This is a test class. Do NOT install this class on the MicroPython board."""

    def __init__(
        self,
        pin_no,
        pin_mode=-1
    ):
        self._value = 0
        self._pin_no = int(pin_no)
        self._mode = int(pin_mode)
        # pin modes supported on ESP8266
        self.IN = 0
        self.OUT = 1
        self.OPEN_DRAIN = 2

    def __str__(self) -> str:
        return "Pin(%d)" % (self._pin_no)

    def value(self,  value=None):
        if value is not None:
            self._value = int(value)
        return self._value
