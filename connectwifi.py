import network


class WIFI(object):
    def __init__(self, ssid, passwd):
        self.ssid = ssid
        self.passwd = passwd

    def do_connect(self):
        self.station = network.WLAN(network.STA_IF)
        self.station.active(True)
        if not self.station.isconnected():
            print("connecting to network...")
            self.station.connect(self.ssid, self.passwd)
            while not self.station.isconnected():
                pass
        print("network config:", self.station.ifconfig())
