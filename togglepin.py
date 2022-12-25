class TogglePin:
    """A sample target class that gets invoked as a timer callback"""

    def __init__(self, pin, schedule=None):
        """
        ;param pin : i/O pin
        ;param schedule : if running in IRQ should be micropython.schedule for safe irq handling
        """
        self.target = pin
        # need to allocate the reference prior to using it in a callback
        self.toggle_pin_ref = self.toggle_pin
        self.schedule = schedule

    def toggle_pin(self, _):
        """Actual callback target run via schedule(). Can be used directly if no allocations. We don't use the timer anyway"""
        self.target.value(not self.target.value())
        # Does this allocate memory? Does this require schedule()?
        print("toggle callback %s" % (str(self.target.value())))

    def irq_callback(self, t):
        """Callback will schedule() an allocated toggle_pin() if schedule() provided at init"""
        if self.schedule:
            self.schedule(self.toggle_pin_ref, 0)
        else:
            self.toggle_pin_ref(0)
