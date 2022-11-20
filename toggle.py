import machine


def toggle_pin(pinNum, msec, times):
    """2: led or 16:relay"""

    pin = machine.Pin(pinNum, machine.Pin.OUT)

    def toggle_pin(p):
        p.value(not p.value())

    import time

    # each blink is on/off
    num_left = times * 2
    while num_left > 0:
        toggle_pin(pin)
        time.sleep_ms(msec)
        num_left -= 1
