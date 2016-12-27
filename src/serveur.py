#!/usr/bin/python3

import socket
import select
import threading
import sys

from macro import *
from jeu import main

listeSocket = []
listeJoueur = []

serverSocket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM, 0, None)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serverSocket.bind(('', 8888))
serverSocket.listen(1)
listeSocket.append(serverSocket)

nb_joueur = 1

while(1):
    listeRead, _ , _ = select.select(listeSocket, [], [])
    for i in listeRead:
        if (i == serverSocket):
            print ("Nombre de joueurs connectes :", nb_joueur)
            new_socket, adresse = serverSocket.accept()
            listeSocket.append(new_socket)

        if (len(listeJoueur) < 2) :
            listeJoueur.append(new_socket)
            nb_joueur = nb_joueur + 1

        if (len(listeJoueur) == 2) :
            for j in listeJoueur :
                j.send(bytes(START))
