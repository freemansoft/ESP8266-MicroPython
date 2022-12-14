import network
import time


class WIFI(object):
    """manages wifi connection"""

    def __init__(self, wifi_ssid, wifi_password, hostname):
        self.wifi_ssid = wifi_ssid
        self.wifi_password = wifi_password
        self.hostname = hostname

    def do_connect(self):
        """connect to wifi"""
        if self.wifi_ssid is not None and self.wifi_password is not None:
            self.station = network.WLAN(network.STA_IF)
            self.station.active(True)
            time.sleep_us(100)
            self.station.config(dhcp_hostname=self.hostname)
            if not self.station.isconnected():
                print("connecting to network...")
                self.station.connect(self.wifi_ssid, self.wifi_password)
                while not self.station.isconnected():
                    pass
            try:
                host = self.station.config("hostname")
            except ValueError:
                # "hostname" is available in master, but not yet in June 2022 1.19.1 release
                host = self.station.config("dhcp_hostname")
            ipinfo = self.station.ifconfig()
            return ipinfo
        else:
            print("No wifi configured because no wifi_ssid or wifi_password set.")
            return ("x", "x", "x", "x")

    def log_ap_state(self):
        ap = network.WLAN(network.AP_IF)
        ipinfo = ap.ifconfig()
        return ipinfo
