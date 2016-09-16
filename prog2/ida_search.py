# Author: Kendall Weihe
# Date: September 16th, 2016
# Program: Atomic Chaos Puzzle solver using the IDA* search algorithm

# General flow of control: (see psuedocode for each section below)
#     - read in puzzle state from files passed as program arguments
#     - construct the puzzle in a numpy array
#     - solve the puzzle by taking k steps backwards
#         - the solved state is used in various parts of the program
#     - execute IDA* search algorithm


import numpy as np
import heapq
import pdb
import sys
from itertools import count

print "Welcome to the IDA* search algorithm for the Atomic Chaos puzzle!"

# READ IN CSV FILE ----------------------------------------------------------------------------------------------
# Psueodcode:
#     - use the numpy `genfromtxt()` function to read in CSV files
#     - return arrays -- one for each file

def read_data(files):
    top = np.genfromtxt(files['top'], delimiter=",") # numpy is the BEST!
    top_location = np.genfromtxt(files['top_location'], delimiter=",")
    bottom = np.genfromtxt(files['bottom'], delimiter=",")
    bottom_location = np.genfromtxt(files['bottom_location'], delimiter=",")
    steps = np.genfromtxt(files['steps'], delimiter=",", dtype=None)
    return top, top_location, bottom, bottom_location, steps

files = {
    'top': sys.argv[1],
    'top_location': sys.argv[2],
    'bottom': sys.argv[3],
    'bottom_location': sys.argv[4],
    'steps': sys.argv[5]
}

top, top_location, bottom, bottom_location, steps = read_data(files)

# CONSTRUCT PUZZLE FROM CSV FILE  ----------------------------------------------------------------------------------------------
# PsueodcodeL
#     - compute the misalignment from Anton's randomizer
#     - iterate over each tube and append entire tube (top and bottom) to the output matrix
#     - return 6x12 puzzle matrix

def construct_puzzle(top, top_location, bottom, bottom_location):

    difference = top_location - bottom_location # the misalignment from Anton's randomizer

    tubes = [] # temporary list to hold the entire tubes
    for i in range(6):
        upper_index = i + difference
        if upper_index < 0: # since the puzzle is a circle, we have to make sure the index loops
            upper_index = 6 - (0 - upper_index)
        elif upper_index > 5:
            upper_index = upper_index - 6
        tubes.append(np.append(np.flipud(bottom[int(i),:]), top[int(upper_index),:])) # bottom tube has to be flipped -- Anton's randomizer

    puzzle = np.array(tubes) # define as numpy array
    return puzzle

puzzle = construct_puzzle(top, top_location, bottom, bottom_location)

# MAKE PHYSICAL MOVES  -----------------------------------------------------------------------------------------------
# Psuedocode:
#     flip():
#         - define temporary tube variables (current_state)
#         - iterate over 6 tubes
#             - compute the capacity of the upper tube
#             - flip the tube (order)
#             - assign entire tube to the index from the capacity of the original upper tube
#         - call function to check if any balls fell
#         - return puzzle
#     check_if_balls_fell():
#         - use a simple comparison along side of Bubble Sort to move balls into the lower half of the puzzle
#         - return puzzle
#     rotate():
#         - define temporary tubes (current state)
#         - depending on the direction, assign tempory tubes for the next tubes over
#         - iterate over 6 tubes
#             - temporary variable for the bottom half of the current tubes
#             - temporary variable for the upper half of the next tube over
#             - append temporary variables and assign to puzzle[]
#         - call function to check if any balls fell
#         - return puzzle

def flip(puzzle):

    tubes = np.array((puzzle[0,:].copy(), puzzle[1,:].copy(), puzzle[2,:].copy(),
                        puzzle[3,:].copy(), puzzle[4,:].copy(), puzzle[5,:].copy())) # temporary variables

    for i in range(6):
        temp_tube = tubes[i]
        upper_tube_capacity = len(temp_tube[temp_tube < 99]) - (6-i) # capacity of the upper tube -- used to assign new puzzle index (remember that the index indicates the capacity of the lower tube)
        tube_flipped = np.flipud(temp_tube) # reverse the order
        puzzle[6-upper_tube_capacity,:] = tube_flipped # assign to the (potentially) new index

    puzzle = check_if_balls_fell(puzzle) # check if any balls fell -- of course they did!

    return puzzle

def check_if_balls_fell(puzzle):

    for k in range(6*11):
        for i in range(6):
            for j in range(11):
                if puzzle[i,j] == 0 and puzzle[i,j+1] != 0 and puzzle[i,j+1] != 99: # there is a empty space below a ball and the next ball isn't 99 -- nonexistent
                    temp_swap = puzzle[i,j] # swap inspired by Bubble Sort
                    puzzle[i,j] = puzzle[i,j+1]
                    puzzle[i,j+1] = temp_swap

    return puzzle

