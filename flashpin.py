# SPDX-FileCopyrightText: 2022 Joe Freeman joe@freemansoft.com
#
# SPDX-License-Identifier: MIT
#
import time


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
