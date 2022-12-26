class ServoSweep:
    """A sample target class that gets invoked as a timer callback"""

    def __init__(self, pin, schedule=None, startangle=0):
        """
        ;param pin : i/O pin
        ;param schedule : if running in IRQ should be micropython.schedule for safe irq handling
        ;param startangle: servo should be initialized to some angle
        """
        self.target = pin
        # need to allocate the reference prior to using it in a callback
        self.sweep_ref = self.sweep
        self.schedule = schedule
        # This will be wrong if not passed in
        self.targetangle = startangle

    def sweep(self, _):
        """Actual callback target run via schedule(). Can be used directly if no allocations. We don't use the timer anyway"""
        if self.targetangle == 0:
            self.target.write_angle(180)
            self.targetangle = 180
        else:
            self.target.write_angle(0)
            self.targetangle = 0
        # Does this allocate memory? Does this require schedule()?
        print("sweeping to %s" % (str(self.targetangle)))

    def irq_callback(self, t):
        """Callback will schedule() an allocated sweep() if schedule() provided at init"""
        if self.schedule:
            self.schedule(self.sweep_ref, 0)
        else:
            self.sweep_ref(0)