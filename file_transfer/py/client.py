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
        s.connect((args.address, args.port))
        logging.info(f'connected to {args.address}:{args.port}')

        if args.client2server:
            util.file2conn(args.file, s)
        else:
            util.conn2file(args.file, s)