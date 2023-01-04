# Complete project details at https://RandomNerdTutorials.com
import socket
import gc

html_template = """<html><head> 
    <title>%s</title> <meta name="viewport" content="width=device-width, initial-scale=1"><link rel="icon" href="data:,"> 
    <link rel="stylesheet" href="//code.jquery.com/ui/1.13.2/themes/excite-bike/jquery-ui.css">
    <script src="https://code.jquery.com/jquery-3.6.0.js"></script>
    <script src="https://code.jquery.com/ui/1.13.2/jquery-ui.min.js"></script>
    <style>
    html{ display:inline-block; margin: 0px auto; text-align: center;}
    table {border-collapse: collapse; display:inline-block; text-align: center;} tr {border-bottom: 1px solid #ddd; } th,td { padding: 10px;}
    body { background-color: lightgrey; }
    </style>
    <script>
        function changeServo(event, ui) { var id = $(this).attr('id'); $.get('/', {[id]: ui.value} ) }
        $(document).ready(function(){
            $('[id^=servo_]').each(
                function(){ var currentValue = $(this).text(); $(this).empty().slider({min: 0, max:180, change:changeServo, value:currentValue});}
            )
        });
        $( function() { $( ".widget a" ).button(); } );
    </script>
    </head><body> <div class="widget">
    <fieldset><legend>Output Pins - Current state incl pin inversion</legend>%s</fieldset>
    <fieldset><legend>Servo Pins</legend>%s</fieldset>
    <fieldset><legend>Timed Operations</legend>%s</fieldset>
    <fieldset><legend>Raw Pin State (as read)</legend><table><tr><th>Pin</th><th>Pin State</th ></tr> %s </table></fieldset>
    %s</div></body></html>"""


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
        periodic_ops,
        periodic_labels,
        title,
        message,
    ):
        self.control_pins = control_pins
        self.control_pin_labels = control_pin_labels
        self.servo_pins = servo_pins
        self.servo_pin_labels = servo_pin_labels
        self.pins_to_monitor = monitor_pins
        self.periodic_ops = periodic_ops
        self.periodic_labels = periodic_labels
        self.message = message
        self.title = title
        self.debug_enabled = True

    def _render_html(self, template):
        # jquery callback that generates a GET request using the id as the key
        # jquery.ready() replaces every div=servo... with the jquery slider
        # Need to turn of logging to increase performance

        control_pin_state = "".join(
            [
                '<div><label>%s Currently:%s</label><br/><a href="?out_%d=on">ON</a><a href="?out_%d=off" >OFF</a></div>'
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
                "<div><label>%s</label><div id=servo_%d>%d</div></div>"
                % (
                    servo_label,
                    p,
                    self.servo_pins[p].degrees,
                )
                for p, servo_label in enumerate(
                    self.servo_pin_labels,
                )
            ]
        )
        timer_pin_state = "".join(
            [
                '<div><label>%s Running: %s</label><br/><a href="?period_%d=on">ON</a><a href="?period_%d=off">OFF</a></div>'
                % (
                    periodic_label,
                    str(periodic_op.running()),
                    p,
                    p,
                )
                for p, (periodic_label, periodic_op) in enumerate(
                    zip(
                        self.periodic_labels,
                        self.periodic_ops,
                    )
                )
            ]
        )
        monitor_pin_state = "".join(
            [
                # each pin on its own row to make JSON easier later
                "<tr><td>%s</td><td>%d</td></tr>"
                % (
                    str(apin),
                    apin.value(),
                )
                for p, apin in enumerate(
                    self.pins_to_monitor,
                )
            ]
        )

        # if self.debug_enabled:
        #     print(monitor_pin_number, '\n', monitor_pin_state)
        return template % (
            self.title,
            control_pin_state,
            servo_pin_state,
            timer_pin_state,
            monitor_pin_state,
            self.message,
        )

    def _query_parse(self, query, path_with_query):
        """https://techtutorialsx.com/2017/09/29/esp32-micropython-developing-a-simple-url-query-string-parser/"""
        parameters = {}
        # remove the GET and HTTP portions looks like
        #   GET /?x=y&a=b HTTP/1.1
        # Code doesn't handle alt paths /api/?x=y&a=b
        pStart = query.split(" ")
        if not pStart[1].startswith(path_with_query):
            if self.debug_enabled:
                print("Request: Skipping param parsing:" + pStart[1])
            return {}
        amperSplit = pStart[1][2:].split("&")
        # if self.debug_enabled:
        #     print(amperSplit)
        for element in amperSplit:
            equalSplit = element.split("=")
            parameters[equalSplit[0]] = equalSplit[1]
        if self.debug_enabled:
            print("Parameters:" + str(parameters))
        return parameters

    def _operate_control_pins(self, parameters):
        # iterate across control pins to see if any were updated
        for p, control_pin in enumerate(self.control_pins):
            try:
                out_value = parameters["out_" + str(p)]
                if self.debug_enabled:
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
                if self.debug_enabled:
                    print("servo_%s %s %s" % (str(p), servo_pin, servo_value))
                servo_pin.write_angle(int(servo_value))
            except KeyError:
                pass

    def _operate_periodic(self, parameters):
        # iterate across control pins to see if any were updated
        for p, period_func in enumerate(self.periodic_ops):
            try:
                out_value = parameters["period_" + str(p)]
                if self.debug_enabled:
                    print("out_%s %s %s" % (str(p), self.periodic_labels[p], out_value))
                if out_value == "on":
                    period_func.start()
                elif out_value == "off":
                    period_func.stop()
            except KeyError:
                pass

    def _handle_request(self, request):
        # first line is request - ignore the headers and referrer
        line_get = request.split("\n")[0]
        print("Request Processing: %s" % (line_get))
        if line_get.startswith("GET"):
            parameters = self._query_parse(line_get, "/?")
            self._operate_control_pins(parameters)
            self._operate_servos(parameters)
            self._operate_periodic(parameters)
        else:
            if self.debug_enabled:
                print("HTTP GET Only. Ignoring: %s" % line_get)

    def _free_mem(self):
        try:
            # 22K was the number before using timer callbacks
            # emperical number for ESP8266
            if gc.mem_free() < 15000:
                if self.debug_enabled:
                    print(
                        "pre-free used:"
                        + str(gc.mem_alloc())
                        + " free:"
                        + str(gc.mem_free())
                    )
                gc.collect()
                if self.debug_enabled:
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
        # print("run_server")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("", 80))
        s.listen(5)
        while True:
            try:
                self._free_mem()
                conn, addr = s.accept()
                # browsers often make an immediate follow up request
                conn.settimeout(3.0)
                if self.debug_enabled:
                    print("Got a connection")
                request = conn.recv(1024).decode()
                if self.debug_enabled:
                    print("Request Bytes:%d " % (len(request)))
                    # print("Request Content:\n%s" % (request))

                self._handle_request(request)

                if request.find("text/html") > 0:
                    if self.debug_enabled:
                        print("Processing HTML request")
                    response = self._render_html(html_template)
                    response_raw = response.encode()
                    response_len_str = str(len(response_raw))
                    response_len_header = "Content-Length: " + response_len_str + "\n"
                    conn.send("HTTP/1.1 200 OK\nContent-Type: text/html\n".encode())
                    conn.send(response_len_header.encode())
                    conn.send("Connection: close\n\n".encode())
                    conn.sendall(response_raw)
                else:
                    # TODO json document generation not implemented
                    if self.debug_enabled:
                        print("Processing as JSON request")
                    # prepare for json
                    response = "{}"
                    response_raw = response.encode()
                    response_len_str = str(len(response_raw))
                    response_len_header = "Content-Length: " + response_len_str + "\n"
                    conn.send("HTTP/1.1 200 OK\nContent-Type: text/json\n".encode())
                    conn.send(response_len_header.encode())
                    conn.send("Connection: close\n\n".encode())
                    conn.sendall("{}".encode())

                conn.close()
                if self.debug_enabled:
                    print("Connection closed ")
                self._free_mem()
            except OSError as e:
                conn.close()
                print("Connection closed on error " + str(e) + " " + str(e.errno))
                pass
                # raise
