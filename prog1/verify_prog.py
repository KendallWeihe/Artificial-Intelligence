
import numpy as np
import pdb

puzzle = np.zeros((6,13))
for i in range(6):
    puzzle[i,6-i:12-i*2] = 1

puzzle[0,0:6] = 2
puzzle[1,0:5] = 3
puzzle[2,0:4] = 4
puzzle[3,0:3] = 5
puzzle[4,0:2] = 6
puzzle[5,0:1] = 7

def find_filled_tubes(puzzle):
    try:
        filled_tubes = []
        for i in range(6):
            #scan i iterations, if full add to return array
            filled = 0
            tube_count = 6-i
            for j in range(13):
                if filled == tube_count:
                    #we have reached the fill line
                    filled_tubes.append(i)
                    break
                if puzzle[i,j] != 1:
                    filled = filled + 1
                if puzzle[i,j] ==  0:
                    break

        return filled_tubes
    except:
        pdb.set_trace()

#extract random number of filled tubes
def extract_rand_num_of_filled_tubes(filled_tubes):
    try:
        rand_size = np.random.randint(1,max(len(filled_tubes),2))
    except:
        pdb.set_trace()
    filled_tubes_random = np.random.choice(filled_tubes, rand_size, 0)
    filled_tubes_random = np.sort(filled_tubes_random)
    return filled_tubes_random

#verify that no tubes where balls have been dropped are adjacent in the
    #in the direction of the turn
def verify_adjacent_tubes(filled_tubes_random):
    # add 1 to all values
    # loop through
    # if [i]+1 == [i+1]
    #     random, set it to zero
    # delete all zeros
    #     arr[arr > 0]
    # decrement all values by 1
    # filled_tubes_random = np.array([0,1,2,3,4,5])
    filled_tubes_random = filled_tubes_random + 1
    for i in range(len(filled_tubes_random)-1):
        if filled_tubes_random[i]+1 == filled_tubes_random[i+1]:
            rand_deletion = np.random.randint(2)
            filled_tubes_random[i+rand_deletion] = 0

    if filled_tubes_random[0] == filled_tubes_random[len(filled_tubes_random)-1]-5:
            rand_deletion = np.random.randint(2)
            if rand_deletion == 0:
                filled_tubes_random[0] = 0
            else:
                filled_tubes_random[len(filled_tubes_random)-1] = 0

    filled_tubes_random = filled_tubes_random[filled_tubes_random > 0]
    filled_tubes_random = filled_tubes_random - 1
    return filled_tubes_random

def generate_random_ball_drops(potential_dropped_tubes, puzzle, direction):
    #generate random extraction from filled_tubes_verified
    #iterate through index's defined above ^^
            #the actual tube where the balls dropped will be adajcent to the above iteration values^^
        #generate random number where the range is min(actual balls,size_of_upper_tube)
            #this will be the number of balls that were dropped in that tube
        #splice off that ^^ number of the balls on top
        #fill in those balls in a tube size of the upper tube
        #blank puzzle index beyond this point
    #iterate through the index's not defined above ^^
        #splice off all values above the fill line
    #by this point we will have temp variables where all we need to do is place them above the fill lines of the puzzle

    upper_red_tube = np.zeros((6))
    upper_green_tube = np.zeros((6))
    upper_yellow_tube = np.zeros((6))
    upper_blue_tube = np.zeros((6))
    upper_white_tube = np.zeros((6))
    upper_black_tube = np.zeros((6))
    if direction == 0:
        potential_dropped_tubes = potential_dropped_tubes + 1
        if 6 in potential_dropped_tubes:
            potential_dropped_tubes[len(potential_dropped_tubes)-1] = 0
    else:
        potential_dropped_tubes = potential_dropped_tubes - 1
        if -1 in potential_dropped_tubes:
            potential_dropped_tubes[0] = 5

    for i in range(len(potential_dropped_tubes)):
        try:
            temp_vector = puzzle[potential_dropped_tubes[i],:].copy()
        except:
            pdb.set_trace()
            print "fail"
        num_balls_in_tube = len(temp_vector[temp_vector > 1])
        end_of_tube = len(temp_vector[temp_vector > 0]) - 1
        size_of_upper_tube = end_of_tube - (5 - potential_dropped_tubes[i])
        # if filled_tubes_verified[i] == 5:
        #we must loop back around to the red tube
        try:
            rand_num_balls = np.random.randint(0,(min(num_balls_in_tube, size_of_upper_tube-1)+1))
        except:
            pdb.set_trace()
            print "failed rand"
        #extract the previous upper_tube
        # pdb.set_trace()
        prev_upper_tube = puzzle[potential_dropped_tubes[i],
                    6-potential_dropped_tubes[i]-rand_num_balls:6-potential_dropped_tubes[i]].copy()
        #remove the rand_num_balls from the current tube
        # pdb.set_trace()
        puzzle[potential_dropped_tubes[i],6-potential_dropped_tubes[i]-rand_num_balls:end_of_tube] = 1
        if potential_dropped_tubes[i] == 0:
            upper_red_tube = prev_upper_tube
        elif potential_dropped_tubes[i] == 1:
            upper_green_tube = prev_upper_tube
        elif potential_dropped_tubes[i] == 2:
            upper_yellow_tube = prev_upper_tube
        elif potential_dropped_tubes[i] == 3:
            upper_blue_tube = prev_upper_tube
        elif potential_dropped_tubes[i] == 4:
            upper_white_tube = prev_upper_tube
        elif potential_dropped_tubes[i] == 5:
            upper_black_tube = prev_upper_tube

        print

    for j in range(5,0,-1):
        temp = puzzle[j,:].copy()
        if len(temp[temp>0]) == 6-j or len(temp[temp>0]) < 6-j:
            pdb.set_trace()
            print "wrong1.0"

    output = []
    try:
        for i in range(len(potential_dropped_tubes)):
            if potential_dropped_tubes[i] == 0:
                output.append(upper_red_tube)
            elif potential_dropped_tubes[i] == 1:
                output.append(upper_green_tube)
            elif potential_dropped_tubes[i] == 2:
                output.append(upper_yellow_tube)
            elif potential_dropped_tubes[i] == 3:
                output.append(upper_blue_tube)
            elif potential_dropped_tubes[i] == 4:
                output.append(upper_white_tube)
            elif potential_dropped_tubes[i] == 5:
                output.append(upper_black_tube)

        return np.asarray(output), potential_dropped_tubes
    except:
        pdb.set_trace()
        print "failed"

