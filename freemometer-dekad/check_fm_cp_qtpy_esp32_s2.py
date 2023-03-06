# SPDX-FileCopyrightText: 2022 Joe Freeman joe@freemansoft.com
#
# SPDX-License-Identifier: MIT
#
# CircuitPython
#
# This expects that adafruit CircuitPython libs
# have been installed in the board's lib directory
#
# Usage in the REPL
"""
import check_fm_cp_qtpy_esp32_s2
from check_fm_cp_qtpy_esp32_s2 import *
"""

import board
import time
import neopixel
from adafruit_motor import servo
import pwmio
from digitalio import DigitalInOut, Direction

board_pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)

# neopixel strip
neopixel_pin = board.A3
num_neopixels = 8
neopixel_bpp = 4
neopixel_strip = neopixel.NeoPixel(neopixel_pin, num_neopixels, bpp=neopixel_bpp)

# The face servo moter control pin
servo_pin = board.A2
servo_pwm = pwmio.PWMOut(servo_pin, duty_cycle=2**15, frequency=50)
# The servo in one of mine has a min of 800
servo = servo.Servo(servo_pwm, min_pulse=800)
servo.angle = 0

# We could have grounded one of the DRV8833 ineopixel_striputs but instead hook this up as if it is a reversable motor
motor1b = DigitalInOut(board.A1)
motor1b.direction = Direction.OUTPUT

# lets try motor speed control with PWM
pwm1a = pwmio.PWMOut(board.A0, frequency=10000, variable_frequency=True)


def verify_board_neopixel():
    import time

    for i in range(1, 10):
        board_pixel.fill((10 * i, 10 * i, 10 * i))
        time.sleep(0.5)
    board_pixel.fill((0, 0, 0))


def verify_neopixels_white_rgbw():
    """This is currently set up for a RGBW Neopixel"""
    import time

    for j in range(num_neopixels):
        neopixel_strip[j] = (0, 0, 0, 20)
    neopixel_strip.write()
    time.sleep(1)
    for j in range(num_neopixels):
        neopixel_strip[j] = (0, 0, 0, 60)
    neopixel_strip.write()
    time.sleep(1)
    for j in range(num_neopixels):
        neopixel_strip[j] = (0, 0, 0, 180)
    neopixel_strip.write()
    time.sleep(1)
    for j in range(num_neopixels):
        neopixel_strip[j] = (0, 0, 0, 250)
    neopixel_strip.write()
    time.sleep(1)
    neopixel_strip.fill((0, 0, 0, 0))
    neopixel_strip.write()


def verify_neopixels_rgbw():
    """This is currently set up for a RGBW Neopixel"""
    import time

    print("show some pretty colors")
    # fade in/out
    for i in range(0, 4 * 256, 4):
        # set all pixels
        for j in range(num_neopixels):
            if (i // 256) % 2 == 0:
                val = i & 0xFF
            else:
                val = 255 - (i & 0xFF)
            neopixel_strip[j] = (val, 0, 255 - val, 0)
        neopixel_strip.write()
        time.sleep(0.010)

    # clear
    neopixel_strip.fill((0, 0, 0, 0))
    time.sleep(1)


def verify_motor():
    import time

    print("Motor (pwm) 10000/65000")
    pwm1a.duty_cycle = 10000  # out of 65000
    time.sleep(1)
    print("Motor (pwm) 25000/65000")
    pwm1a.duty_cycle = 25000  # out of 65000
    time.sleep(1)
    print("Motor (pwm) 45000/65000")
    pwm1a.duty_cycle = 45000  # out of 65000
    time.sleep(1)
    print("Motor (pwm) 60000/65000")
    pwm1a.duty_cycle = 60000  # out of 65000
    time.sleep(1)
    print("Motor (pwm) 00000/65000")
    pwm1a.duty_cycle = 00000  # out of 65000
    time.sleep(1)
    # pwm1a.deinit()
    # motor1b.deinit()
    # time.sleep(1)


def verify_servo():
    print("servo 0")
    servo.angle = 0
    time.sleep(1)
    print("Servo 80")
    servo.angle = 80
    time.sleep(1)
    print("servo 160")
    servo.angle = 160
    time.sleep(1)
    print("servo 0")
    servo.angle = 0
    time.sleep(1)
