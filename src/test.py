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

listeSocket = []
listeJoueur = []
listeSpec   = []

serverSocket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM, 0, None)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serverSocket.bind(('', 8888))
serverSocket.listen(1)
listeSocket.append(serverSocket)

nb_client = 0
nb_joueur = 0
game = Game()

turn = J1
start = 0

while(1) :
    print("début boucle")

    listeRead, _ , _ = select.select(listeSocket, [], [])
    for i in listeRead:
        if (i == serverSocket):
            new_socket, adresse = serverSocket.accept()
            listeSocket.append(new_socket)
            nb_client = nb_client + 1

        print("accept done")
        if (nb_joueur < 2) :
            listeJoueur.append(new_socket)
            nb_joueur = nb_joueur + 1

        """listeSpec.append(new_socket)
        game.add_spectators(listeSpec)"""

        if (nb_joueur == 2) :

            if (game.grids[2].gameOver() == -1) :

                if (start == 0) :
                    print("2 joueurs, la partie va commencer")
                    game.add_players(listeJoueur)
                    start = 1
                    for j in game.players :
                        j.send(MSG_START)

                game.grids[2].display()

                if turn == J1 :
                    print("Tour du joueur 1, valeur : " + str(turn))
                    shot = -1
                    while shot <0 or shot >=NB_CELLS:
                        tosend = pickle.dumps([PLAY, game.grids[turn]])
                        game.players[turn].send(tosend)
                        shot = int(game.players[turn].recv(1024))
                        print("coup recu :" + str(shot))

                if turn == J2 :
                    print("Tour du joueur 2, valeur : " + str(turn))
                    shot = -1
                    while shot <0 or shot >=NB_CELLS:
                        tosend = pickle.dumps([PLAY, game.grids[turn]])
                        game.players[turn].send(tosend)
                        shot = int(game.players[turn].recv(1024))
                        print("coup recu :" + str(shot))

                if (game.grids[2].cells[shot] != EMPTY):
                    game.grids[turn].cells[shot] = game.grids[2].cells[shot]
                    game.players[turn].send(MSG_ERROR)

                else:
                    game.grids[turn].cells[shot] = turn
                    game.grids[2].play(turn, shot)
                    turn = (turn+1)%2
                    print("prochain tour : " + str(turn))

                winner = game.grids[2].gameOver()
                print("winner calculé : " + str(winner))

                if (winner == J1) :
                    game.players[J1].send(MSG_WIN)
                    game.players[J2].send(MSG_LOSE)

                if (winner == J2) :
                    game.players[J1].send(MSG_LOSE)
                    game.players[J2].send(MSG_WIN)

                if (winner == EMPTY) :
                    game.players[J1].send(MSG_DRAW)
                    game.players[J2].send(MSG_DRAW)

    print("fin boucle")
for j in game.players :
    tosend = pickle.dumps([GRID, game.grids[2]])
    j.send(tosend)

for j in game.players :
    j.send(MSG_END)
    time.sleep(1)
