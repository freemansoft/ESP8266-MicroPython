"""
Usage in REPL:

from checksweep import sweep_esp_32
sweep_esp_32()

Depends on classes from this project:
 Servo
 ServoSweep
"""
from servosweep import ServoSweep
from servo import Servo
from machine import Pin, ADC
import time


def sweep_esp_32():
    """
    Exercises ServoSweep.
    Originally written to verify logging of servo position.
    Later extended to log the analog read back position if available.
    """
    adc = ADC(Pin(4))
    # set full attenuation to have full 0-3v range
    adc.atten(adc.ATTN_11DB)

    servo = Servo(Pin(5))
    sweeper = ServoSweep(servo, step_degrees=10)

    while True:
        # this advances the stepper by whatever the current step size is
        sweeper.sweep(None)
        time.sleep(1)
        sweeper.log_pin_adc(adc)
