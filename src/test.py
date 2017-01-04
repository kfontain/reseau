#!/usr/bin/python3

from grid import *
from macro import *

def main(listeJoueur):

    grids = [grid(), grid(), grid()]
    current_player = J1

    for j in listeJoueur :
        j.send(MSG_START)

    while grids[0].gameOver() == -1 :

        if current_player == J1 :
            shot = -1
            while shot <0 or shot >=NB_CELLS:
                tosend = pickle.dumps([PLAY, grids[current_player]])
                listeJoueur[current_player-1].send(tosend)
                shot = int(listeJoueur[J1-1].recv(1024))

        if current_player == J2 :
            shot = -1
            while shot <0 or shot >=NB_CELLS:
                tosend = pickle.dumps([PLAY, grids[current_player]])
                listeJoueur[current_player-1].send(tosend)
                shot = int(listeJoueur[J2-1].recv(1024))

        if (grids[0].cells[shot] != EMPTY):
            grids[current_player].cells[shot] = grids[0].cells[shot]
            listeJoueur[current_player-1].send(MSG_ERROR)

        else:
            grids[current_player].cells[shot] = current_player
            grids[0].play(current_player, shot)
            current_player = current_player%2+1

    winner = grids[0].gameOver()

    for j in listeJoueur :
        tosend = pickle.dumps([GRID, grids[0]])
        j.send(tosend)

    if (winner == J1) :
        listeJoueur[J1-1].send(MSG_WIN)
        listeJoueur[J2-1].send(MSG_LOSE)

    if (winner == J2) :
        listeJoueur[J1-1].send(MSG_LOSE)
        listeJoueur[J2-1].send(MSG_WIN)

    if (winner == EMPTY) :
        listeJoueur[J1-1].send(MSG_DRAW)
        listeJoueur[J2-1].send(MSG_DRAW)
