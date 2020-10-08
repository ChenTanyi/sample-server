#!/usr/bin/env python3
import os
import sys
import util
import socket
import logging

if __name__ == "__main__":
    logging.basicConfig(
        format = '%(asctime)s %(levelname)s %(message)s',
        level = logging.DEBUG)
    args = util.parse_arg()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', args.port))
        logging.info(f'listening at {args.port} ...')

        s.listen()
        conn, addr = s.accept()
        logging.info(f'connected from {addr}')

        if args.client2server:
            util.conn2file(args.file, conn)
        else:
            util.file2conn(args.file, conn)