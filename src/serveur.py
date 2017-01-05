#!/usr/bin/python3

import socket
import select
import threading
import sys
import pickle
import time

from macro import *
from test import main
from grid import *

listeSocket = []
listeJoueur = []
listeSpec   = []

serverSocket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM, 0, None)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serverSocket.bind(('', 8888))
serverSocket.listen(1)
listeSocket.append(serverSocket)

nb_joueur = 0

while(1):
    listeRead, _ , _ = select.select(listeSocket, [], [])
    for i in listeRead:
        if (i == serverSocket):
            new_socket, adresse = serverSocket.accept()
            listeSocket.append(new_socket)
            nb_joueur = nb_joueur + 1
            print("clients connectés : " + str(nb_joueur))

        if (len(listeJoueur) < 2) :
            listeJoueur.append(new_socket)

        if (len(listeJoueur) > 2) :
            listeSpec.append(new_socket)

        if (len(listeJoueur) == 2) :
            main(listeJoueur)
            time.sleep(1)
            serverSocket.close()
