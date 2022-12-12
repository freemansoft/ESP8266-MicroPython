import machine
from config import wifi_ssid, wifi_password, hostname
from config import web_repl_password

""" copies of the variables"""
from connectwifi import WIFI
from webserver import WebServer
from toggle import toggle_pin
from httpget import http_get_print

from servo import Servo


def main():
    """lets us test main() without board reset"""
    toggle_pin(2, 200, 2)
    conn = WIFI(wifi_ssid, wifi_password, hostname)
    conn.do_connect()
    # http_get_print("http://micropython.org/ks/test.html")
    toggle_pin(2, 200, 2)

    # import webrepl
    # webrepl.start(password=web_repl_password)

    # import time

    # servo = Servo(machine.Pin(14))
    # servo.write_angle(0)
    # time.sleep_ms(2000)
    # servo.write_angle(180)

    server = WebServer(
        [machine.Pin(2, machine.Pin.OUT), machine.Pin(16, machine.Pin.OUT)],
        ["LED (Pin 2)", "RELAY (Pin 16)"],
        [False, True],
        [machine.Pin(i) for i in [0, 2, 4, 5, 12, 13, 15, 16]],
        [Servo(machine.Pin(14))],
        ["Servo (P 14)"],
    )
    server.run_server()


if __name__ == "__main__":
    main()
