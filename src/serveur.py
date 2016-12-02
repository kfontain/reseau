#!/usr/bin/python3

import socket
import select
import threading
import sys

listeSocket = []

serverSocket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM, 0, None)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serverSocket.bind(('',7777))
serverSocket.listen(1)
listeSocket.append(serverSocket)

while(1):
    listeRead, l2 ,l3 = select.select(l, t1, t2)
    for i in listeRead:
        if (i == serverSocket):
            new_socket, adresse = serverSocket.accept()
            listeSocket.append(new_socket)
            if (listeSocket.len > 3) :
                new_socket.send("Déjà 2 joueurs connectés.")

        else:
