#!/usr/bin/python3

import time
import random

from grid import *
from macro import *

class Game:
    def __init__(self) :
        self.grids = [Grid(), Grid(), Grid()]
        self.players = [None, None]
        self.spectators = []

    def reset(self) :
        self.grids = [Grid(), Grid(), Grid()]

    def add_players(self, listeJoueur) :
        self.players[J1] = listeJoueur[J1]
        self.players[J2] = listeJoueur[J2]

    def add_spectators(self, listeSpec) :
        tmp = len(listeSpec)
        for i in range(tmp) :
            self.spectators[i] = listeSpec[i]


def main(game):

    game.reset()
    turn = random.randint(J1,J2)

    for j in game.players :
        j.send(MSG_START)

    while game.grids[2].gameOver() == -1 :

        if turn == J1 :
            shot = -1
            game.players[J2].send(MSG_WAIT)
            while shot <0 or shot >=NB_CELLS:
                tosend = pickle.dumps([PLAY, game.grids[turn]])
                game.players[turn].send(tosend)
                shot = int(game.players[turn].recv(1024))

        if turn == J2 :
            shot = -1
            game.players[J1].send(MSG_WAIT)
            while shot <0 or shot >=NB_CELLS:
                tosend = pickle.dumps([PLAY, game.grids[turn]])
                game.players[turn].send(tosend)
                shot = int(game.players[turn].recv(1024))

        if (game.grids[2].cells[shot] != EMPTY):
            game.grids[turn].cells[shot] = game.grids[2].cells[shot]
            game.players[turn].send(MSG_ERROR)

        else:
            game.grids[turn].cells[shot] = turn
            game.grids[2].play(turn, shot)
            turn = (turn+1)%2

    winner = game.grids[2].gameOver()

    if (winner == J1) :
        game.players[J1].send(MSG_WIN)
        game.players[J2].send(MSG_LOSE)

    if (winner == J2) :
        game.players[J1].send(MSG_LOSE)
        game.players[J2].send(MSG_WIN)

    if (winner == EMPTY) :
        game.players[J1].send(MSG_DRAW)
        game.players[J2].send(MSG_DRAW)

    for j in game.players :
        tosend = pickle.dumps([GRID, game.grids[2]])
        j.send(tosend)

    answer = 0

    for j in game.players :
        j.send(MSG_REPLAY)
        shot = int(j.recv(1024))
        answer = answer + shot
        if (answer == 2) :
            main(game)

    for j in game.players :
        j.send(MSG_END)
