from machine import Pin, Signal, Timer, reset_cause
import machine
import micropython
import os

from config import wifi_ssid, wifi_password, hostname
from config import web_repl_password

""" copies of the variables"""
from connectwifi import WIFI
from webserver import WebServer
from flashpin import flash_pin
from togglepin import TogglePin
from servosweep import ServoSweep
from servo import Servo
from httpget import http_get_print
from periodicoperator import PeriodicOperator

# timer/interrupt exception buffer
micropython.alloc_emergency_exception_buf(100)

# os.uname()
# (sysname='esp32', nodename='esp32', release='1.19.1', version='v1.19.1 on 2022-06-18', machine='ESP32C3 module with ESP32C3')
# (sysname='rp2', nodename='rp2', release='1.19.1', version='v1.19.1-782-g699477d12 on 2022-12-20 (GNU 12.1.0 MinSizeRel)', machine='Raspberry Pi Pico W with RP2040')
# (sysname='esp8266', nodename='esp8266', release='2.2.0-dev(9422289)', version='v1.19.1 on 2022-06-18', machine='ESP module with ESP8266')


def get_pins():
    """
    lists of pins whose status can be displayed
    """
    if os.uname().sysname == "rp2":
        # rp2040
        return [
            Pin(i)
            for i in [
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15,
                16,
                17,
                18,
                19,
                20,
                21,
                22,
                26,
                27,
                28,
            ]
        ]
    elif os.uname().machine.startswith("ESP32C3"):
        # Seeed Studio Xiao
        return [Pin(i) for i in [2, 3, 4, 5, 6, 7, 8, 9, 10]]
    elif os.uname().sysname == "esp8266":
        # linknode R1
        return [Pin(i) for i in [0, 2, 4, 5, 12, 13, 15, 16]]
    else:
        return [Pin(i) for i in [2, 3, 4, 5]]


def get_outs():
    """
    List of output pins that can be controlled.
    """
    if os.uname().sysname == "rp2":
        # rp2040
        return (
            [
                Signal(Pin(2, Pin.OUT), invert=True),
                Signal(Pin(3, Pin.OUT), invert=False),
                # Pico W on board LED connected to pin on wireless chip not to GPIO
                machine.Pin("LED", machine.Pin.OUT),
            ],
            ["LED (Pin 2)", "RELAY (Pin 3)", "Onboard LED"],
        )
    elif os.uname().machine.startswith("ESP32C3"):
        # Seeed Studio Xiao
        return (
            [
                Signal(Pin(2, Pin.OUT), invert=True),
                Signal(Pin(3, Pin.OUT), invert=False),
            ],
            ["LED (Pin 2)", "RELAY (Pin 3)"],
        )
    elif os.uname().sysname == "esp8266":
        # linknode R1
        return (
            [
                Signal(Pin(2, Pin.OUT), invert=True),
                Signal(Pin(16, Pin.OUT), invert=False),
            ],
            ["Onboard LED", "RELAY (Pin 16)"],
        )
    else:
        return ([], [])


def get_periodics():
    """
    This exists because of the mix of Micropython hardware and software timer support on different boards
    Servos moved to pin 5 because adc is 0-4 on ESP32C3
    LED is on pin 2 because that is where onboard it is on ESP8266
    """
    if os.uname().machine.startswith("ESP32C3"):
        # hardware timers
        # flash 1/sec
        periodic_handler_1 = TogglePin(Pin(2, Pin.OUT), micropython.schedule)
        periodic_operator_1 = PeriodicOperator(
            Timer(2), 500, periodic_handler_1.irq_callback
        )
        periodic_label_1 = "Flashing LED (2)"
        # sweep back and forth
        # support feedback servos with full 0-3.3v range
        adc = machine.ADC(Pin(4))
        adc.atten(adc.ATTN_11DB)
        # Servo is on pin 5 because we need pin 4 for adc
        periodic_handler_2 = ServoSweep(
            Servo(Pin(5)), pin_adc=adc, schedule=micropython.schedule
        )
        periodic_operator_2 = PeriodicOperator(
            Timer(0), 2000, periodic_handler_2.irq_callback
        )
        periodic_label_2 = "Servo Sweep (5)"
        return (
            [periodic_operator_1, periodic_operator_2],
            [periodic_label_1, periodic_label_2],
        )
    elif os.uname().sysname == "rp2" or os.uname().sysname == "esp8266":
        # rp2 has only software timers as of 2022/12
        # esp8266 has one software timer
        # docs say do use '-1'
        # flash 1/sec
        periodic_handler_1 = TogglePin(Pin(2, Pin.OUT), micropython.schedule)
        periodic_operator_1 = PeriodicOperator(
            Timer(-1), 500, periodic_handler_1.irq_callback
        )
        periodic_label_1 = "Flashing LED (2)"

        # sweep back and forth
        periodic_handler_2 = ServoSweep(Servo(Pin(5)), schedule=micropython.schedule)
        periodic_operator_2 = PeriodicOperator(
            Timer(-1), 2000, periodic_handler_2.irq_callback
        )
        periodic_label_2 = "Servo Sweep (5)"
        return (
            [periodic_operator_1, periodic_operator_2],
            [periodic_label_1, periodic_label_2],
        )
    else:
        return ([], [])


def get_servos():
    """
    lists of servo pins and servo labels
    should be empty if no servos
    """
    return ([Servo(Pin(5))], ["Servo (P5 : 600-2400)"])


def onboard_led():
    if os.uname().machine.startswith("ESP32C3"):
        # there is no onboard default on my ESP32C3
        return Pin(2, Pin.OUT)
    elif os.uname().sysname == "rp2":
        # no easy way to figure out which one
        # Pico no W
        # machine.Pin(25, machine.Pin.OUT)
        # Pico W
        return machine.Pin("LED", machine.Pin.OUT)
    elif os.uname().sysname == "esp8266":
        return Pin(2, Pin.OUT)
    else:
        # there is no onboard by default so pick a random number.
        return Pin(2, Pin.OUT)


def main():
    print("Reset cause is ", reset_cause())

    """lets us test main() without board reset"""
    pin_to_toggle = onboard_led()
    flash_pin(pin_to_toggle, 300, 2)
    conn = WIFI(wifi_ssid, wifi_password, hostname)
    ipinfo_sta = conn.do_connect()
    ipinfo_ap = conn.log_ap_state()
    flash_pin(pin_to_toggle, 300, 4)
    print("STA network config:", ipinfo_sta)
    print("AP  network config:", ipinfo_ap)
    flash_pin(pin_to_toggle, 300, 6)

    # http_get_print("http://micropython.org/ks/test.html")

    # import webrepl
    # webrepl.start(password=web_repl_password)

    server = None

    if (
        os.uname().machine.startswith("ESP32C3")
        or os.uname().sysname == "rp2"
        or os.uname().sysname == "esp8266"
    ):
        (periodic_operators, periodic_labels) = get_periodics()
        (out_pins, out_labels) = get_outs()
        (servo_pins, servo_labels) = get_servos()
        # dummy up the pins for the SeedStudio Xiao ESP32C3 that I have https://wiki.seeedstudio.com/XIAO_ESP32C3_Getting_Started/
        server = WebServer(
            out_pins,
            out_labels,
            servo_pins,
            servo_labels,
            get_pins(),
            periodic_operators,
            periodic_labels,
            "Demo Page: " + os.uname().sysname,
            "Station:" + str(ipinfo_sta[0]) + "<br/>AP:" + str(ipinfo_ap[0]),
        )
    else:
        print("************* unrecognized board ===>> " + str(os.uname()))
    server.run_server()


if __name__ == "__main__":
    main()
