import sys
import numpy as np
import heapq
import pdb

#TODO
    # read in mixed puzzle files
    # construct puzzle data structure
    # read in moves to solve
    # verify puzzle is solvable with those moves
    # begin IDA*
    #
    # functions:
    # read_data()
    # construct_puzzle()
    # rotate()
    # flip()
    # IDA* funcs (already implemented)

# ----------------------------------------------------------------------------------------------

def read_data(files):
    top = np.genfromtxt(files['top'], delimiter=",")
    top_location = np.genfromtxt(files['top_location'], delimiter=",")
    bottom = np.genfromtxt(files['bottom'], delimiter=",")
    bottom_location = np.genfromtxt(files['bottom_location'], delimiter=",")
    steps = np.genfromtxt(files['steps'], delimiter=",", dtype=None)
    return top, top_location, bottom, bottom_location, steps

files = {
    'top': "top.csv",
    'top_location': "top_location.csv",
    'bottom': "bottom.csv",
    'bottom_location': "bottom_location.csv",
    'steps': "steps.csv"
}

top, top_location, bottom, bottom_location, steps = read_data(files)

# ----------------------------------------------------------------------------------------------

def construct_puzzle(top, top_location, bottom, bottom_location, steps):

    difference = top_location - bottom_location

    tubes = []
    for i in range(6):
        upper_index = i + difference
        if upper_index < 0:
            upper_index = 6 - (0 - upper_index)
        elif upper_index > 5:
            upper_index = upper_index - 6 ##WARNING!!!!!
        tubes.append(np.append(np.flipud(bottom[i,:]), top[upper_index,:]))

    puzzle = np.array(tubes)
    # print "after constructing..."
    # print puzzle
    # print "\n\n"
    return puzzle

puzzle = construct_puzzle(top, top_location, bottom, bottom_location, steps)

# -----------------------------------------------------------------------------------------------

def flip(puzzle):

    tubes = np.array((puzzle[0,:].copy(), puzzle[1,:].copy(), puzzle[2,:].copy(),
                        puzzle[3,:].copy(), puzzle[4,:].copy(), puzzle[5,:].copy()))

    # print puzzle
    # print "\n\n"
    for i in range(6):
        temp_tube = tubes[i]
        upper_tube_capacity = len(temp_tube[temp_tube < 99]) - (6-i)
        tube_flipped = np.flipud(temp_tube)
        puzzle[6-upper_tube_capacity,:] = tube_flipped

    # print "after flipping..."
    # print puzzle
    # print "\n\n"

    puzzle = check_if_balls_fell(puzzle)

    # print "after checking if balls fell..."
    # print puzzle
    # print "\n\n"

    return puzzle

def check_if_balls_fell(puzzle):

    for k in range(6*11):
        for i in range(6):
            for j in range(11):
                if puzzle[i,j] == 0 and puzzle[i,j+1] != 0 and puzzle[i,j+1] != 99:
                    temp_swap = puzzle[i,j]
                    puzzle[i,j] = puzzle[i,j+1]
                    puzzle[i,j+1] = temp_swap

    return puzzle

def rotate(puzzle, direction):

    tubes = np.array((puzzle[0,:].copy(), puzzle[1,:].copy(), puzzle[2,:].copy(),
                        puzzle[3,:].copy(), puzzle[4,:].copy(), puzzle[5,:].copy()))

    if direction == 0:
        next_tubes = np.array((puzzle[1,:].copy(), puzzle[2,:].copy(), puzzle[3,:].copy(),
                        puzzle[4,:].copy(), puzzle[5,:].copy(), puzzle[0,:].copy()))
    else:
        next_tubes = np.array((puzzle[5,:].copy(), puzzle[0,:].copy(), puzzle[1,:].copy(),
                            puzzle[2,:].copy(), puzzle[3,:].copy(), puzzle[4,:].copy()))

    for i in range(6):
        temp_bottom_tube = tubes[i]
        temp_bottom_tube = temp_bottom_tube[0:6]
        temp_top_tube = next_tubes[i]
        temp_top_tube = temp_top_tube[6:12]

        puzzle[i,:] = np.append(temp_bottom_tube, temp_top_tube)


    # print "before checking if balls fell..."
    # print puzzle
    # print "\n\n"
    puzzle = check_if_balls_fell(puzzle)
    # print "after checking if balls fell..."
    # print puzzle
    # print "\n\n"

    return puzzle

