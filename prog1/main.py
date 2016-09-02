#Psuedocode:
    #take user input of number of moves
    #call moves ()
    #recursively call moves() until defined number is reached
    #call main function

import pdb
import numpy as np

red_tube = np.empty(6)
red_tube[:] = 0
green_tube = np.empty(5)
green_tube[:] = 1
yellow_tube = np.empty(4)
yellow_tube[:] = 2
blue_tube = np.empty(3)
blue_tube[:] = 3
white_tube = np.empty(2)
white_tube[:] = 4
black_tube = np.empty(1)
black_tube[:] = 5
pdb.set_trace()

def main():
    #function is called by move() after k moves has been reached
    print

def move(num_moves, num_moves_left):
    #make recursive move
    #check for whether or not move has reached defined number of moves
    #else make random move (out of the three)
    #then recursively call move()
    #finally call solver function
    #after each recursive call, move() needs to check if the user wants to undo another move
    print
