class ServoSweep:
    """A sample target class that gets invoked as a timer callback"""

    def __init__(self, pin, pin_adc=None, schedule=None, startangle=0):
        """
        ;param pin : i/O pin
        ;param schedule : if running in IRQ should be micropython.schedule for safe irq handling
        ;param startangle: servo should be initialized to some angle
        """
        self.target = pin
        self.pin_adc = pin_adc
        # need to allocate the reference prior to using it in a callback
        self.sweep_ref = self.sweep
        self.schedule = schedule
        # This will be wrong if not passed in
        self.targetangle = startangle

    def sweep(self, _):
        """Actual callback target run via schedule(). Can be used directly if no allocations. We don't use the timer anyway"""
        if self.pin_adc:
            # try highest resolution first
            try:
                print("Analog: prev position raw u16: " + str(self.pin_adc.read_u16()))
            except AttributeError:
                print("Analog prev position raw : " + str(self.pin_adc.read()))

        new_target = self.targetangle
        if self.targetangle < 180:
            new_target = self.targetangle + 30
        else:
            new_target = 0
        # Does this allocate memory? Does this require schedule()?
        print("Sweeping to %s" % (str(new_target)))
        self.target.write_angle(new_target)
        self.targetangle = new_target

    def irq_callback(self, t):
        """Callback will schedule() an allocated sweep() if schedule() provided at init"""
        if self.schedule:
            self.schedule(self.sweep_ref, 0)
        else:
            self.sweep_ref(0)
