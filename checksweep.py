"""
Usage in REPL:

from checksweep import sweep_esp_32
sweep_esp_32(5,4)

or if you don't have feedback servos
sweep_esp_32(5)

Depends on classes from this project:
 Servo
 ServoSweep
"""
from servosweep import ServoSweep
from servo import Servo
from machine import Pin, ADC
import time


def sweep_esp_32(servo_pin_num, adc_pin_num=None):
    """
    Exercises ServoSweep.
    Originally written to verify logging of servo position.
    Later extended to log the analog read back position if available.
    """
    if adc_pin_num:
        adc = ADC(Pin(adc_pin_num))
        # set full attenuation to have full 0-3v range
        adc.atten(adc.ATTN_11DB)

    servo = Servo(Pin(servo_pin_num))
    sweeper = ServoSweep(servo, step_degrees=10)

    while True:
        # this advances the stepper by whatever the current step size is
        sweeper.sweep(None)
        time.sleep(1)
        if adc_pin_num:
            sweeper.log_pin_adc(adc)
