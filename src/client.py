#!/usr/bin/python3

from grid import *
from macro import *
from main import *

import sys
import socket
import select
import pickle

def handle(msg, server) :

    code = msg[0]

    if (code == WELCOME) :
        print("Bienvenue sur le jeu du morpion aveugle.")
        return

    if (code == START) :
        print("La partie va commencer.")
        return

    if (code == PLAY) :
        test = msg[1]
        test.display()
        print("Quelle case voulez-vous jouer ?")
        print("Veuillez entrer un entier allant de 0 à 8")
        shot = input()
        server.send(bytes(str(shot).encode('utf')))
        print("Vous avez joué la case " + shot)
        return

    if (code == ERROR) :
        print("Cette case a déjà été jouée, elle a été révélée.")
        return

    if (code == GRID) :
        test = msg[1]
        test.display()
        return

    if (code == WIN) :
        print("Vous avez gagné.")
        return

    if (code == LOSE) :
        print("Vous avez perdu.")
        return

    if (code == DRAW) :
        print("Egalité.")
        return

    if (code == END) :
        print("Parti terminée. Le serveur va fermer.")
        exit()

if (len(sys.argv) == 1) :
    solo()
    exit()

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
        tmp = sock.recv(1024)
        msg = pickle.loads(tmp)
        handle(msg, sock)
