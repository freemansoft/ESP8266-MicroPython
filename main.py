from machine import Pin, Signal, Timer
from config import wifi_ssid, wifi_password, hostname
from config import web_repl_password

""" copies of the variables"""
from connectwifi import WIFI
from webserver import WebServer
from flashpin import flash_pin
from toggle import TogglePin
from servo import Servo
from httpget import http_get_print
from periodicoperator import PeriodicOperator

import micropython

# timer/interrupt exception buffer
micropython.alloc_emergency_exception_buf(100)


def main():

    # basically flashing every 1 seconds
    a_periodic_handler = TogglePin(Pin(2, Pin.OUT))
    a_periodic_operator = PeriodicOperator(
        Timer(-1), 500, a_periodic_handler.toggle_pin_callback
    )

    """lets us test main() without board reset"""
    pin_to_toggle = Pin(2, Pin.OUT)
    flash_pin(pin_to_toggle, 300, 3)
    conn = WIFI(wifi_ssid, wifi_password, hostname)
    ipinfo_sta = conn.do_connect()
    ipinfo_ap = conn.log_ap_state()
    flash_pin(pin_to_toggle, 300, 4)
    print("STA network config:", ipinfo_sta)
    print("AP  network config:", ipinfo_ap)

    # http_get_print("http://micropython.org/ks/test.html")

    # import webrepl
    # webrepl.start(password=web_repl_password)

    server = WebServer(
        [
            Signal(Pin(2, Pin.OUT), invert=True),
            Signal(Pin(16, Pin.OUT), invert=False),
        ],
        ["LED (Pin 2)", "RELAY (Pin 16)"],
        [Servo(Pin(14))],
        ["Servo (P 14)"],
        [Pin(i) for i in [0, 2, 4, 5, 12, 13, 15, 16]],
        [a_periodic_operator],
        ["Flash LED"],
        "Station:" + str(ipinfo_sta[0]) + "<br/>AP:" + str(ipinfo_ap[0]),
    )
    server.run_server()


if __name__ == "__main__":
    main()
