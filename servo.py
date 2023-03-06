# SPDX-FileCopyrightText: 2022 Joe Freeman joe@freemansoft.com
#
# SPDX-License-Identifier: MIT
#
from machine import PWM
import math

# copied from https://github.com/pvanallen/esp32-getstarted/blob/master/examples/servo.py
# originally by Radomir Dopieralski http://sheep.art.pl
# from https://bitbucket.org/thesheep/micropython-servo


class Servo:
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
        self.debug_enabled = True
        self.pin = pin
        self.min_us = min_us
        self.max_us = max_us
        self.us = min_us  # set the current usec to the minimum
        self.degrees = 0  # match the angle to the minimum
        self.freq = freq
        self.max_angle = max_angle
        self.pqm = None
        try:
            self.pwm = PWM(pin, freq=freq, duty=0)
        except TypeError:
            # added to support rp2 which has 16 bit pwm
            self.pwm = PWM(pin)
            self.pwm.freq(freq)
            self.pwm.duty_u16(0)
        self.write_angle(0)

    def __str__(self) -> str:
        return "%s" % (self.pin)

    def write_us(self, us):
        """Set the signal to be ``us`` microseconds long. Zero disables it."""
        if us == 0:
            try:
                self.pwm.duty(0)
            except AttributeError:
                self.pwm.duty_u16(0)
            self.us = 0
            self.degrees = -1
        else:
            us = min(self.max_us, max(self.min_us, us))
            try:
                # the duty method takes the duty portion over 1024 so a portion of 1024
                # convert usec to duty cycle knowing  frequency in this case 50Hz results in 20ms period
                duty = us * 1024 * self.freq // 1000000
                self.pwm.duty(duty)
                if self.debug_enabled:
                    print("Servo: converted us:", us, " to duty:", duty)
            except AttributeError:
                # from https://forums.raspberrypi.com/viewtopic.php?t=307218
                # the rp2 rp2040 is 16 bit. The duty cycle over 0-65535
                # Total PWM period is 20ms or 20,000usec - 50Hz
                duty = us * 65536 * self.freq // 1000000
                self.pwm.duty_u16(duty)
                if self.debug_enabled:
                    print("Servo request us:", us, " set duty_u16 to:", duty)
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
        if self.debug_enabled:
            print("Servo: degrees:", degrees, " equvalent to usec:", us)
        self.write_us(us)
