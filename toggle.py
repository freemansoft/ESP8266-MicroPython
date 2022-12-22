import time


class TogglePin:
    """A sample target class that gets invoked as a timer callback"""

    def __init__(self, pin):
        self._periodic_target = pin

    def toggle_pin_callback(self, t):
        """the callback method"""
        self._periodic_target.value(not self._periodic_target.value())
        # print("timer toggle callback %s" % (str(self._periodic_target.value())))
