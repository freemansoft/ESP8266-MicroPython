# MICROPYTHON
#
# This expects
# sh1106.py and servo.py to be on the pyboard
#
# Usage in the REPL
"""
from check_fm_mp_pico import *
"""

from machine import Pin
import time


def demo_rp2040_led():
    # RP2040 special :-)
    led = Pin.board.LED
    for i in range(0, 10):
        led.value(not led.value())
        time.sleep_ms(300)


def verify_neopixels_white_rgbw():
    """This is currently set up for a RGBW Neopixel"""
    import neopixel

    # neopixels
    neopixel_pin_num = 16
    num_neopixels = 8
    neopixel_bpp = 4
    np = neopixel.NeoPixel(Pin(neopixel_pin_num), num_neopixels, bpp=neopixel_bpp)
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
    for j in range(num_neopixels):
        np[j] = (0, 0, 0, 0)
    np.write()


def verify_neopixels_white_rgb():
    """This is currently set up for a RGB Neopixel"""
    import neopixel

    # neopixels
    neopixel_pin_num = 16
    num_neopixels = 8
    neopixel_bpp = 3
    np = neopixel.NeoPixel(Pin(neopixel_pin_num), num_neopixels, bpp=neopixel_bpp)
    for j in range(num_neopixels):
        np[j] = (20, 20, 20)
    np.write()
    time.sleep(1)
    for j in range(num_neopixels):
        np[j] = (64, 64, 64)
    np.write()
    time.sleep(1)
    for j in range(num_neopixels):
        np[j] = (180, 180, 180)
    np.write()
    time.sleep(1)


def demo_neopixels_rgbw():
    """This is currently set up for a RGBW Neopixel"""
    import neopixel

    # neopixels
    neopixel_pin_num = 16
    num_neopixels = 8
    neopixel_bpp = 4
    np = neopixel.NeoPixel(Pin(neopixel_pin_num), num_neopixels, bpp=neopixel_bpp)

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
        time.sleep_ms(10)

    # clear
    for i in range(num_neopixels):
        np[i] = (0, 0, 0, 0)

    np.write()
    time.sleep(1)


def demo_neopixels_rgb():
    """This is currently set up for a RGBW Neopixel"""
    import neopixel

    # neopixels
    neopixel_pin_num = 16
    num_neopixels = 8
    neopixel_bpp = 3
    np = neopixel.NeoPixel(Pin(neopixel_pin_num), num_neopixels, bpp=neopixel_bpp)

    print("show some pretty colors")
    # fade in/out
    for i in range(0, 4 * 256, 4):
        # set all pixels
        for j in range(num_neopixels):
            if (i // 256) % 2 == 0:
                val = i & 0xFF
            else:
                val = 255 - (i & 0xFF)
            np[j] = (val, 0, 255 - val)
        np.write()
        time.sleep_ms(10)

    # clear
    for i in range(num_neopixels):
        np[i] = (0, 0, 0)

    np.write()
    time.sleep(1)


def demo_motor():
    from machine import PWM

    # DEKAD alarm bell motor
    motor_pin_1_num = 18
    motor_pin_2_num = 19

    # We could have grounded one of the DRV8833 inputs but instead hook this up as if it is a reversable motor
    motor1a = Pin(motor_pin_1_num, Pin.OUT)
    motor1b = Pin(motor_pin_2_num, Pin.OUT)

    # go motor go - they need to be opposite values
    print("Motor like a bat out of hell")
    motor1a.value(0)
    motor1b.value(1)
    time.sleep(1)

    # stop motor stop
    print("Motor off")
    motor1a.value(0)
    motor1b.value(0)
    time.sleep(1)

    # lets try motor speed control with PWM
    pwm1a = PWM(motor1b)
    pwm1a.freq(10000)
    print("Motor (pwm) 10000/65000")
    pwm1a.duty_u16(10000)  # out of 65000
    time.sleep(1)
    print("Motor (pwm) 25000/65000")
    pwm1a.duty_u16(25000)  # out of 65000
    time.sleep(1)
    print("Motor (pwm) 45000/65000")
    pwm1a.duty_u16(45000)  # out of 65000
    time.sleep(1)
    print("Motor (pwm) 00000/65000")
    pwm1a.duty_u16(00000)  # out of 65000
    time.sleep(1)
    pwm1a.deinit()
    time.sleep(1)


def demo_servo():
    # Must copy servo.py to /pyboard before running
    from servo import Servo

    # The face servo moter control pin
    servo_pin_num = 22
    # The servo in one of mine has a min of 800
    servo = Servo(Pin(servo_pin_num, Pin.OUT), min_us=800)
    print("servo 0")
    servo.write_angle(0)
    time.sleep(1)
    print("Servo 80")
    servo.write_angle(80)
    time.sleep(1)
    print("servo 160")
    servo.write_angle(160)
    time.sleep(1)
    print("servo 0")
    servo.write_angle(0)
    time.sleep(1)


def demo_sh1106():
    # copy sh1106 to /pyboard
    # https://github.com/robert-hh/SH1106
    # https://docs.micropython.org/en/latest/esp8266/tutorial/ssd1306.html display commands
    from machine import SPI
    import sh1106

    spi1_sck_clk = Pin(14)
    spi1_tx_mosi = Pin(15)
    spi1_rx_miso_dc = Pin(12)
    spi1_csn_cs = Pin(13)

    oled_spi = SPI(1, sck=spi1_sck_clk, mosi=spi1_tx_mosi, miso=spi1_rx_miso_dc)

    display_sh1106 = sh1106.SH1106_SPI(
        128, 64, oled_spi, dc=spi1_rx_miso_dc, cs=spi1_csn_cs
    )
    display_sh1106.init_display()  # clears the display
    display_sh1106.invert(1)
    time.sleep(1)
    display_sh1106.invert(0)
    time.sleep(1)

    display_sh1106.text("Hello World!", 0, 0, 1)
    # this text will be truncated -- appropriate I think for a goodbye message
    display_sh1106.text("So long. Thanks", 0, 10, 1)
    display_sh1106.text("Thanks for the ", 0, 20, 1)
    display_sh1106.text("fish", 0, 30, 1)
    display_sh1106.show()
    time.sleep(2)
    display_sh1106.fill(0)  # clears the display
    display_sh1106.show()
