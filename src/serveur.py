#!/usr/bin/python3

import socket
import select
import threading
import sys
import pickle
import time

from macro import *
from grid import *
from jeu import *

port = 8888

listeSocket = []
listeJoueur = []

serverSocket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM, 0, None)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serverSocket.bind(('', port))
serverSocket.listen(1)
listeSocket.append(serverSocket)

nb_joueur = 0
game = Game()

while(1):
    listeRead, _ , _ = select.select(listeSocket, [], [])
    for i in listeRead:
        if (i == serverSocket):
            new_socket, adresse = serverSocket.accept()
            listeSocket.append(new_socket)
            new_socket.send(MSG_WELCOME)

        if (nb_joueur < 2) :
            listeJoueur.append(new_socket)
            nb_joueur = nb_joueur + 1

        if (nb_joueur == 2) :
            game.add_players(listeJoueur)
            main(game) #fonction main jeu.py
            time.sleep(1)
            exit()
