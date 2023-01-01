import math

# copied from https://github.com/pvanallen/esp32-getstarted/blob/master/examples/servo.py
# originally by Radomir Dopieralski http://sheep.art.pl
# from https://bitbucket.org/thesheep/micropython-servo


class FakeServo:
    """
    A simple class for controlling hobby servos.

    Args:
        pin (machine.Pin): The pin where servo is connected. Must support PWM.
        freq (int): The frequency of the signal, in hertz.
        min_us (int): The minimum signal length supported by the servo.
        max_us (int): The maximum signal length supported by the servo.
        angle (int): The angle between the minimum and maximum positions.

    """

    def __init__(self, pin, freq=50, min_us=600, max_us=2400, max_angle=180):
        """
        resets the servo back to the home position
        ;param max_angle: maximum angle - min_angle will be 0
        """
        self.pin = pin
        self.min_us = min_us
        self.max_us = max_us
        self.us = min_us  # set the current usec to the minimum
        self.degrees = 0  # match the angle to the minimum
        self.freq = freq
        self.max_angle = max_angle
        # self.pwm = PWM(pin, freq=freq, duty=0)
        self.write_angle(0)

    def __str__(self) -> str:
        return "%s" % (self.pin)

    def write_us(self, us):
        """Set the signal to be ``us`` microseconds long. Zero disables it."""
        if us == 0:
            # self.pwm.duty(0)
            self.us = 0
            self.degrees = -1
        else:
            us = min(self.max_us, max(self.min_us, us))
            duty = us * 1024 * self.freq // 1000000
            # self.pwm.duty(duty)
            self.us = us
            # self.degrees=  TODO back into

    def write_angle(self, degrees=None, radians=None):
        """Move to the specified angle in ``degrees`` or ``radians``."""
        if degrees is None:
            degrees = math.degrees(radians)
        degrees = degrees % 360
        total_range = self.max_us - self.min_us
        us = self.min_us + total_range * degrees // self.max_angle
        # minor hack because we should calculate the degrees from microsecends in write_us()
        self.degrees = degrees
        self.write_us(us)
