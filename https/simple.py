#!/usr/bin/env python3
import http.server
import ssl

httpd = http.server.HTTPServer(('', 443), http.server.SimpleHTTPRequestHandler)
httpd.socket = ssl.wrap_socket(
    httpd.socket,
    keyfile = './key.pem',
    certfile = './cer.pem',
    server_side = True)

httpd.serve_forever()