# This expects
# sh1106.py and servo.py to be on the pyboard
#
# Usage in the REPL
"""
from checkfreemometer import *
"""

from machine import Pin
import time


def demo_rp2040_led():
    # RP2040 special :-)
    led = Pin.board.LED
    for i in range(0, 10):
        led.value(not led.value())
        time.sleep_ms(300)


def demo_neopixels():
    import neopixel

    # neopixels
    neopixel_pin_num = 16
    num_neopixels = 2
    np = neopixel.NeoPixel(Pin(neopixel_pin_num), num_neopixels)

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
    print("Motor 10000/65000")
    pwm1a.duty_u16(10000)  # out of 65000
    time.sleep(1)
    print("Motor 25000/65000")
    pwm1a.duty_u16(25000)  # out of 65000
    time.sleep(1)
    print("Motor 45000/65000")
    pwm1a.duty_u16(45000)  # out of 65000
    time.sleep(1)
    print("Motor 00000/65000")
    pwm1a.duty_u16(00000)  # out of 65000
    time.sleep(1)
    pwm1a.deinit()
    time.sleep(1)


def demo_servo():
    # Must copy servo.py to /pyboard before running
    from servo import Servo

    # The face servo moter control pin
    servo_pin_num = 22

    servo = Servo(Pin(servo_pin_num, Pin.OUT))
    print("servo 0")
    servo.write_angle(0)
    time.sleep(1)
    print("Servo 80")
    servo.write_angle(80)
    time.sleep(1)
    print("servo 160")
    servo.write_angle(160)
    time.sleep(1)
    servo.write_us(0)


def demo_sh1106():
    # copy sh1106 to /pyboard
    # https://github.com/scy/SH1106/blob/master/sh1106.py
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
    display_sh1106.text("Goodby Cruel World!", 0, 10, 1)
    display_sh1106.show()
    time.sleep(2)
    display_sh1106.fill(0)  # clears the display
    display_sh1106.show()
