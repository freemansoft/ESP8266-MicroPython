# Complete project details at https://RandomNerdTutorials.com
import socket
import machine
import gc


class WebServer(object):
    """webserver that can change output pins and display current pin state"""

    def __init__(
        self,
        control_pin_nums,
        control_pin_labels,
        control_pin_on_high,
        monitor_pin_nums,
    ):
        self.control_pin_labels = control_pin_labels
        self.control_pin_on_high = control_pin_on_high
        self.control_pin_nums = control_pin_nums
        self.control_pins = [machine.Pin(i, machine.Pin.OUT)
                             for i in control_pin_nums]
        self.pins_to_monitor = [machine.Pin(i) for i in monitor_pin_nums]

    def _web_page_html(self):

        html = (
            """<html><head> <title>ESP Web Server</title> <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="icon" href="data:,"> <style>
    html{font-family: Verndana; display:inline-block; margin: 0px auto; text-align: center;}
    h1{color: #0F3376; padding: 2vh;}
    p{font-size: 1.5rem;}
    .button{display: inline-block; background-color: #e7bd3b; border: none; border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
    .button2{background-color: #4286f4;} 
    table {border-collapse: collapse; display:inline-block; margin: 5px auto; text-align: center;} tr {border-bottom: 1px solid #ddd; font-size: 1.5rem;} td { padding: 10px;}
    </style>
    </head>
    <body> 
    <h1>ESP Controls</h1> 
    %s
    <p>Current state takes into account pin inversion</p>
    <h1>ESP Pin Raw State</h1> 
    <table><tr><th>Pin</th> %s </tr><tr><th>Pin State</th > %s </tr></table>
    </body></html>"""
        )
        control_pin_state = ''.join(
            ['<p><strong>%s</strong> Currently On: %s</p> <p><a href="?dev_%s=on"><button class="button button">ON</button></a><a href="?dev_%s=off"><button class="button button2">OFF</button></a></p>'
             % (pin_label, str(bool(self.control_pins[p].value()) == self.control_pin_on_high[p]), str(p), str(p))
             for p, pin_label in enumerate(self.control_pin_labels)]
        )
        # labels and values on own rows
        monitor_pin_number = ''.join(
            ['<td> %s </td>' % (str(p)) for p in self.pins_to_monitor])
        monitor_pin_state = ''.join(
            ['<td> %s </td>' % (str(p.value())) for p in self.pins_to_monitor])

        #print(monitor_pin_number, '\n', monitor_pin_state)
        return html % (control_pin_state, monitor_pin_number, monitor_pin_state)

    def _handle_request(self, request):

        # first line is request - ignore the headers and referrer
        line_get = request.split("\r")[0]
        # should we verify it is a GET?
        for p, control_pin in enumerate(self.control_pins):
            dev_on = line_get.find("dev_"+str(p)+"=on")
            dev_off = line_get.find("dev_"+str(p)+"=off")
            if dev_on > 0:
                #print("DEV ", p, " ON: ", dev_on)
                control_pin.value(int(self.control_pin_on_high[p]))
            if dev_off > 0:
                #print("DEV ", p, " OFF: ", dev_off)
                control_pin.value(int(not self.control_pin_on_high[p]))

    def run_server(self):
        """runs the web server"""
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("", 80))
        s.listen(5)
        try:
            while True:
                # emperical number for ESP8266
                if gc.mem_free() < 20000:
                    print("pre-free used:"+str(gc.mem_alloc()) +
                          " free:"+str(gc.mem_free()))
                    gc.collect()
                    print("post-free used:"+str(gc.mem_alloc()) +
                          " free:"+str(gc.mem_free()))
                conn, addr = s.accept()
                conn.settimeout(3.0)
                print("Got a connection from %s" % str(addr))
                request = conn.recv(1024)
                request = request.decode("utf-8")
                print("Request Bytes:%d Content:\n%s" %
                      (len(request), request))

                self._handle_request(request)

                response = self._web_page_html()
                conn.send("HTTP/1.1 200 OK\n")
                conn.send("Content-Type: text/html\n")
                conn.send("Connection: close\n\n")
                conn.sendall(response)
                conn.close()
                print('Connection closed used:'+str(gc.mem_alloc()) +
                      ' free:'+str(gc.mem_free()))
        except OSError as e:
            conn.close()
            print("Connection closed on error " + str(e.errno))
            raise
