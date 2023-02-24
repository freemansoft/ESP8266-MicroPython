# CircuitPython
#
# This expects
# sh1106.py and servo.py to be on the pyboard
#
# Usage in the REPL
"""
import check_fm_cp_qtpy_esp32_s2
from check_fm_cp_qtpy_esp32_s2 import *
"""

import board
import time


def demo_board_neopixel():
    import time
    import neopixel

    board_pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)

    for i in range(1, 10):
        board_pixel.fill((10 * i, 10 * i, 10 * i))
        time.sleep(0.5)
    board_pixel.fill((0, 0, 0))


def verify_neopixels_white_rgbw():
    import time
    import neopixel
    import board

    """This is currently set up for a RGBW Neopixel"""

    # neopixels
    neopixel_pin = board.A3
    num_neopixels = 8
    neopixel_bpp = 4

    np = neopixel.NeoPixel(neopixel_pin, num_neopixels, bpp=neopixel_bpp)
    for j in range(num_neopixels):
        np[j] = (0, 0, 0, 20)
    np.write()
    time.sleep(1)
    for j in range(num_neopixels):
        np[j] = (0, 0, 0, 60)
    np.write()
    time.sleep(1)
    for j in range(num_neopixels):
        np[j] = (0, 0, 0, 180)
    np.write()
    time.sleep(1)
    for j in range(num_neopixels):
        np[j] = (0, 0, 0, 250)
    np.write()
    time.sleep(1)
    np.fill((0, 0, 0, 0))
    np.write()


def demo_neopixels_rgbw():
    """This is currently set up for a RGBW Neopixel"""
    import time
    import neopixel
    import board

    # neopixels
    neopixel_pin = board.A3
    num_neopixels = 8
    neopixel_bpp = 4

    np = neopixel.NeoPixel(neopixel_pin, num_neopixels, bpp=neopixel_bpp)

    print("show some pretty colors")
    # fade in/out
    for i in range(0, 4 * 256, 4):
        # set all pixels
        for j in range(num_neopixels):
            if (i // 256) % 2 == 0:
                val = i & 0xFF
            else:
                val = 255 - (i & 0xFF)
            np[j] = (val, 0, 255 - val, 0)
        np.write()
        time.sleep(0.010)

    # clear
    np.fill((0, 0, 0, 0))
    time.sleep(1)


def demo_motor():
    import board
    import time
    import pwmio
    from digitalio import DigitalInOut, Direction, Pull

    # We could have grounded one of the DRV8833 inputs but instead hook this up as if it is a reversable motor
    motor1a = DigitalInOut(board.A0)
    motor1a.direction = Direction.OUTPUT
    motor1b = DigitalInOut(board.A1)
    motor1b.direction = Direction.OUTPUT

    # go motor go - they need to be opposite values
    print("Motor like a bat out of hell")
    motor1a.value = False
    motor1b.value = True
    time.sleep(1)

    # stop motor stop
    print("Motor off")
    motor1a.value = False
    motor1b.value = False
    time.sleep(1)

    # lets try motor speed control with PWM
    motor1a.deinit()
    pwm1a = pwmio.PWMOut(board.A0, frequency=10000, variable_frequency=True)
    print("Motor (pwm) 10000/65000")
    pwm1a.duty_cycle = 10000  # out of 65000
    time.sleep(1)
    print("Motor (pwm) 25000/65000")
    pwm1a.duty_cycle = 25000  # out of 65000
    time.sleep(1)
    print("Motor (pwm) 45000/65000")
    pwm1a.duty_cycle = 45000  # out of 65000
    time.sleep(1)
    print("Motor (pwm) 00000/65000")
    pwm1a.duty_cycle = 00000  # out of 65000
    time.sleep(1)
    pwm1a.deinit()
    # if we don't have this the pins may be in loud alarm state
    # of course this ties up A0 again
    motor1a = DigitalInOut(board.A0)
    motor1a.direction = Direction.OUTPUT

    time.sleep(1)


def demo_servo():
    from adafruit_motor import servo
    import pwmio
    import time

    # The face servo moter control pin
    servo_pin = board.A2
    servo_pwm = pwmio.PWMOut(servo_pin, duty_cycle=2**15, frequency=50)
    # The servo in one of mine has a min of 800
    servo = servo.Servo(servo_pwm, min_pulse=800)
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
