#!/usr/bin/python3

from grid import *
from macro import *

import sys
import socket
import select
import pickle

def handle(tmp, server) :

    code = tmp[0]

    if (code == WELCOME) :
        print("Bienvenue sur le jeu du morpion aveugle.")

    if (code == START) :
        print("La partie va commencer.")

    if (code == PLAY) :
        test = tmp[1]
        test.display()
        print("Quelle case voulez-vous jouer ?")
        print("Veuillez entrer un entier allant de 0 à 8")
        shot = int(input())
        server.send(bytes(str(shot).encode('utf')))
        print("Vous avez joué la case " + str(shot))

    if (code == ERROR) :
        print("Cette case a déjà été jouée, elle a été révélée.")

    if (code == GRID) :
        test = tmp[1]
        test.display()

    if (code == WIN) :
        print("Vous avez gagné.")

    if (code == LOSE) :
        print("Vous avez perdu.")

    if (code == DRAW) :
        print("Egalité.")

    if (code == END) :
        print("Parti terminée.")

host = "localhost"
port = int(sys.argv[1])

s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM, 0, None)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.connect((host, port))
s.setblocking(True)
print("connecting to port " + str(8888))

while True :
    read, _ , _ = select.select([s], [], [])
    for sock in read :
        msg = sock.recv(1024)
        tmp = pickle.loads(msg)
        handle(tmp, sock)
