import time
from machine import Pin


def flash_pin(pin, msec, times):
    """pin: an actual pin construct not number on my ESP8266 was from 2: led or 16:relay"""

    def flash_pin(p):
        p.value(not p.value())

    # each blink is on/off
    num_left = times * 2
    while num_left > 0:
        flash_pin(pin)
        time.sleep_ms(msec)
        num_left -= 1


periodic_target = Pin(2, Pin.OUT)


def toggle_pin_callback(t):
    """sutable for call from a timer event"""
    global periodic_target
    periodic_target.value(not periodic_target.value())
    # print("timer toggle callback %s" % (str(periodic_target.value())))
