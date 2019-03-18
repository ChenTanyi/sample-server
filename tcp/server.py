#!/usr/bin/env python3
import socketserver
import select
import logging
import socket


class ThreadingTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True


class TCPHandler(socketserver.StreamRequestHandler):

    def handle(self):
        sock = self.connection
        try:
            fdset = [sock]
            while True:
                r, w, e = select.select(fdset, [], [])
                if sock in r:
                    data = sock.recv(4096)
                    if len(data) <= 0:
                        break
                    logging.info(data)

        finally:
            sock.close()


if __name__ == '__main__':
    logging.basicConfig(
        format = '%(asctime)s %(levelname)-8s %(message)s',
        level = logging.DEBUG)
    try:
        port = 9999
        server = ThreadingTCPServer(('', port), TCPHandler)
        logging.info(f'listening at {port}')
        server.serve_forever()
    except socket.error as e:
        logging.exception(e)
