# Micropython
# This expects
# sh1106.py and servo.py to be on the pyboard
#
# Usage in the REPL
"""
from check_fm_mp_tiny2040 import *
"""

from machine import Pin
import time


# The ESP32.C3 seems to start with the pins high which runs the bell
def quiet_motor():
    Pin(6, Pin.OUT).value(0)
    Pin(7, Pin.OUT).value(0)


def demo_motor():
    from machine import PWM

    # DEKAD alarm bell motor
    motor_pin_1_num = 2
    motor_pin_2_num = 3

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
    quiet_motor()
    time.sleep(1)


def demo_servo():
    # Must copy servo.py to /pyboard before running
    from servo import Servo

    # The face servo moter control pin
    servo_pin_num = 29

    servo = Servo(Pin(servo_pin_num, Pin.OUT), min_us=1000)
    print("servo 0")
    servo.write_angle(0)
    time.sleep(1)
    print("Servo 80")
    servo.write_angle(80)
    time.sleep(1)
    print("servo 170")
    servo.write_angle(170)
    time.sleep(1)
    servo.write_us(0)


def demo_sh1106():
    # copy sh1106 to /pyboard
    # https://github.com/robert-hh/SH1106
    # https://docs.micropython.org/en/latest/esp8266/tutorial/ssd1306.html display commands
    from machine import SPI, SoftSPI
    import sh1106

    spi1_sck_clk = Pin(6)
    spi1_tx_mosi = Pin(7)
    spi1_rx_miso_dc = Pin(4)
    spi1_csn_cs = Pin(5)

    # two hardware SPI to specific pins
    oled_spi = SPI(0, sck=spi1_sck_clk, mosi=spi1_tx_mosi, miso=spi1_rx_miso_dc)
    print(oled_spi)

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
