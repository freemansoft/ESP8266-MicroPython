from config import wifi_ssid, wifi_password, hostname
from config import web_repl_password
""" copies of the variables"""
from connectwifi import WIFI
from webserver import WebServer
from toggle import toggle_pin
from httpget import http_get_print


def main():
    """lets us test main() without board reset"""
    toggle_pin(2, 200, 2)
    conn = WIFI(wifi_ssid, wifi_password, hostname)
    conn.do_connect()
    # http_get_print("http://micropython.org/ks/test.html")
    toggle_pin(2, 200, 2)

    server = WebServer("LED (Pin 2)", 2, False, "RELAY (Pin 16)", 16, True)
    server.run_server()


if __name__ == "__main__":
    main()
