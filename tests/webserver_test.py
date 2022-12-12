"""
Run with `pytest -s` if you wish to see the print output
This is in the test module because of the __init__.py file in this dir
"""
from tests.testfakepin import FakePin
from tests.testfakeservo import FakeServo
from webserver import WebServer
from unittest import TestCase

# This horrible thing is not really a test because it never ends!
# TODO figure out a way to bring up the server, run tests and then tear down the server


def test_run_server():
    pin1 = FakePin(2)
    pin2 = FakePin(5)
    pin3 = FakePin(16)
    out_pins = [pin1, pin3]
    out_labels = ["LED (Pin 2)", "RELAY (Pin 16)"]
    out_inversion = [False, True]
    servo_pins = [FakeServo(FakePin(14))]
    servo_labels = ["Servo 14"]
    out_pins_all = [pin1, pin2, pin3]
    server = WebServer(
        out_pins,
        out_labels,
        out_inversion,
        servo_pins,
        servo_labels,
        out_pins_all,
    )
    print("")
    print("ctrl-c to exit this server")
    server.run_server()
