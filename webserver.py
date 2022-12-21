# Complete project details at https://RandomNerdTutorials.com
import socket
import gc


class WebServer(object):
    """webserver that can change output pins and display current pin state.
    Control pins should be presented as machine.Signal.
    """

    def __init__(
        self,
        control_pins,
        control_pin_labels,
        servo_pins,
        servo_pin_labels,
        monitor_pins,
        message,
    ):
        self.control_pins = control_pins
        self.control_pin_labels = control_pin_labels
        self.servo_pins = servo_pins
        self.servo_pin_labels = servo_pin_labels
        self.pins_to_monitor = monitor_pins
        self.message = message

    def _web_page_html(self):

        html = """<html><head> <title>ESP Web Server</title> <meta name="viewport" content="width=device-width, initial-scale=1"><link rel="icon" href="data:,"> 
    <style>
    html{font-family: Verndana; display:inline-block; margin: 0px auto; text-align: center;}
    h1{color: #0F3376; padding: 2vh;}
    p{font-size: 1.5rem;}
    .button{display: inline-block; background-color: #e7bd3b; border: none; border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
    .button2{background-color: #4286f4;} 
    table {border-collapse: collapse; display:inline-block; margin: 5px auto; text-align: center;} tr {border-bottom: 1px solid #ddd; font-size: 1.0rem;} td { padding: 10px;}
    </style></head>
    <body> 
    <h1>ESP 8266</h1><hr>
    <h2>Output Pins</h2> 
    %s
    <br/>Current state takes into account pin inversion<br/><hr>
    <h2>Servo Pins</h2> 
    %s
    <p></p><hr>
    <h2>Raw Pin State - as read</h2> 
    <table><tr><th>Pin</th> %s </tr><tr><th>Pin State</th > %s </tr></table>
    <br/><hr><br/>%s<br/>
    </body></html>"""

        control_pin_state = "".join(
            [
                '<p><strong>%s</strong> Currently On: %s</p> <p><a href="?out_%d=on"><button class="button button">ON</button></a><a href="?out_%d=off"><button class="button button2">OFF</button></a></p>'
                % (
                    pin_label,
                    str(control_pin.value()),
                    p,
                    p,
                )
                for p, (pin_label, control_pin) in enumerate(
                    zip(
                        self.control_pin_labels,
                        self.control_pins,
                    )
                )
            ]
        )
        servo_pin_state = "".join(
            [
                '<p><strong>%s</strong> uSec: %d</p> <p><a href="?servo_%d=0"><button class="button button">0</button></a><a href="?servo_%d=90"><button class="button button2">90</button></a><a href="?servo_%d=180"><button class="button button">180</button></a></p>'
                % (
                    servo_label,
                    self.servo_pins[p].us,
                    p,
                    p,
                    p,
                )
                for p, servo_label in enumerate(
                    self.servo_pin_labels,
                )
            ]
        )
        # labels and values on own rows
        monitor_pin_number = "".join(
            ["<td> %s </td>" % (str(p)) for p in self.pins_to_monitor]
        )
        monitor_pin_state = "".join(
            ["<td> %d </td>" % (p.value()) for p in self.pins_to_monitor]
        )

        # print(monitor_pin_number, '\n', monitor_pin_state)
        return html % (
            control_pin_state,
            servo_pin_state,
            monitor_pin_number,
            monitor_pin_state,
            self.message,
        )

    def _query_parse(self, query):
        """https://techtutorialsx.com/2017/09/29/esp32-micropython-developing-a-simple-url-query-string-parser/"""
        parameters = {}
        # remove the GET and HTTP portions
        pStart = query.split(" ")
        # after /?
        if not ("/?" in pStart[1]):
            return {}
        amperSplit = pStart[1][2:].split("&")
        # print(amperSplit)
        for element in amperSplit:
            equalSplit = element.split("=")
            parameters[equalSplit[0]] = equalSplit[1]
        print("Parameters: " + str(parameters))
        return parameters

    def _operate_control_pins(self, parameters):
        # iterate across control pins to see if any were updated
        for p, control_pin in enumerate(self.control_pins):
            try:
                out_value = parameters["out_" + str(p)]
                print("out_%s %s %s" % (str(p), control_pin, out_value))
                if out_value == "on":
                    control_pin.on()
                elif out_value == "off":
                    control_pin.off()
            except KeyError:
                pass

    def _operate_servos(self, parameters):
        for p, servo_pin in enumerate(self.servo_pins):
            try:
                servo_value = parameters["servo_" + str(p)]
                print("servo_%s %s %s" % (str(p), servo_pin, servo_value))
                servo_pin.write_angle(int(servo_value))
            except KeyError:
                pass

    def _handle_request(self, request):
        # first line is request - ignore the headers and referrer
        line_get = request.split("\n")[0]
        print("Request Processing: %s" % (line_get))
        if line_get.startswith("GET"):
            parameters = self._query_parse(line_get)
            self._operate_control_pins(parameters)
            self._operate_servos(parameters)
        else:
            print("HTTP GET Only.  Ignoring: %s" % line_get)

    def _free_mem(self):
        try:
            # emperical number for ESP8266
            if gc.mem_free() < 20000:
                print(
                    "pre-free used:"
                    + str(gc.mem_alloc())
                    + " free:"
                    + str(gc.mem_free())
                )
                gc.collect()
                print(
                    "post-free used:"
                    + str(gc.mem_alloc())
                    + " free:"
                    + str(gc.mem_free())
                )
        except AttributeError:
            print("no memfree in this version of python")

    def run_server(self):
        """runs the web server"""
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("", 80))
        s.listen(5)
        while True:
            try:
                self._free_mem()
                conn, addr = s.accept()
                # browsers often make an immediate follow up request
                conn.settimeout(30.0)
                print("Got a connection from %s" % str(addr))
                request = conn.recv(1024).decode()
                print("Request Bytes:%d " % (len(request)))
                # print("Request Content:\n%s" % (request))

                self._handle_request(request)

                response = self._web_page_html()
                response_raw = response.encode()
                conn.send(
                    "HTTP/1.1 200 OK\nContent-Type: text/html\nConnection: close\n\n".encode()
                )
                conn.sendall(response_raw)
                conn.close()
                print("Connection closed ")
                self._free_mem()
            except OSError as e:
                conn.close()
                print("Connection closed on error " + str(e) + " " + str(e.errno))
                pass
                # raise
