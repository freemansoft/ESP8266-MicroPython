import network
import time


class WIFI(object):
    '''manages wifi connection'''

    def __init__(self, ssid, passwd, hostname):
        self.ssid = ssid
        self.passwd = passwd
        self.hostname = hostname

    def do_connect(self):
        '''connect to wifi'''
        self.station = network.WLAN(network.STA_IF)
        self.station.active(True)
        time.sleep_us(100)
        self.station.config('dhcp_hostname')
        self.station.config(dhcp_hostname=self.hostname)
        if not self.station.isconnected():
            print("connecting to network...")
            self.station.connect(self.ssid, self.passwd)
            while not self.station.isconnected():
                pass
        print("network config:", self.station.ifconfig())
