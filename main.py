from machine import Pin, Signal
from config import wifi_ssid, wifi_password, hostname
from config import web_repl_password

""" copies of the variables"""
from connectwifi import WIFI
from webserver import WebServer
from toggle import toggle_pin
from servo import Servo
from httpget import http_get_print


def main():
    """lets us test main() without board reset"""
    pin_to_toggle = Pin(2, Pin.OUT)
    toggle_pin(pin_to_toggle, 300, 3)
    conn = WIFI(wifi_ssid, wifi_password, hostname)
    ipinfo_sta = conn.do_connect()
    ipinfo_ap = conn.log_ap_state()
    toggle_pin(pin_to_toggle, 300, 4)
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
        "Station:" + str(ipinfo_sta[0]) + "<br/>AP:" + str(ipinfo_ap[0]),
    )
    server.run_server()


if __name__ == "__main__":
    main()
