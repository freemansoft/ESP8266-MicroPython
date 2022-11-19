# Brings in copies of the variables
from config import ssid, password
from connectwifi import WIFI
from toggle import toggle_pin

# lets me test main.py on boards that don't reset when main.py is updated
def main():
    conn = WIFI(ssid, password)
    conn.do_connect()

    from httpget import http_get_print

    http_get_print("http://micropython.org/ks/test.html")

    toggle_pin(2, 500, 10)


if __name__ == "__main__":
    main()
