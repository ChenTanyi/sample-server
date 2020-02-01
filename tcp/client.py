#!/usr/bin/env python3
import socket

address = '0.0.0.0'
port = 9999

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((address, port))

client.send('Hello From Client!')