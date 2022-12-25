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

    # flash 1/sec
    periodic_handler = TogglePin(Pin(2, Pin.OUT), micropython.schedule)
    periodic_operator = PeriodicOperator(
        Timer(-1), 500, periodic_handler.toggle_pin_callback
    )
    periodic_label = "Flashing LED"

    # sweep back and forth
    # periodic_handler = ServoSweep(Servo(Pin(14)), micropython.schedule)
    # periodic_operator = PeriodicOperator(
    #     Timer(-1), 2000, periodic_handler.sweep_callback
    # )
    # periodic_label = "Servo Sweep"

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
