class PeriodicOperator:
    """A construct that binds a timer to a function.
    PeriodicOperator(Timer(-1), ms, function)
    """

    def __init__(self, timer, period, callback):
        self._timer_ = timer
        self._period_ = period
        self._callback_ = callback
        self._isRunning_ = False

    def __str__(self) -> str:
        return "%s is running: %d" % (self._timer_, self._isRunning_)

    def start(self):
        if not self._isRunning_:
            self._timer_.init(period=self._period_, callback=self._callback_)
            self._isRunning_ = True

    def stop(self):
        if self._isRunning_:
            self._timer_.deinit()
            self._isRunning_ = False

    def running(self):
        return self._isRunning_
