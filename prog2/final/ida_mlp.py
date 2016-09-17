import sys
import numpy as np
import heapq
import pdb
import Queue as Q
from itertools import count

# ----------------------------------------------------------------------------------------------

def read_data(files):
    top = np.genfromtxt(files['top'], delimiter=",")
    top_location = np.genfromtxt(files['top_location'], delimiter=",")
    bottom = np.genfromtxt(files['bottom'], delimiter=",")
    bottom_location = np.genfromtxt(files['bottom_location'], delimiter=",")
    steps = np.genfromtxt(files['steps'], delimiter=",", dtype=None)
    return top, top_location, bottom, bottom_location, steps

files = {
    'top': "test/top.csv",
    'top_location': "test/top_location.csv",
    'bottom': "test/bottom.csv",
    'bottom_location': "test/bottom_location.csv",
    'steps': "test/steps.csv"
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
        tubes.append(np.append(np.flipud(bottom[int(i),:]), top[int(upper_index),:]))

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

def is_solved(puzzle_state, solved_puzzle):

    verify_correctness = []
    for i in range(6):
        verify_correctness.append(np.intersect1d(puzzle_state[i,:], solved_puzzle[i,:]).shape[0])

    verify_correctness = np.array(verify_correctness)
    if verify_correctness[0] == 7 and verify_correctness[1] == 7 and verify_correctness[2] == 6 and verify_correctness[3] == 5 and verify_correctness[4] == 4 and verify_correctness[5] == 3:
        return True
    else:
        return False

starting_depth = input("Please enter the depth at which you want the IDA* search algorithm to start: ")

import numpy as np
import tensorflow as tf
import pdb

'''
A Multilayer Perceptron implementation example using TensorFlow library.
This example is using the MNIST database of handwritten digits
(http://yann.lecun.com/exdb/mnist/)
Author: Aymeric Damien
Project: https://github.com/aymericdamien/TensorFlow-Examples/
'''

# Parameters
learning_rate = 0.001
training_epochs = 4000
batch_size = 7
display_step = 500

# Network Parameters
n_hidden_1 = 256 # 1st layer number of features
n_hidden_2 = 256 # 2nd layer number of features
n_input = 6 * 12 # MNIST data input (img shape: 28*28)
n_classes = 7 # MNIST total classes (0-9 digits)

# tf Graph input
x = tf.placeholder("float", [None, n_input])
y = tf.placeholder("float", [None, n_classes])

# Create model
def multilayer_perceptron(x, weights, biases):
    # Hidden layer with RELU activation
    layer_1 = tf.add(tf.matmul(x, weights['h1']), biases['b1'])
    layer_1 = tf.nn.sigmoid(layer_1)
    # Hidden layer with RELU activation
    layer_2 = tf.add(tf.matmul(layer_1, weights['h2']), biases['b2'])
    layer_2 = tf.nn.sigmoid(layer_2)
    # Output layer with linear activation
    out_layer = tf.matmul(layer_2, weights['out']) + biases['out']
    return out_layer

# Store layers weight & bias
weights = {
    'h1': tf.Variable(tf.random_normal([n_input, n_hidden_1])),
    'h2': tf.Variable(tf.random_normal([n_hidden_1, n_hidden_2])),
    'out': tf.Variable(tf.random_normal([n_hidden_2, n_classes]))
}
biases = {
    'b1': tf.Variable(tf.random_normal([n_hidden_1])),
    'b2': tf.Variable(tf.random_normal([n_hidden_2])),
    'out': tf.Variable(tf.random_normal([n_classes]))
}

# Construct model
pred = multilayer_perceptron(x, weights, biases)

# Define loss and optimizer
cost = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(pred, y))
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)

# Initializing the variables
init = tf.initialize_all_variables()

