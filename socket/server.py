#!/usr/bin/env python3
import os
import sys
import socket
import logging

if __name__ == "__main__":
    logging.basicConfig(
        format = '%(asctime)s %(levelname)-8s %(message)s',
        level = logging.DEBUG)
    port = 9999 if len(sys.argv) < 2 else int(sys.argv[1])
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', port))
        logging.info(f'listening at {port}')

        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                conn.sendall(data)