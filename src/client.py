#!/usr/bin/python3

from grid import *
from macro import *
from main import *

import sys
import socket
import select
import pickle

def handle(msg, server) :
    #Cette fonction prend en premier paramètre le tableau envoyé depuis le serveur.
    #Le deuxième paramètre est le serveur en question.
    code = msg[0] #Première case des données reçues détermine le comportement.

    if (code == WELCOME) :
        print("Bienvenue sur le jeu du morpion aveugle.")
        return

    if (code == START) :
        print("La partie va commencer.")
        return

    if (code == SPEC) :
        print("Deja une partie en cours, vous serez spectateur de la prochaine partie.")

    if (code == PLAY) :
        test = msg[1] #Affiche la grille reçue.
        test.display()
        print("Quelle case voulez-vous jouer ?")
        print("Veuillez entrer un entier allant de 0 à 8")
        shot = input()
        server.send(bytes(str(shot).encode('utf'))) #Envoie le coup joué sous forme d'octets.
        print("Vous avez joué la case " + shot)
        return

    if (code == WAIT) :
        print("C'est au tour de votre adversaire...")

    if (code == REPLAY) :
        print("Souhaitez-vous rejouer une partie ?")
        print("Tapez 1 pour rejouer, 0 sinon.")
        shot = input()
        tmp = int(shot)
        server.send(bytes(str(shot).encode('utf'))) #Même fonctionnement que dans le cas PLAY.
        if (tmp == 1) :
            print("Une nouvelle partie commencera si votre adversaire veut aussi rejouer.")
            return
        else :
            print("Merci d'avoir joué.")
            exit()


    if (code == ERROR) :
        print("Cette case a déjà été jouée, elle a été révélée.")
        return

    if (code == GRID) :
        tmp = msg[1]
        tmp.display()
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
        print("Parti terminée, merci d'avoir jouer.")
        exit()

if (len(sys.argv) == 1) : #Sans argument = partie en solo
    solo() #fonction solo du fichier main.py
    exit()

host = "localhost" #Peut ne pas marcher, à remplacer par "::1" (avec les quotes) dans ce cas.
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