def input_data():
    puzzle_states = []
    classes = []
    for i in range(988):
        filename = "ground_truth/string_of_puzzle_states_" + str(i) + ".csv"
        puzzle_state = np.genfromtxt(filename, delimiter=",")
        if puzzle_state.shape[0] == 48:
            puzzle_states.append(puzzle_state.reshape((8,6,12)))

            filename = "ground_truth/list_of_moves_" + str(i) + ".csv"
            puzzle_class = np.genfromtxt(filename, delimiter=",")
            classes.append(puzzle_class)

    return np.array(puzzle_states), np.array(classes)

def get_batch(puzzle_states, classes, index):
    if index > puzzle_states.shape[0] - batch_size:
        index = 0

    puzzle_batch = puzzle_states[index,1:8,:,:]
    puzzle_batch = puzzle_batch.reshape((7,6*12))
    classes =  np.rot90(np.identity(7))

    return puzzle_batch, classes

def is_complete(puzzle_state, solved_puzzle):
    # print "computing heuristic"
    # heuristic (sum all three):
    #     1. how many tubes is the puzzle state from tubes being aligned -- max is 3
    #     2. is there balls in the top portion? 1 -- yes || 0 -- no
    #     3. are there balls in the wrong place in the bottom half? 1 -- yes || 0 -- no
    part_1 = tubes_aligned(puzzle_state)
    part_2 = balls_in_top_half(puzzle_state)
    part_3 = balls_in_correct_place(puzzle_state, solved_puzzle)
    return part_1 + part_2 + part_3

saver = tf.train.Saver()
index = 0
# Launch the graph
with tf.Session() as sess:
    sess.run(init)

    saver.restore(sess, "heuristic.ckpt")

    def compute_heuristic(current_node):
        # pdb.set_trace()
        prediction = sess.run(tf.nn.sigmoid(pred), feed_dict={x: current_node.reshape((1,72))})
        return np.argmax(prediction)

    def explore_children(current_node, priority_queue, solved_puzzle, tiebreaker):
        # print "exploring children"
        try:
            for i in range(3):

                if i == 2:
                    child_node_puzzle_state = flip(current_node[4].copy())
                else:
                    child_node_puzzle_state = rotate(current_node[4].copy(), i)
                # print current_node[4]
                # print "\n\n"
                # print child_node_puzzle_state
                h = is_complete(child_node_puzzle_state, solved_puzzle)
                depth = current_node[1] + 1
                f = h + depth
                moves_to_solve = np.array(current_node[3]).copy()
                moves_to_solve = np.append(moves_to_solve, i)
                string_of_puzzle_states = np.array(current_node[5]).copy()
                string_of_puzzle_states = np.vstack((string_of_puzzle_states, child_node_puzzle_state))
                # pdb.set_trace()
                heapq.heappush(priority_queue, [f, depth, next(tiebreaker), moves_to_solve, child_node_puzzle_state, string_of_puzzle_states])
                # priority_queue.put((f, depth, child_node_puzzle_state))

            return priority_queue

        except:
            pdb.set_trace()
            print "explore_children failed"

    solved = False
    depth = starting_depth - 1
    move_count = 0
    while not solved:
        # priority_queue structue: f, depth, tiebreaker, moves to solve, current puzzle,  previous puzzle states
        priority_queue = []
        heapq.heappush(priority_queue, (5,0,-1,[0], puzzle, puzzle))
        depth = depth + 1
        current_depth = 0
        tiebreaker = count()
        while current_depth < depth and not solved:
            current_node = heapq.heappop(priority_queue)
            # current_node = priority_queue.get()
            # pdb.set_trace()
            # np.savetxt("puzzle.csv", current_node[4], delimiter=",")
            h = is_complete(current_node[4], solved_puzzle)

            # if is_solved(current_node[4], solved_puzzle):
            if h == 0:
                solved = True
            else:
                priority_queue = explore_children(current_node, priority_queue, solved_puzzle, tiebreaker)
                # print
            current_depth = current_node[1] + 1
            move_count = move_count+1
            # pdb.set_trace()

            if move_count % 100 == 0:
                print move_count

    print "Success!"
    print "Depth = " + str(current_node[1])
    print "Solved puzzle: "
    print current_node[4]

# at this point we have found the optimal solution
# print out the depth
# then do the moves in reverse to verify
