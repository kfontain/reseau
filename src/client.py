#!/usr/bin/python3

from grid import grid
from macro import *

import sys
import socket
import select


host = "localhost"
port = int(sys.argv[1])

s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM, 0, None)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.connect((host, port))
grid = grid()
print("connecting to port " + str(port))

while True :
    read, _ , _ = select.select([s], [], [])
    for tmp in read :
        msg = int.from_bytes(tmp.recv(1024), byteorder = 'big')
        print("message reçu : " + str(msg))

#Pour l'instant ne marche pas, l'entier reçu est toujours égal à 0. (Normalement égal à 11)