def rotate(puzzle, direction):

    tubes = np.array((puzzle[0,:].copy(), puzzle[1,:].copy(), puzzle[2,:].copy(),
                        puzzle[3,:].copy(), puzzle[4,:].copy(), puzzle[5,:].copy())) # temporary tubes for the lower half

    if direction == 0:
        next_tubes = np.array((puzzle[1,:].copy(), puzzle[2,:].copy(), puzzle[3,:].copy(), # temporary tubes for the upper half
                        puzzle[4,:].copy(), puzzle[5,:].copy(), puzzle[0,:].copy()))
    else:
        next_tubes = np.array((puzzle[5,:].copy(), puzzle[0,:].copy(), puzzle[1,:].copy(),
                            puzzle[2,:].copy(), puzzle[3,:].copy(), puzzle[4,:].copy()))

    for i in range(6):
        temp_bottom_tube = tubes[i]
        temp_bottom_tube = temp_bottom_tube[0:6] # grab the lower half
        temp_top_tube = next_tubes[i]
        temp_top_tube = temp_top_tube[6:12] # grab the upper half

        puzzle[i,:] = np.append(temp_bottom_tube, temp_top_tube) # append and assign to puzzle[]


    puzzle = check_if_balls_fell(puzzle) # check if any balls fell

    return puzzle

# SOLVE BACKWARDS  ------------------------------------------------------------------------------------------------
# Psuedocode:
#     - read in the steps required to solve it backwards -- provided by Anton's randomizer
#     - call solve_backwards()
#     - ask the user if they would like proof that it is solvable
#     - solve_backwards()
#         - iterate over the number of steps
#             - depending on the state, call the physical moves to go in reverse

def solve_backwards(puzzle, steps):

    for i in range(steps.shape[0]):

        if steps[i] != 2: # step 2 means flip, steps 0 and 1 are rotate (opposite directions)
            puzzle = rotate(puzzle, steps[i])
        else:
            puzzle = flip(puzzle)

    return puzzle

steps_in_int_form = []
for i in range(steps.shape[0]-1):
    if steps[i] == 'left':
        steps_in_int_form.append(0)
    elif steps[i] == 'right':
        steps_in_int_form.append(1)
    else:
        steps_in_int_form.append(2)

steps_in_int_form = np.array(steps_in_int_form)
solved_puzzle = solve_backwards(puzzle.copy(), steps_in_int_form) # the solved puzzle is used throughout the program

# uncomment the below line if you want to verify the puzzle is solvable
user_input = "n"
# user_input = raw_input("Would you like to verify the puzzle is solvable? (Y/N) ")
if user_input == "Y" or user_input == "y":
    print "\n\n"
    print "Here's what the puzzle looks like (identical to the web interface)..."
    print puzzle
    print "\n\n"

    print "Here's after solving the puzzle using the steps given by Anton's randomizer..."
    print solved_puzzle
    print "\n\n"

# IDA*  --------------------------------------------------------------------------------------------------
# Psuedocode:
#     - general flow of control
#         - main() loops until solution
#             - calls function to explore children
#         - explore_children() explores three children nodes
#             - calls function to make physical move
#             - calls function to compute heuristic (after physical move)
#         - compute_heuristic() computes the h value
#             - calls three other functions to compute the three parts of the heuristic (see README)
#
#     - main()
#         - loop until the solution is found -- when h = 0
#             - insert root into heap
#             - loop until the depth of the current node reaches the IDA* depth threshold
#                 - pop of the first node in the priority_queue
#                 - compute heuristic
#                 - if h == 0, then solved
#                 - else explore the children
#             - return current_node
#
#     - explore_children()
#         - iterate over three possible moves / children
#         - make physical move
#         - compute new h value
#         - increment depth from parent
#         - compute f (f = g + h)
#         - append the current move to the parent nodes moves_to_solve list (located in priority_queue node)
#         - add the child to the string_of_puzzle_states back to the root
#         - insert the child into the heap
#         - return priority_queue
#
#     - compute_heuristic()
#         - call three functions
#         - sum results
#         - return results
#
#     - tubes_aligned()
#         - use tube at index 3 for comparison purposes
#         - compute capacity of upper tube
#         - compute the correct index (what index the bottom tube would have to turn to in order to be aligned)
#         - iterate over tubes 0-2
#             - if i == correct_index then distance is the current index (3) minus i
#                 - set flag found to true
#         - if index still not found
#             - iterate over tubes 5-3
#                 - same comparison, but this time distance = i - current_index (3)
#         - return distance
#
#     - balls_in_top_half()
#         - compute the total number of balls
#         - subtract the number of balls from the capacity of the current lower tube
#         - if any of the computations != 0 then return 1
#         - else return 0
#
#     - balls_in_correct_place()
#         - take the intersection of each tube with the solved tube (this way order doesn't matter)
#         - if the intersection values are consistent with a solved puzzle, then return 0
#         - else return 1

