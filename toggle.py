import machine
import time


def toggle_pin(pin, msec, times):
    """pin: an actual pin construct not number on my ESP8266 was from 2: led or 16:relay"""

    def toggle_pin(p):
        p.value(not p.value())

    # each blink is on/off
    num_left = times * 2
    while num_left > 0:
        toggle_pin(pin)
        time.sleep_ms(msec)
        num_left -= 1
