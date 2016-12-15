#!/usr/bin/python3

import socket
import select
import threading
import sys

listeSocket = []
listeJoueur = []

serverSocket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM, 0, None)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serverSocket.bind(('',8888))
serverSocket.listen(1)
listeSocket.append(serverSocket)

t1 = []
t2 = []
nb_joueur = 1
while(1):
    listeRead, l2 ,l3 = select.select(listeSocket, t1, t2)
    for i in listeRead:
        if (i == serverSocket):
            print (nb_joueur)
            new_socket, adresse = serverSocket.accept()
            listeSocket.append(new_socket)
            new_socket.send(bytes("Bienvenue sur le jeu du morpion aveugle. \n", 'utf-8'))
            print (len(listeJoueur))
            if (len(listeJoueur)  < 2) :
                listeJoueur.append(new_socket)
                new_socket.send(bytes("Vous êtes le joueur "+str(nb_joueur)+"\n", 'utf-8'))
                if (nb_joueur < 2) :
                    new_socket.send(bytes("En attente d'un autre joueur...\n", 'utf-8'))
                nb_joueur = nb_joueur + 1
            else :
                new_socket.send(bytes("Déjà 2 joueurs connectés. Vous êtes spectateur.\n", 'utf-8'))
