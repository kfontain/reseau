#!/usr/bin/python3

from grid import *
import random

def solo():
    grids = [Grid(), Grid(), Grid()]
    current_player = J1
    grids[J1].display()
    while grids[2].gameOver() == -1:
        if current_player == J1:
            shot = -1
            while shot <0 or shot >=NB_CELLS:
                shot = int(input ("quel case allez-vous jouer ?"))
        else:
            shot = random.randint(0,8)
            while grids[current_player].cells[shot] != EMPTY:
                shot = random.randint(0,8)
        if (grids[2].cells[shot] != EMPTY):
            grids[current_player].cells[shot] = grids[2].cells[shot]
        else:
            grids[current_player].cells[shot] = current_player
            grids[2].play(current_player, shot)
            current_player = (current_player+1)%2
        if current_player == J1:
            grids[J1].display()
    print("game over")
    grids[2].display()
    if grids[2].gameOver() == J1:
        print("You win !")
    if grids[2].gameOver() == 2:
        print("Draw !")
    if grids[2].gameOver() == J2 :
        print("You lose !")
