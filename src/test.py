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
listeSpec   = []

serverSocket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM, 0, None)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serverSocket.bind(('', port))
serverSocket.listen(1)
listeSocket.append(serverSocket)

nb_user = 0
nb_joueur = 0
gaming = 0
game = Game()

while(1):
    listeRead, _ , _ = select.select(listeSocket, [], [])
    for i in listeRead:
        if (i == serverSocket):
            new_socket, adresse = serverSocket.accept()
            listeSocket.append(new_socket)
            new_socket.send(MSG_WELCOME)
            nb_user = nb_user + 1

        if (nb_user <= 2) :
            nb_joueur = nb_joueur + 1
            listeJoueur.append(new_socket)

        if (nb_user > 2) : #Spectateur, cette boucle s'execute plusieurs fois.
            listeSpec.append(new_socket)
            for i in listeSpec :
                tosend = pickle.dumps([GRID, game.grids[2]])
                i.send(tosend)

        if (nb_joueur == 2 and gaming == 0) :
            game.add_players(listeJoueur)
            gameThread = threading.Thread(target = main, args = (game, ))
            gameThread.start()
            gaming = 1
            print("thread")
            time.sleep(1)
