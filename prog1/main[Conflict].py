#Psuedocode:
    #take user input of number of moves
    #call moves ()
    #recursively call moves() until defined number is reached
    #call main function

import pdb
import numpy as np

#specifications:
    #a 0 means end of tube
    #1 means empty
red_tube = np.empty(6)
red_tube[:] = 2
green_tube = np.empty(5)
green_tube[:] = 3
yellow_tube = np.empty(4)
yellow_tube[:] = 4
blue_tube = np.empty(3)
blue_tube[:] = 5
white_tube = np.empty(2)
white_tube[:] = 6
black_tube = np.empty(1)
black_tube[:] = 7
pdb.set_trace()

solved_puzzle = np.empty((12,6))

solved_puzzle[12:12,10:12,8:12,6:12,4:12,2:12] = 0.0
solved_puzzle[6:12,5:10,4:8,3:6,2:4,1:2] = 1.0
pdb.set_trace()

def main():
    #function is called by move() after k moves has been reached
    print

def move(num_moves, num_moves_left, puzzle):
    #make recursive move
    #check for whether or not move has reached defined number of moves
    #else make random move (out of the three)
    #then recursively call move()
    #finally call solver function
    #after each recursive call, move() needs to check if the user wants to undo another move

    #if rotate, calculate size of new arrays, generate new arrays, and fill with necessary elements
        #if tube is cut in half, move balls past threshold value into new array
    #if flip, reorder all arrays in reverse
    print

k = input("Please enter the number of moves to shuffle the puzzle: ")
print "Number of moves = " + str(k)
moves(k,k,empty_puzzle)