def rotate(current_tube, previous_tube, i, balls_that_fell, index_fell_from, direction):

    try:
        if direction == 0:
            if i == 0: prev_tube_index = 5
            else: prev_tube_index = i-1
        else:
            if i == 5: prev_tube_index = 0
            else: prev_tube_index = i+1

        prev_tube = previous_tube
        len_of_prev_upper_tube = len(prev_tube[prev_tube > 0]) - (6-prev_tube_index)
        end_of_balls_index = len(current_tube[current_tube > 1])
        len_new_tube = (6-i) + len_of_prev_upper_tube
        if prev_tube_index in index_fell_from:
            index_balls_fell_from = np.where(index_fell_from == prev_tube_index)[0][0]
            num_that_fell = len(balls_that_fell[index_balls_fell_from])
            puzzle[i, min(end_of_balls_index,6-i):min(end_of_balls_index,6-i)+num_that_fell] = balls_that_fell[index_balls_fell_from]
            puzzle[i, min(end_of_balls_index,6-i)+num_that_fell:len_new_tube] = 1

        else:
            puzzle[i,min(end_of_balls_index,6-i):min(end_of_balls_index,6-i)+len_of_prev_upper_tube] = prev_tube[6-prev_tube_index:6-prev_tube_index+len_of_prev_upper_tube]
            puzzle[i,min(end_of_balls_index,6-i)+len_of_prev_upper_tube:len_new_tube] = 1
        puzzle[i,len_new_tube:13] = 0

        return puzzle
    except:
        pdb.set_trace()
        print "broadcast error"

def call_rotate(puzzle, direction):

    # rotate pseudocode:
    #     store copies of each tube
    #     iterate through puzzle
    #     call function (one for each direction) with params:
    #         tube copy
    #         index (i) [indicates tube number]
    #         length of upper tube
    #         balls_that_fell
    #         index_fell_from

    filled_tubes = find_filled_tubes(puzzle)
    filled_tubes_random = extract_rand_num_of_filled_tubes(filled_tubes)
    filled_tubes_verified = verify_adjacent_tubes(filled_tubes_random)
    balls_that_fell, index_fell_from = generate_random_ball_drops(filled_tubes_verified, puzzle, 0)

    current_tubes = {
        0: puzzle[0,:].copy(),
        1: puzzle[1,:].copy(),
        2: puzzle[2,:].copy(),
        3: puzzle[3,:].copy(),
        4: puzzle[4,:].copy(),
        5: puzzle[5,:].copy()
    }

    if direction == 0:
        previous_tubes = {
            0: puzzle[5,:].copy(),
            1: puzzle[0,:].copy(),
            2: puzzle[1,:].copy(),
            3: puzzle[2,:].copy(),
            4: puzzle[3,:].copy(),
            5: puzzle[4,:].copy()
        }
    else:
        previous_tubes = {
            0: puzzle[1,:].copy(),
            1: puzzle[2,:].copy(),
            2: puzzle[3,:].copy(),
            3: puzzle[4,:].copy(),
            4: puzzle[5,:].copy(),
            5: puzzle[0,:].copy()
        }

    for i in range(6):
        puzzle = rotate(current_tubes[i], previous_tubes[i], i, balls_that_fell, index_fell_from, direction)

    return puzzle

