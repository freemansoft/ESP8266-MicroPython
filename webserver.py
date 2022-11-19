# Complete project details at https://RandomNerdTutorials.com
import socket
import machine
import gc


class WebServer(object):
    """webserver that can change output pins"""

    def __init__(
        self,
        dev1_label,
        dev1_pin_number,
        dev1_on_is_high,
        dev2_label,
        dev2_pin_number,
        dev2_on_is_high,
    ):
        self.dev1_label = dev1_label
        self.dev1_pin_number = dev1_pin_number
        self.dev1_on_is_high = dev1_on_is_high
        self.dev2_label = dev2_label
        self.dev2_pin_number = dev2_pin_number
        self.dev2_on_is_high = dev2_on_is_high
        self.led = machine.Pin(self.dev1_pin_number, machine.Pin.OUT)
        self.relay = machine.Pin(self.dev2_pin_number, machine.Pin.OUT)

    def _web_page_html(self):

        html = (
            """<html><head> <title>ESP Web Server</title> <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="icon" href="data:,"> <style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
    h1{color: #0F3376; padding: 2vh;}p{font-size: 1.5rem;}.button{display: inline-block; background-color: #e7bd3b; border: none; 
    border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
    .button2{background-color: #4286f4;}</style></head><body> <h1>ESP Web Server</h1> 
    """
            + """<p><strong>"""
            + self.dev1_label
            + """</strong></p>
    <p><a href="/?dev1=on"><button class="button button">ON</button></a><a href="/?dev1=off"><button class="button button2">OFF</button></a></p>
    """
            + """<p><strong>"""
            + self.dev2_label
            + """</strong></p>
    <p><a href="/?dev2=on"><button class="button button">ON</button></a><a href="/?dev2=off"><button class="button button2">OFF</button></a></p>
    </body></html>"""
        )
        return html

    def _handle_request(self, request):

        dev1_on = request.find("dev1=on")
        dev1_off = request.find("dev1=off")
        dev2_on = request.find("dev2=on")
        dev2_off = request.find("dev2=off")

        # fixed index because content has referrer uri
        if dev1_on == 8:
            print("DEV1 ON: ", dev1_on)
            self.led.value(int(self.dev1_on_is_high))
        if dev1_off == 8:
            print("DEV1 OFF: ", dev1_off)
            self.led.value(int(not self.dev1_on_is_high))
        if dev2_on == 8:
            print("DEV2 ON: ", dev2_on)
            self.relay.value(int(self.dev2_on_is_high))
        if dev2_off == 8:
            print("DEV2 OFF: ", dev2_off)
            self.relay.value(int(not self.dev2_on_is_high))

    def run_server(self):
        """runs the web server"""
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("", 80))
        s.listen(5)
        try:
            while True:
                if gc.mem_free() < 102000:
                    gc.collect()
                conn, addr = s.accept()
                conn.settimeout(3.0)
                print("Got a connection from %s" % str(addr))
                request = conn.recv(1024)
                request = str(request)
                print("Content = %s" % request)

                self._handle_request(request)

                response = self._web_page_html()
                conn.send("HTTP/1.1 200 OK\n")
                conn.send("Content-Type: text/html\n")
                conn.send("Connection: close\n\n")
                conn.sendall(response)
                conn.close()
                # print('Connection closed')
        except OSError as e:
            conn.close()
            print("Connection closed on error")