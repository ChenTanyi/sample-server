#!/usr/bin/env python3
import socket

address = '127.0.0.1'
port = 9999

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((address, port))

client.send(b'Hello From Client!')