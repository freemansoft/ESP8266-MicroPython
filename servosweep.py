class ServoSweep:
    """A sample target class that gets invoked as a timer callback"""

    def __init__(
        self, pin, pin_adc=None, schedule=None, start_angle=0, step_degrees=30
    ):
        """
        ;param pin : i/O pin
        ;param pin_adc: adc pin to log values - really should be a function or remoted
        ;param schedule : if running in IRQ should be micropython.schedule for safe irq handling
        ;param start_angle: servo should be initialized to some angle
        ;param step_degrees: size of each step
        """
        self.target = pin
        self.pin_adc = pin_adc
        # need to allocate the reference prior to using it in a callback
        self.sweep_ref = self.sweep
        self.schedule = schedule
        # This will be wrong if not passed in
        self.target_angle = start_angle
        self.step_degrees = step_degrees
        self.debug_enabled = True

    def sweep(self, _):
        """Actual callback target run via schedule(). Can be used directly if no allocations. We don't use the timer anyway"""
        if self.pin_adc:
            self.log_pin_adc(self.pin_adc)

        new_target = self.target_angle
        if self.target_angle < 180 and self.target_angle + self.step_degrees <= 180:
            new_target = self.target_angle + self.step_degrees
        else:
            new_target = 0
        # Does this allocate memory? Does this require schedule()?
        if self.debug_enabled:
            print("Sweeping to %s" % (str(new_target)))
        self.target.write_angle(new_target)
        self.target_angle = new_target

    def irq_callback(self, t):
        """Callback will schedule() an allocated sweep() if schedule() provided at init"""
        if self.schedule:
            self.schedule(self.sweep_ref, 0)
        else:
            self.sweep_ref(0)

    def log_pin_adc(self, pin_adc):
        # try highest resolution first
        try:
            if self.debug_enabled:
                print("Analog: prev position raw u16: " + str(pin_adc.read_u16()))
        except AttributeError:
            if self.debug_enabled:
                print("Analog prev position raw : " + str(pin_adc.read()))
