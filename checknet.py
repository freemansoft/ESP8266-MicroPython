"""
Simple test program.  
Should probably rename main.py to something else if you want to use start_network()
"""
import network


def check_ap():
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    print(ap.ifconfig())
    # ap.active(False)


# 1001
# 1010
def start_network():
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    print(sta_if.scan())  # Scan for available access points
    sta_if.connect("python", "pythonpython")  # Connect to an AP


def check_if():
    sta_if = network.WLAN(network.STA_IF)
    print(sta_if.isconnected())  # Check for successful connection
    print(sta_if.ifconfig())
    print(sta_if.status())
