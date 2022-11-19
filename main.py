''' copies of the variables'''
from config import ssid, password

from connectwifi import WIFI
from webserver import WebServer
from toggle import toggle_pin
from httpget import http_get_print


def main():
    '''lets us test main() without board reset'''
    conn = WIFI(ssid, password, "myhostname")
    conn.do_connect()

    http_get_print("http://micropython.org/ks/test.html")
    toggle_pin(2, 500, 10)

    server = WebServer(2, 16)
    server.run_server()


if __name__ == "__main__":
    main()
