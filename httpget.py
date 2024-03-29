# SPDX-FileCopyrightText: 2022 Joe Freeman joe@freemansoft.com
#
# SPDX-License-Identifier: MIT
#
import socket


def http_get_print(url):

    _, _, host, path = url.split("/", 3)
    addr = socket.getaddrinfo(host, 80)[0][-1]
    s = socket.socket()
    s.connect(addr)
    s.send(bytes("GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n" % (path, host), "utf8"))
    while True:
        data = s.recv(100)
        if data:
            print(str(data, "utf8"), end="")
        else:
            break
    s.close()
