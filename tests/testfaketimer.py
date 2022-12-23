# TODO: Put a timer object in there maybe something like https://stackoverflow.com/questions/12435211/threading-timer-repeat-function-every-n-seconds
class FakeTimer:
    """Meets the machine Timer API but does not actually run a timer"""

    def __init__(self, timer_no):
        """placeholder"""
        self._timer_no = timer_no
        self._period = -1
        self._callback = None
        self._is_running = False

    def __str__(self) -> str:
        return "Timer %d period %d is running %s " % (
            self._timer_no,
            self._period,
            self._is_running,
        )

    def init(self, period=-1, callback=None):
        self._period = period
        self._callback = callback
        self._is_running = True
        print("init() timer %d" % (self._timer_no))

    def deinit(self):
        self._is_running = False
        print("deinit() timer %d" % (self._timer_no))
