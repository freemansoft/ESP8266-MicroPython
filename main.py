from machine import Pin, Signal, Timer
import micropython


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


def main():

    """lets us test main() without board reset"""
    pin_to_toggle = Pin(2, Pin.OUT)
    flash_pin(pin_to_toggle, 300, 1)
    conn = WIFI(wifi_ssid, wifi_password, hostname)
    ipinfo_sta = conn.do_connect()
    ipinfo_ap = conn.log_ap_state()
    flash_pin(pin_to_toggle, 300, 2)
    print("STA network config:", ipinfo_sta)
    print("AP  network config:", ipinfo_ap)
    flash_pin(pin_to_toggle, 300, 3)

    # http_get_print("http://micropython.org/ks/test.html")

    # import webrepl
    # webrepl.start(password=web_repl_password)

    server = None
    import os

    if os.uname().machine.startswith("ESP32C3"):
        # (sysname='esp32', nodename='esp32', release='1.19.1', version='v1.19.1 on 2022-06-18', machine='ESP32C3 module with ESP32C3')
        # flash 1/sec
        periodic_handler = TogglePin(Pin(2, Pin.OUT), micropython.schedule)
        periodic_operator = PeriodicOperator(
            Timer(2), 500, periodic_handler.irq_callback
        )
        periodic_label = "Flashing LED (2)"

        # dummy up the pins for the SeedStudio Xiao ESP32C3 that I have https://wiki.seeedstudio.com/XIAO_ESP32C3_Getting_Started/
        server = WebServer(
            [
                Signal(Pin(2, Pin.OUT), invert=True),
                Signal(Pin(3, Pin.OUT), invert=False),
            ],
            ["LED (Pin 2)", "RELAY (Pin 3)"],
            [Servo(Pin(4))],
            ["Servo (P 4)"],
            [Pin(i) for i in [2, 3, 4, 5, 6, 7, 8, 9, 10]],
            [periodic_operator],
            [periodic_label],
            "Station:" + str(ipinfo_sta[0]) + "<br/>AP:" + str(ipinfo_ap[0]),
        )
    else:
        # (sysname='esp8266', nodename='esp8266', release='2.2.0-dev(9422289)', version='v1.19.1 on 2022-06-18', machine='ESP module with ESP8266')
        # flash 1/sec
        periodic_handler = TogglePin(Pin(2, Pin.OUT), micropython.schedule)
        periodic_operator = PeriodicOperator(
            Timer(-1), 500, periodic_handler.irq_callback
        )
        periodic_label = "Flashing LED"

        # sweep back and forth
        # periodic_handler = ServoSweep(Servo(Pin(14)), micropython.schedule)
        # periodic_operator = PeriodicOperator(
        #     Timer(-1), 2000, periodic_handler.irq_callback
        # )
        # periodic_label = "Servo Sweep"

        # ESP8266
        server = WebServer(
            [
                Signal(Pin(2, Pin.OUT), invert=True),
                Signal(Pin(16, Pin.OUT), invert=False),
            ],
            ["LED (Pin 2)", "RELAY (Pin 16)"],
            [Servo(Pin(14))],
            ["Servo (P 14)"],
            [Pin(i) for i in [0, 2, 4, 5, 12, 13, 15, 16]],
            [periodic_operator],
            [periodic_label],
            "Station:" + str(ipinfo_sta[0]) + "<br/>AP:" + str(ipinfo_ap[0]),
        )
    server.run_server()


if __name__ == "__main__":
    main()
