#!/usr/bin/python3

import sys
import socket

host = "localhost"
port = int(sys.argv[1])

sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM, 0, None)
sock.connect((host, port))
print("connecting to port "+ str(port))

while True : 
    message = str(sock.recv(10000))
    print(message)
