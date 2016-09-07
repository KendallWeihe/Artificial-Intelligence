#Psuedocode:
    #take user input of number of moves
    #call moves ()
    #recursively call moves() until defined number is reached
    #call main function

import pdb
import numpy as np
from random import randint

#specifications:
    #a 0 means end of tube
    #1 means empty

solved_puzzle = np.zeros((6,13))
for i in range(6):
    solved_puzzle[i,6-i:12-i*2] = 1

solved_puzzle[0,0:6] = 2
solved_puzzle[1,0:5] = 3
solved_puzzle[2,0:4] = 4
solved_puzzle[3,0:3] = 5
solved_puzzle[4,0:2] = 6
solved_puzzle[5,0:1] = 7

def main():
    #function is called by move() after k moves has been reached
    print

def make_move(num_moves, num_moves_left, puzzle):
    #make recursive move
    #check for whether or not move has reached defined number of moves
    #else make random move (out of the three)
    #then recursively call move()
    #finally call solver function
    #after each recursive call, move() needs to check if the user wants to undo another move

    #if rotate, calculate size of new arrays, generate new arrays, and fill with necessary elements
        #if tube is cut in half, move balls past threshold value into new array
    #if flip, reorder all arrays in reverse

    red_tube_temp = np.zeros((6))
    red_tube_len = 0
    green_tube_temp = np.zeros((6))
    green_tube_len = 0
    yellow_tube_temp = np.zeros((6))
    yellow_tube_len = 0
    blue_tube_temp = np.zeros((6))
    blue_tube_len = 0
    white_tube_temp = np.zeros((6))
    white_tube_len = 0
    black_tube_temp = np.zeros((6))
    black_tube_len = 0

    move = randint(1,3)
    pdb.set_trace()

    move = input("enter move: 1=flip, 2=rotate_down, 3=rotate_up")
    # print "Number of moves = " + str(k)

    if move == 1: #flip
        print "flip"
        for i in range(6):
            index = 0
            for j in range(13):
                if puzzle[i,j] == 1.0:
                    if i == 0: #red tube
                        red_tube_temp = np.flipud(puzzle[i,0:j].copy())
                        for k in range(j,13):
                            if puzzle[i,k] != 0:
                                red_tube_len = red_tube_len + 1
                        break
                    elif i == 1:
                        green_tube_temp = np.flipud(puzzle[i,0:j].copy())
                        for k in range(j,13):
                            if puzzle[i,k] != 0:
                                green_tube_len = green_tube_len + 1
                        break
                    elif i == 2:
                        yellow_tube_temp = np.flipud(puzzle[i,0:j].copy())
                        for k in range(j,13):
                            if puzzle[i,k] != 0:
                                yellow_tube_len = yellow_tube_len + 1
                        break
                    elif i == 3:
                        blue_tube_temp = np.flipud(puzzle[i,0:j].copy())
                        for k in range(j,13):
                            if puzzle[i,k] != 0:
                                blue_tube_len = blue_tube_len + 1
                        break
                    elif i == 4:
                        white_tube_temp = np.flipud(puzzle[i,0:j].copy())
                        for k in range(j,13):
                            if puzzle[i,k] != 0:
                                white_tube_len = white_tube_len + 1
                        break
                    elif i == 5:
                        black_tube_temp = np.flipud(puzzle[i,0:j].copy())
                        for k in range(j,13):
                            if puzzle[i,k] != 0:
                                black_tube_len = black_tube_len + 1
                        break

        puzzle_temp = np.empty((6,13))
        for i in range(6):
            if i == 0:
                for j in range(len(red_tube_temp)):
                    puzzle[i,j] = red_tube_temp[j]
                puzzle_temp[6-red_tube_len,:] = puzzle[i,:]
            if i == 1:
                for j in range(len(green_tube_temp)):
                    puzzle[i,j] = green_tube_temp[j]
                puzzle_temp[6-green_tube_len,:] = puzzle[i,:]
            if i == 2:
                for j in range(len(yellow_tube_temp)):
                    puzzle[i,j] = yellow_tube_temp[j]
                puzzle_temp[6-yellow_tube_len,:] = puzzle[i,:]
            if i == 3:
                for j in range(len(blue_tube_temp)):
                    puzzle[i,j] = blue_tube_temp[j]
                puzzle_temp[6-blue_tube_len,:] = puzzle[i,:]
            if i == 4:
                for j in range(len(white_tube_temp)):
                    puzzle[i,j] = white_tube_temp[j]
                puzzle_temp[6-white_tube_len,:] = puzzle[i,:]
            if i == 5:
                for j in range(len(black_tube_temp)):
                    puzzle[i,j] = black_tube_temp[j]
                puzzle_temp[6-black_tube_len,:] = puzzle[i,:]

        puzzle = puzzle_temp
        make_move(num_moves, 2, puzzle)


    elif move == 2: #rotate down
        print "rotate right"
        for i in range(6):
            for j in range(13):
                if puzzle[i,j] == 0.0:
                    if i == 0: #red tube
                        red_tube_temp = np.trim_zeros(puzzle[i,6-i:j].copy())
                    elif i == 1:
                        green_tube_temp = np.trim_zeros(puzzle[i,6-i:j].copy())
                    elif i == 2:
                        yellow_tube_temp = np.trim_zeros(puzzle[i,6-i:j].copy())
                    elif i == 3:
                        blue_tube_temp = np.trim_zeros(puzzle[i,6-i:j].copy())
                    elif i == 4:
                        white_tube_temp = np.trim_zeros(puzzle[i,6-i:j].copy())
                    elif i == 5:
                        black_tube_temp = np.trim_zeros(puzzle[i,6-i:j].copy())

        for i in range(6):
            for j in range(13):
                if i == 0:
                    #drop into red tube
                    if j == 6:
                        index = 0
                        for k in range(j,j+len(black_tube_temp)):
                            puzzle[i,k] = black_tube_temp[index]
                            index = index + 1
                        for k in range(j+len(black_tube_temp),13):
                            puzzle[i,k] = 0.0
                        break
                if i == 1:
                    if j == 5:
                        index = 0
                        for k in range(j,j+len(red_tube_temp)):
                            puzzle[i,k] = red_tube_temp[index]
                            index = index + 1
                        for k in range(j+len(red_tube_temp),13):
                            puzzle[i,k] = 0.0
                        break
                if i == 2:
                    if j == 4:
                        index = 0
                        for k in range(j,j+len(green_tube_temp)):
                            puzzle[i,k] = green_tube_temp[index]
                            index = index + 1
                        for k in range(j+len(green_tube_temp),13):
                            puzzle[i,k] = 0.0
                        break
                if i == 3:
                    if j == 3:
                        index = 0
                        for k in range(j,j+len(yellow_tube_temp)):
                            puzzle[i,k] = yellow_tube_temp[index]
                            index = index + 1
                        for k in range(j+len(yellow_tube_temp),13):
                            puzzle[i,k] = 0.0
                        break
                if i == 4:
                    if j == 2:
                        index = 0
                        for k in range(j,j+len(blue_tube_temp)):
                            puzzle[i,k] = blue_tube_temp[index]
                            index = index + 1
                        for k in range(j+len(blue_tube_temp),13):
                            puzzle[i,k] = 0.0
                        break
                if i == 5:
                    if j == 1:
                        index = 0
                        for k in range(j,j+len(white_tube_temp)):
                            puzzle[i,k] = white_tube_temp[index]
                            index = index + 1
                        for k in range(j+len(white_tube_temp),13):
                            puzzle[i,k] = 0.0
                        break

        make_move(num_moves, 2, puzzle)


    elif move == 3: #rotate up
        print "rotate left"
        for i in range(6):
            for j in range(13):
                if puzzle[i,j] == 0.0:
                    if i == 0: #red tube
                        red_tube_temp = np.trim_zeros(puzzle[i,6-i:j].copy())
                    elif i == 1:
                        green_tube_temp = np.trim_zeros(puzzle[i,6-i:j].copy())
                    elif i == 2:
                        yellow_tube_temp = np.trim_zeros(puzzle[i,6-i:j].copy())
                    elif i == 3:
                        blue_tube_temp = np.trim_zeros(puzzle[i,6-i:j].copy())
                    elif i == 4:
                        white_tube_temp = np.trim_zeros(puzzle[i,6-i:j].copy())
                    elif i == 5:
                        black_tube_temp = np.trim_zeros(puzzle[i,6-i:j].copy())

        for i in range(6):
            for j in range(13):
                if i == 0:
                    #drop into red tube
                    if j == 6:
                        index = 0
                        for k in range(j,j+len(green_tube_temp)):
                            puzzle[i,k] = green_tube_temp[index]
                            index = index + 1
                        for k in range(j+len(green_tube_temp),13):
                            puzzle[i,k] = 0.0
                        break
                if i == 1:
                    if j == 5:
                        index = 0
                        for k in range(j,j+len(yellow_tube_temp)):
                            puzzle[i,k] = yellow_tube_temp[index]
                            index = index + 1
                        for k in range(j+len(yellow_tube_temp),13):
                            puzzle[i,k] = 0.0
                        break
                if i == 2:
                    if j == 4:
                        index = 0
                        for k in range(j,j+len(blue_tube_temp)):
                            puzzle[i,k] = blue_tube_temp[index]
                            index = index + 1
                        for k in range(j+len(blue_tube_temp),13):
                            puzzle[i,k] = 0.0
                        break
                if i == 3:
                    if j == 3:
                        index = 0
                        for k in range(j,j+len(white_tube_temp)):
                            puzzle[i,k] = white_tube_temp[index]
                            index = index + 1
                        for k in range(j+len(white_tube_temp),13):
                            puzzle[i,k] = 0.0
                        break
                if i == 4:
                    if j == 2:
                        index = 0
                        for k in range(j,j+len(black_tube_temp)):
                            puzzle[i,k] = black_tube_temp[index]
                            index = index + 1
                        for k in range(j+len(black_tube_temp),13):
                            puzzle[i,k] = 0.0
                        break
                if i == 5:
                    if j == 1:
                        index = 0
                        for k in range(j,j+len(red_tube_temp)):
                            puzzle[i,k] = red_tube_temp[index]
                            index = index + 1
                        for k in range(j+len(red_tube_temp),13):
                            puzzle[i,k] = 0.0
                        break

        make_move(num_moves, 2, puzzle)

    print

# k = input("Please enter the number of moves to shuffle the puzzle: ")
# print "Number of moves = " + str(k)
# make_move(k,k,solved_puzzle)
make_move(1,1,solved_puzzle)
