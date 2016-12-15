#!/usr/bin/python3

from grid import *
import  random

def main(listeJoueur):
    grids = [grid(), grid(), grid()]
    current_player = J1
    quelle_case = bytes("Quelle case allez-vous jouer ?", 'utf-8')
    while grids[0].gameOver() == -1:
        if current_player == J1 :
            shot = -1
            while shot <0 or shot >=NB_CELLS:
                listeJoueur[J1-1].send(quelle_case)
                shot = int(listeJoueur[J1-1].recv(100))
        if current_player == J2 :
            shot = -1
            while shot <0 or shot >=NB_CELLS:
                listeJoueur[J2-1].send(quelle_case)
                shot = int(listeJoueur[J2-1].recv(100))

        if (grids[0].cells[shot] != EMPTY):
            grids[current_player].cells[shot] = grids[0].cells[shot]

        else:
            grids[current_player].cells[shot] = current_player
            grids[0].play(current_player, shot)
            current_player = current_player%2+1

        if current_player == J1:
            listeJoueur[J1-1].send()

        if current_player == J2:
            listeJoueur[J2-1].send() //Grille en bytes.

    print("game over")
    grids[0].display()
    if grids[0].gameOver() == J1:
        print("You win !")
    else:
        print("you loose !")
