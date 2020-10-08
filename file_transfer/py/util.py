#!/usr/bin/env python3
import os
import sys
import socket
import logging
import argparse
import typing_extensions  # typing.Protocol is available in py 3.8


class ReaderWriter(typing_extensions.Protocol):

    def read(self, size: int) -> bytes:
        pass

    def write(self, data: bytes) -> int:
        pass


class ConnReaderWriter():

    def __init__(self, conn: socket.socket):
        self._conn: socket.socket = conn

    def read(self, size: int) -> bytes:
        return self._conn.recv(size)

    def write(self, data: bytes) -> int:
        return self._conn.send(data)


class StdoutReaderWriter():

    def read(self, size: int) -> bytes:
        return sys.stdout.read(size).encode('utf-8')

    def write(self, data: bytes) -> int:
        return sys.stdout.write(data.decode('utf-8'))


def copy(src: ReaderWriter, dst: ReaderWriter) -> int:
    chunk = 16 * 1024 * 1024
    count = 1

    total = 0
    while True:
        data = src.read(4096)
        if not data:
            break
        size = 0
        while size < len(data):
            size += dst.write(data[size:])
        total += size

        if total > count * chunk:
            logging.debug(f'Copied {total / 1024 / 1024} MB')
            count += 1

    return total


def file2conn(filename: str, conn: socket.socket):
    if not os.path.isfile(filename):
        logging.error(
            f'"{filename}" is not file, please specify a file for reading')
        sys.exit(1)

    with open(filename, 'rb') as reader:
        copy(reader, ConnReaderWriter(conn))
    conn.close()


def conn2file(filename: str, conn: socket.socket):
    if not filename:
        writer = StdoutReaderWriter()
    else:
        writer = open(filename, 'wb')

    copy(ConnReaderWriter(conn), writer)

    if filename:
        writer.close()


def parse_arg():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-a',
        '--address',
        type = str,
        default = '',
        help = 'The address for connecting to server')
    parser.add_argument(
        '-p',
        '--port',
        type = int,
        default = 8000,
        help = 'The port for connecting or listening')
    parser.add_argument(
        '-f',
        '--file',
        type = str,
        default = '',
        help = 'The filename for reading or writing')
    parser.add_argument(
        '-c2s',
        '--client2server',
        action = 'store_true',
        help = 'Specify for transfering file from client to server')

    return parser.parse_args()
