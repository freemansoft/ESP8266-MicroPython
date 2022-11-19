# Complete project details at https://RandomNerdTutorials.com
import socket
import machine
import gc


class WebServer(object):
    """webserver that can change output pins"""

    def __init__(self, ledpinnumbr, relaypinnumber):
        self.ledpinnumber = ledpinnumbr
        self.relaypinnumber = relaypinnumber
        self.led = machine.Pin(self.ledpinnumber, machine.Pin.OUT)
        self.relay = machine.Pin(self.relaypinnumber, machine.Pin.OUT)

    def _web_page_html(self):

        html = """<html><head> <title>ESP Web Server</title> <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="icon" href="data:,"> <style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
    h1{color: #0F3376; padding: 2vh;}p{font-size: 1.5rem;}.button{display: inline-block; background-color: #e7bd3b; border: none; 
    border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
    .button2{background-color: #4286f4;}</style></head><body> <h1>ESP Web Server</h1> 
    <p><strong>LED (2)</strong></p>
    <p><a href="/?led=on"><button class="button button">ON</button></a></p>
    <p><a href="/?led=off"><button class="button button2">OFF</button></a></p>
    <p><strong>Relay (16)</strong></p>
    <p><a href="/?relay=on"><button class="button button">ON</button></a></p>
    <p><a href="/?relay=off"><button class="button button2">OFF</button></a></p>
    </body></html>"""
        return html

    def _handle_request(self, request):

        relay_on = request.find("relay=on")
        relay_off = request.find("relay=off")
        led_on = request.find("led=on")
        led_off = request.find("led=off")

        # content has referrer uri
        if led_on == 8:
            print("LED ON: ", led_on)
            self.led.value(0)
        if led_off == 8:
            print("LED OFF: ", led_off)
            self.led.value(1)
        if relay_on == 8:
            print("RELAY ON: ", relay_on)
            self.relay.value(1)
        if relay_off == 8:
            print("RELAY OFF: ", relay_off)
            self.relay.value(0)

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