def flip(puzzle):
    print "flip"
    puzzle_temp = np.zeros((6,13))
    red_tube = puzzle[0,:].copy()
    green_tube = puzzle[1,:].copy()
    yellow_tube = puzzle[2,:].copy()
    blue_tube = puzzle[3,:].copy()
    white_tube = puzzle[4,:].copy()
    black_tube = puzzle[5,:].copy()

    for j in range(5,0,-1):
        temp = puzzle[j,:].copy()
        if len(temp[temp>0]) == 6-j or len(temp[temp>0]) < 6-j:
            pdb.set_trace()
            print "wrong3.0"

    try:
        for i in range(6):
            if i == 0:
                # find the size of the top tube
                # flip
                # reorder 0's and 1's
                # store in index ^^
                size_vector = red_tube[6:13]
                top_tube_size = len(size_vector[size_vector > 0])
                flip_vector = red_tube[red_tube > 1]
                flip_vector = np.flipud(flip_vector)
                red_tube[0:len(flip_vector)] = flip_vector
                puzzle[6-top_tube_size,:] = red_tube
            if i == 1:
                size_vector = green_tube[5:13]
                top_tube_size = len(size_vector[size_vector > 0])
                flip_vector = green_tube[green_tube > 1]
                flip_vector = np.flipud(flip_vector)
                green_tube[0:len(flip_vector)] = flip_vector
                puzzle[6-top_tube_size,:] = green_tube
            if i == 2:
                size_vector = yellow_tube[4:13]
                top_tube_size = len(size_vector[size_vector > 0])
                flip_vector = yellow_tube[yellow_tube > 1]
                flip_vector = np.flipud(flip_vector)
                yellow_tube[0:len(flip_vector)] = flip_vector
                puzzle[6-top_tube_size,:] = yellow_tube
            if i == 3:
                size_vector = blue_tube[3:13]
                top_tube_size = len(size_vector[size_vector > 0])
                flip_vector = blue_tube[blue_tube > 1]
                flip_vector = np.flipud(flip_vector)
                blue_tube[0:len(flip_vector)] = flip_vector
                puzzle[6-top_tube_size,:] = blue_tube
            if i == 4:
                size_vector = white_tube[2:13]
                top_tube_size = len(size_vector[size_vector > 0])
                flip_vector = white_tube[white_tube > 1]
                flip_vector = np.flipud(flip_vector)
                white_tube[0:len(flip_vector)] = flip_vector
                puzzle[6-top_tube_size,:] = white_tube
            if i == 5:
                size_vector = black_tube[1:13]
                top_tube_size = len(size_vector[size_vector > 0])
                flip_vector = black_tube[black_tube > 1]
                flip_vector = np.flipud(flip_vector)
                black_tube[0:len(flip_vector)] = flip_vector
                puzzle[6-top_tube_size,:] = black_tube

        for j in range(5,0,-1):
            temp = puzzle[j,:].copy()
            if len(temp[temp>0]) == 5-j or len(temp[temp>0]) < 5-j:
                pdb.set_trace()
                print "wrong4.0"


        return puzzle

    except:
        pdb.set_trace()
        print "failed 1.0"

# puzzle = call_rotate(puzzle, 0)
# pdb.set_trace()
# puzzle = call_rotate(puzzle, 1)
# pdb.set_trace()
# puzzle = flip(puzzle)
# pdb.set_trace()
# puzzle = call_rotate(puzzle, 0)
# pdb.set_trace()
# puzzle = flip(puzzle)
# pdb.set_trace()
# puzzle = call_rotate(puzzle, 0)
# pdb.set_trace()
print

def rotate_normal(puzzle,direction):
    # store temps for each tube
    # for each tube
    #     find size of upper tube
    #     find end of balls of next tube
    #     find length of new tube
    #     place in range min(eob,fill line) to min(eob,fill_line)+size_of_upper_tube
    tubes = {
        0: puzzle[0,:].copy(),
        1: puzzle[1,:].copy(),
        2: puzzle[2,:].copy(),
        3: puzzle[3,:].copy(),
        4: puzzle[4,:].copy(),
        5: puzzle[5,:].copy()
    }
    pdb.set_trace()
    for i in range(6):
        if direction == 0:
            if i == 5: prev_tube_index = 0
            else: prev_tube_index = i+1
        else:
            if i == 0: prev_tube_index = 5
            else: prev_tube_index = i-1

        prev_tube = tubes[prev_tube_index]
        len_of_prev_upper_tube = len(prev_tube[prev_tube > 0]) - (6-prev_tube_index)
        current_tube = tubes[i]
        end_of_balls_index = len(current_tube[current_tube > 1])
        len_new_tube = (6-i) + len_of_prev_upper_tube

        puzzle[i, min(end_of_balls_index,(6-i)):min(end_of_balls_index,(6-i))+len_of_prev_upper_tube] = prev_tube[(6-prev_tube_index):(6-prev_tube_index)+len_of_prev_upper_tube]
        puzzle[i, min(end_of_balls_index,(6-i))+len_of_prev_upper_tube:len_new_tube] = 1
        puzzle[i, len_new_tube:13] = 0
    return puzzle



pdb.set_trace()
# puzzle = call_rotate(puzzle, 0)
# puzzle = rotate_up(puzzle)
puzzle = call_rotate(puzzle, 1)
puzzle = call_rotate(puzzle, 0)
pdb.set_trace()
puzzle = rotate_normal(puzzle, 1)
pdb.set_trace()
print "play the game"
