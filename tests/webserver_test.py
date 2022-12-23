"""
Run with `pytest -s` if you wish to see the print output
This is in the test module because of the __init__.py file in this dir
"""
from tests.testfakepin import FakePin
from tests.testfakeservo import FakeServo
from tests.testfakesignal import FakeSignal
from tests.testfaketimer import FakeTimer
from webserver import WebServer
from unittest import TestCase
from periodicoperator import PeriodicOperator
from toggle import TogglePin

# This horrible thing is not really a test because it never ends!
# TODO figure out a way to bring up the server, run tests and then tear down the server


def test_run_server():
    pin1 = FakePin(2)
    pin2 = FakePin(5)
    pin3 = FakePin(16)
    out_pins = [FakeSignal(pin1, invert=True), FakeSignal(pin3, invert=False)]
    out_labels = ["LED (Pin 2)", "RELAY (Pin 16)"]
    servo_pins = [FakeServo(FakePin(14))]
    servo_labels = ["Servo 14"]
    out_pins_all = [pin1, pin2, pin3]

    a_periodic_handler = TogglePin(pin2)
    periodic_operators = [
        PeriodicOperator(FakeTimer(-1), 500, a_periodic_handler.toggle_pin_callback)
    ]
    periodic_labels = ["my fake timer control"]

    server = WebServer(
        out_pins,
        out_labels,
        servo_pins,
        servo_labels,
        out_pins_all,
        periodic_operators,
        periodic_labels,
        "Hello this is the message area",
    )
    print("")
    print("ctrl-c to exit this server")
    server.run_server()