def tubes_aligned(puzzle_state):

    current_index = 3 #test for index 3
    blue_tube = puzzle_state[3,:]
    len_of_top_tube = len(blue_tube[blue_tube < 99]) - 3
    correct_index = 6 - len_of_top_tube

    found = False
    distance = 3
    for i in range(3):
        if i == correct_index:
            distance = current_index - i
            found = True

    if not found:
        for i in range(5,2,-1):
            if i == correct_index:
                distance = i - current_index

    return distance

def balls_in_top_half(puzzle_state):

    for i in range(6):
        full_tube = puzzle_state[i,:]
        num_balls = full_tube[full_tube < 99]
        num_balls = len(num_balls[num_balls > 0])
        if (6 - i - num_balls) != 0:
            return 1 # if any of the tubes are filled past the lower tube capacity then return 1

    return 0

def balls_in_correct_place(puzzle_state, solved_puzzle):

    verify_correctness = []
    for i in range(6):
        verify_correctness.append(np.intersect1d(puzzle_state[i,:], solved_puzzle[i,:]).shape[0]) # intersection

    verify_correctness = np.array(verify_correctness)
    if verify_correctness[0] == 7 and verify_correctness[1] == 7 and verify_correctness[2] == 6 and verify_correctness[3] == 5 and verify_correctness[4] == 4 and verify_correctness[5] == 3:
        return 0
    else:
        return 1

def compute_heuristic(puzzle_state, solved_puzzle):
    # heuristic (sum all three):
    #     1. how many rotations is the puzzle state from tubes being aligned -- max is 3
    #     2. is there balls in the top portion? 1 -- yes || 0 -- no
    #     3. are there balls in the wrong place in the bottom half? 1 -- yes || 0 -- no
    part_1 = tubes_aligned(puzzle_state)
    part_2 = balls_in_top_half(puzzle_state)
    part_3 = balls_in_correct_place(puzzle_state, solved_puzzle)
    return part_1 + part_2 + part_3

def explore_children(current_node, priority_queue, solved_puzzle, tiebreaker):
    try:
        for i in range(3):

            if i == 2:
                child_node_puzzle_state = flip(current_node[4].copy())
            else:
                child_node_puzzle_state = rotate(current_node[4].copy(), i)

            h = compute_heuristic(child_node_puzzle_state, solved_puzzle)
            depth = current_node[1] + 1
            f = h + depth
            moves_to_solve = np.array(current_node[3]).copy()
            moves_to_solve = np.append(moves_to_solve, i)
            string_of_puzzle_states = np.array(current_node[5]).copy() # used for the MLP training
            string_of_puzzle_states = np.vstack((string_of_puzzle_states, child_node_puzzle_state))
            heapq.heappush(priority_queue, [f, depth, next(tiebreaker), moves_to_solve, child_node_puzzle_state, string_of_puzzle_states])

        return priority_queue

    except:
        pdb.set_trace()
        print "explore_children failed"

# MAIN  --------------------------------------------------------------------------------------------------
# Pseudocode: see psuedocode from IDA* section

def main(starting_depth):
    solved = False
    depth = starting_depth - 1
    while not solved:
        # priority_queue structue: f, depth, tiebreaker, moves to solve, current puzzle,  previous puzzle states
        priority_queue = []
        heapq.heappush(priority_queue, (5,0,-1,[0], puzzle, puzzle))
        depth = depth + 1
        current_depth = 0
        tiebreaker = count()
        print "Current maximum depth: " + str(depth)
        while current_depth < depth and not solved:
            current_node = heapq.heappop(priority_queue)
            h = compute_heuristic(current_node[4], solved_puzzle)

            if h == 0:
                solved = True
            else:
                priority_queue = explore_children(current_node, priority_queue, solved_puzzle, tiebreaker)

            current_depth = current_node[1] + 1

    print "The puzzle has been solved!"
    print "The depth to the solution is: " + str(current_node[1])
    print "\n"
    print current_node[4]
    return current_node

# uncomment the below line to set custom starting depth
# starting_depth = input("Please enter the depth at which you want the IDA* search algorithm to start: ")
starting_depth = 5
solved_node = main(starting_depth)