# puzzle = flip(puzzle)
# puzzle = rotate(puzzle,1)

# ------------------------------------------------------------------------------------------------

def verify_solvability(puzzle, steps):

    for i in range(steps.shape[0]):
        # pdb.set_trace()
        # print "puzzle solving, step #" + str(i)
        # print puzzle
        # print "\n\n"

        if steps[i] != 2:
            puzzle = rotate(puzzle, steps[i])
        else:
            puzzle = flip(puzzle)

    return puzzle

user_input = raw_input("Would you like to verify the puzzle is solvable? (Y/N) ")
print "\n\n"

steps_in_int_form = []
for i in range(steps.shape[0]-1):
    if steps[i] == 'left':
        steps_in_int_form.append(0)
    elif steps[i] == 'right':
        steps_in_int_form.append(1)
    else:
        steps_in_int_form.append(2)

steps_in_int_form = np.array(steps_in_int_form)
solved_puzzle = verify_solvability(puzzle.copy(), steps_in_int_form)

if user_input == "Y" or user_input == "y":
    print "Here's what the puzzle looks like (identical to the web interface)..."
    print puzzle
    print "\n\n"

    print "Here's after solving the puzzle using the steps given by Anton's randomizer..."
    print solved_puzzle
    print "\n\n"

# --------------------------------------------------------------------------------------------------

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
            return 1

    return 0

def balls_in_correct_place(puzzle_state, solved_puzzle):
    if is_solved(puzzle_state, solved_puzzle):
        return 0
    else:
        return 1

def compute_heuristic(puzzle_state, solved_puzzle):
    # print "computing heuristic"
    # heuristic (sum all three):
    #     1. how many tubes is the puzzle state from tubes being aligned -- max is 3
    #     2. is there balls in the top portion? 1 -- yes || 0 -- no
    #     3. are there balls in the wrong place in the bottom half? 1 -- yes || 0 -- no
    part_1 = tubes_aligned(puzzle_state)
    part_2 = balls_in_top_half(puzzle_state)
    part_3 = balls_in_correct_place(puzzle_state, solved_puzzle)
    return part_1 + part_2 + part_3

def explore_children(current_node, priority_queue, solved_puzzle):
    # print "exploring children"
    try:
        for i in range(3):

            if i == 2:
                child_node_puzzle_state = flip(current_node[2].copy())
            else:
                child_node_puzzle_state = rotate(current_node[2].copy(), i)
            # print current_node[2]
            # print "\n\n"
            # print child_node_puzzle_state
            h = compute_heuristic(child_node_puzzle_state, solved_puzzle)
            depth = current_node[1] + 1
            heapq.heappush(priority_queue, (h, depth, child_node_puzzle_state))

        return priority_queue

    except:
        pdb.set_trace()
        print "failure"

def is_solved(puzzle_state, solved_puzzle):

    verify_correctness = []
    for i in range(6):
        verify_correctness.append(np.intersect1d(puzzle_state[i,:], solved_puzzle[i,:]).shape[0])

    verify_correctness = np.array(verify_correctness)
    if verify_correctness[0] == 7 and verify_correctness[1] == 7 and verify_correctness[2] == 6 and verify_correctness[3] == 5 and verify_correctness[4] == 4 and verify_correctness[5] == 3:
        return True
    else:
        return False

def main():
    # print "main"
    priority_queue = []
    # priority_queue tuple has the following structure: heuristic, depth (or the cost), puzzle state
    heapq.heappush(priority_queue, (5,0,puzzle))
    solved = False
    starting_depth = input("Please enter the depth at which you want the IDA* search algorithm to start: ")
    depth = starting_depth - 1
    count = 0
    while not solved:
        depth = depth + 1
        current_depth = 0
        while current_depth < depth and not solved:
            current_node = heapq.heappop(priority_queue)
            # pdb.set_trace()
            np.savetxt("puzzle.csv", current_node[2], delimiter=",")
            if is_solved(current_node[2], solved_puzzle):
                solved = True
            else:
                priority_queue = explore_children(current_node, priority_queue, solved_puzzle)
                # print
            current_depth = current_depth + 1
            count = count+1
            print count
    return count

main()
pdb.set_trace()
print
