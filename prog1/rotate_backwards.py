
#TODO
    # find the tubes that are filled
    # generate a random "index array" made up of those ^^ tubes
    # extract a random number of those tubes
    # verify they are not adjacent to each other in the direction of the turn
    # those ^^ are the tubes where balls were dropped
    # take a random number of balls where the range is no more than the size of the top tube
    # that ^^ is the number of balls that fell
    # those ^^ balls should be placed on top of the "fill line" in the previous tube
    # any balls above the fill line in the previous tube came from the previous previous tube


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
def verify_adjacent_tubes(filled_tubes_random, direction):

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
    if direction == 0:
        potential_dropped_tubes = filled_tubes_random - 1
        potential_dropped_tubes[potential_dropped_tubes < 0] = 5
    elif direction == 1:
        potential_dropped_tubes = filled_tubes_random + 1
        potential_dropped_tubes[potential_dropped_tubes > 5] = 0
    return potential_dropped_tubes

def generate_random_ball_drops(potential_dropped_tubes, puzzle):
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
            rand_num_balls = np.random.randint(1,(min(num_balls_in_tube, size_of_upper_tube - 1)+1))
        except:
            pdb.set_trace()
            print "failed rand"
        #extract the previous upper_tube
        pdb.set_trace()
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

    pdb.set_trace()
    for j in range(5,0,-1):
        temp = puzzle[j,:].copy()
        if len(temp[temp>0]) == 6-j or len(temp[temp>0]) < 6-j:
            pdb.set_trace()
            print "wrong1.0"

    output = []
    try:
        for i in range(len(filled_tubes_verified)):
            if filled_tubes_verified[i] == 0:
                output.append(upper_red_tube)
            elif filled_tubes_verified[i] == 1:
                output.append(upper_green_tube)
            elif filled_tubes_verified[i] == 2:
                output.append(upper_yellow_tube)
            elif filled_tubes_verified[i] == 3:
                output.append(upper_blue_tube)
            elif filled_tubes_verified[i] == 4:
                output.append(upper_white_tube)
            elif filled_tubes_verified[i] == 5:
                output.append(upper_black_tube)

        return np.asarray(output)
    except:
        pdb.set_trace()
        print "failed"


def rotate_backwards_downwards(puzzle, tubes_that_fell, dropped_tubes):
    # store puzzle vectors in temp vectors
    # iterate through puzzle
    # if i+1 = dropped_tubes
    #     append tubes that fell to the fill line
    # else
    #     append temp vector to the fill line
    print "rotate upwards"

    red_tube = puzzle[0,:].copy()
    green_tube = puzzle[1,:].copy()
    yellow_tube = puzzle[2,:].copy()
    blue_tube = puzzle[3,:].copy()
    white_tube = puzzle[4,:].copy()
    black_tube = puzzle[5,:].copy()

    #ROTATE DOWNWARDS!!!
    # iterate through puzzle
    # if i == 0 check if black tube fell
    # else
    #     if i-1 in tubes that fell
    #     append those balls above fill line
    try:
        for i in range(len(puzzle[:,0])):
            pdb.set_trace()
            if i == 0:
                # from red tube to black tube
                # loop back to the black tube
                if 5 in dropped_tubes:
                    # tubes fell into the red tube from the black tube
                    # append to black tube
                    index_of_black_tube = np.where(dropped_tubes == 5)[0][0]
                    size_of_upper_tube = len(tubes_that_fell[index_of_black_tube])
                    # index_of_first_empty_spot = np.where(black_tube == 1)[0][0]
                    # puzzle[5,min(index_of_first_empty_spot,1):min(index_of_first_empty_spot,1)+size_of_upper_tube] = tubes_that_fell[index_of_red_tube]
                    end_of_balls_index = len(red_tube[red_tube > 1])
                    puzzle[0,end_of_balls_index:end_of_balls_index+size_of_upper_tube] = tubes_that_fell[index_of_black_tube]
                    puzzle[0,end_of_balls_index+size_of_upper_tube:6+size_of_upper_tube] = 1
                    puzzle[0,6+size_of_upper_tube:13] = 0
                else:
                    # index_of_first_empty_spot = np.where(black_tube == 1)[0][0]
                    size_of_upper_tube = len(black_tube[black_tube > 0]) - 1
                    end_of_balls_index = len(red_tube[red_tube > 1])
                    puzzle[0,end_of_balls_index:end_of_balls_index+size_of_upper_tube] = black_tube[1:1+size_of_upper_tube]
                    puzzle[0,end_of_balls_index+size_of_upper_tube:6+size_of_upper_tube] = 1
                    puzzle[0,6+size_of_upper_tube:13] = 0
                for j in range(5,0,-1):
                    temp = puzzle[j,:].copy()
                    if len(temp[temp>0]) == 6-j or len(temp[temp>0]) < 6-j:
                        pdb.set_trace()
                        print "wrong1.0"

            if i == 1:
                # pdb.set_trace()
                if i-1 in dropped_tubes:
                    # tubes fell into the red tube from the black tube
                    # append to black tube
                    index_of_red_tube = np.where(dropped_tubes == i-1)[0][0]
                    size_of_upper_tube = len(tubes_that_fell[index_of_red_tube])
                    # index_of_first_empty_spot = np.where(black_tube == 1)[0][0]
                    # puzzle[5,min(index_of_first_empty_spot,1):min(index_of_first_empty_spot,1)+size_of_upper_tube] = tubes_that_fell[index_of_red_tube]
                    end_of_balls_index = len(green_tube[green_tube > 1])
                    puzzle[1,end_of_balls_index:end_of_balls_index+size_of_upper_tube] = tubes_that_fell[index_of_red_tube]
                    puzzle[1,end_of_balls_index+size_of_upper_tube:5+size_of_upper_tube] = 1
                    puzzle[1,5+size_of_upper_tube:13] = 0
                else:
                    # index_of_first_empty_spot = np.where(black_tube == 1)[0][0]
                    size_of_upper_tube = len(red_tube[red_tube > 0]) - 6
                    end_of_balls_index = len(green_tube[green_tube > 1])
                    puzzle[1,end_of_balls_index:end_of_balls_index+size_of_upper_tube] = red_tube[6:6+size_of_upper_tube]
                    puzzle[1,end_of_balls_index+size_of_upper_tube:5+size_of_upper_tube] = 1
                    puzzle[1,5+size_of_upper_tube:13] = 0

            if i == 2:
                # pdb.set_trace()
                if i-1 in dropped_tubes:
                    # tubes fell into the red tube from the black tube
                    # append to black tube
                    index_of_green_tube = np.where(dropped_tubes == i-1)[0][0]
                    size_of_upper_tube = len(tubes_that_fell[index_of_green_tube])
                    # index_of_first_empty_spot = np.where(black_tube == 1)[0][0]
                    # puzzle[5,min(index_of_first_empty_spot,1):min(index_of_first_empty_spot,1)+size_of_upper_tube] = tubes_that_fell[index_of_red_tube]
                    end_of_balls_index = len(yellow_tube[yellow_tube > 1])
                    puzzle[i,end_of_balls_index:end_of_balls_index+size_of_upper_tube] = tubes_that_fell[index_of_green_tube]
                    puzzle[i,end_of_balls_index+size_of_upper_tube:4+size_of_upper_tube] = 1
                    puzzle[i,4+size_of_upper_tube:13] = 0
                else:
                    # index_of_first_empty_spot = np.where(black_tube == 1)[0][0]
                    size_of_upper_tube = len(green_tube[green_tube > 0]) - 5
                    end_of_balls_index = len(yellow_tube[yellow_tube > 1])
                    puzzle[i,end_of_balls_index:end_of_balls_index+size_of_upper_tube] = green_tube[5:5+size_of_upper_tube]
                    puzzle[i,end_of_balls_index+size_of_upper_tube:4+size_of_upper_tube] = 1
                    puzzle[i,4+size_of_upper_tube:13] = 0

            if i == 3:
                # pdb.set_trace()
                if i-1 in dropped_tubes:
                    # tubes fell into the red tube from the black tube
                    # append to black tube
                    index_of_yellow_tube = np.where(dropped_tubes == i-1)[0][0]
                    size_of_upper_tube = len(tubes_that_fell[index_of_yellow_tube])
                    # index_of_first_empty_spot = np.where(black_tube == 1)[0][0]
                    # puzzle[5,min(index_of_first_empty_spot,1):min(index_of_first_empty_spot,1)+size_of_upper_tube] = tubes_that_fell[index_of_red_tube]
                    end_of_balls_index = len(blue_tube[blue_tube > 1])
                    puzzle[i,end_of_balls_index:end_of_balls_index+size_of_upper_tube] = tubes_that_fell[index_of_yellow_tube]
                    puzzle[i,end_of_balls_index+size_of_upper_tube:3+size_of_upper_tube] = 1
                    puzzle[i,3+size_of_upper_tube:13] = 0
                else:
                    # index_of_first_empty_spot = np.where(black_tube == 1)[0][0]
                    size_of_upper_tube = len(yellow_tube[yellow_tube > 0]) - 4
                    end_of_balls_index = len(blue_tube[blue_tube > 1])
                    puzzle[i,end_of_balls_index:end_of_balls_index+size_of_upper_tube] = yellow_tube[4:4+size_of_upper_tube]
                    puzzle[i,end_of_balls_index+size_of_upper_tube:3+size_of_upper_tube] = 1
                    puzzle[i,3+size_of_upper_tube:13] = 0

            if i == 4:
                # pdb.set_trace()
                if i-1 in dropped_tubes:
                    # tubes fell into the red tube from the black tube
                    # append to black tube
                    index_of_blue_tube = np.where(dropped_tubes == i-1)[0][0]
                    size_of_upper_tube = len(tubes_that_fell[index_of_blue_tube])
                    # index_of_first_empty_spot = np.where(black_tube == 1)[0][0]
                    # puzzle[5,min(index_of_first_empty_spot,1):min(index_of_first_empty_spot,1)+size_of_upper_tube] = tubes_that_fell[index_of_red_tube]
                    end_of_balls_index = len(white_tube[white_tube > 1])
                    puzzle[i,end_of_balls_index:end_of_balls_index+size_of_upper_tube] = tubes_that_fell[index_of_blue_tube]
                    puzzle[i,end_of_balls_index+size_of_upper_tube:2+size_of_upper_tube] = 1
                    puzzle[i,2+size_of_upper_tube:13] = 0
                else:
                    # index_of_first_empty_spot = np.where(black_tube == 1)[0][0]
                    size_of_upper_tube = len(blue_tube[blue_tube > 0]) - 3
                    end_of_balls_index = len(white_tube[white_tube > 1])
                    puzzle[i,end_of_balls_index:end_of_balls_index+size_of_upper_tube] = blue_tube[3:3+size_of_upper_tube]
                    puzzle[i,end_of_balls_index+size_of_upper_tube:2+size_of_upper_tube] = 1
                    puzzle[i,2+size_of_upper_tube:13] = 0

            if i == 5:
                # pdb.set_trace()
                if i-1 in dropped_tubes:
                    # tubes fell into the red tube from the black tube
                    # append to black tube
                    index_of_white_tube = np.where(dropped_tubes == i-1)[0][0]
                    size_of_upper_tube = len(tubes_that_fell[index_of_white_tube])
                    # index_of_first_empty_spot = np.where(black_tube == 1)[0][0]
                    # puzzle[5,min(index_of_first_empty_spot,1):min(index_of_first_empty_spot,1)+size_of_upper_tube] = tubes_that_fell[index_of_red_tube]
                    end_of_balls_index = len(black_tube[black_tube > 1])
                    puzzle[i,end_of_balls_index:end_of_balls_index+size_of_upper_tube] = tubes_that_fell[index_of_white_tube]
                    puzzle[i,end_of_balls_index+size_of_upper_tube:1+size_of_upper_tube] = 1
                    puzzle[i,1+size_of_upper_tube:13] = 0
                else:
                    # index_of_first_empty_spot = np.where(black_tube == 1)[0][0]
                    size_of_upper_tube = len(white_tube[white_tube > 0]) - 2
                    end_of_balls_index = len(black_tube[black_tube > 1])
                    puzzle[i,end_of_balls_index:end_of_balls_index+size_of_upper_tube] = white_tube[2:2+size_of_upper_tube]
                    puzzle[i,end_of_balls_index+size_of_upper_tube:1+size_of_upper_tube] = 1
                    puzzle[i,1+size_of_upper_tube:13] = 0
            for j in range(5,0,-1):
                temp = puzzle[j,:].copy()
                if len(temp[temp>0]) == 6-j or len(temp[temp>0]) < 6-j:
                    pdb.set_trace()
                    print "wrong1.0"


    except:
        pdb.set_trace()
        print "what line is this?"

    for j in range(5,0,-1):
        temp = puzzle[j,:].copy()
        if len(temp[temp>0]) == 6-j or len(temp[temp>0]) < 6-j:
            pdb.set_trace()
            print "wrong1.0"

    return puzzle

def rotate_backwards_upwards(puzzle, tubes_that_fell, dropped_tubes):
    # store puzzle vectors in temp vectors
    # iterate through puzzle
    # if i+1 = dropped_tubes
    #     append tubes that fell to the fill line
    # else
    #     append temp vector to the fill line

    red_tube = puzzle[0,:].copy()
    green_tube = puzzle[1,:].copy()
    yellow_tube = puzzle[2,:].copy()
    blue_tube = puzzle[3,:].copy()
    white_tube = puzzle[4,:].copy()
    black_tube = puzzle[5,:].copy()

    #ROTATE UPWARDS!!!
    # iterate through puzzle
    # if i == 0 check if black tube fell
    # else
    #     if i-1 in tubes that fell
    #     append those balls above fill line
    try:
        for i in range(len(puzzle[:,0])):
            if i == 0:
                # from red tube to black tube
                # loop back to the black tube
                if i+1 in dropped_tubes:
                    # tubes fell into the red tube from the black tube
                    # append to black tube
                    pdb.set_trace()
                    index_of_green_tube = np.where(dropped_tubes == i+1)[0][0]
                    size_of_upper_tube = len(tubes_that_fell[index_of_green_tube])
                    # index_of_first_empty_spot = np.where(black_tube == 1)[0][0]
                    # puzzle[5,min(index_of_first_empty_spot,1):min(index_of_first_empty_spot,1)+size_of_upper_tube] = tubes_that_fell[index_of_red_tube]
                    puzzle[0,6:6+size_of_upper_tube] = tubes_that_fell[index_of_green_tube]
                    puzzle[0,6+size_of_upper_tube:13] = 0
                else:
                    # index_of_first_empty_spot = np.where(black_tube == 1)[0][0]
                    pdb.set_trace()
                    size_of_upper_tube = len(green_tube[green_tube > 0]) - 5
                    puzzle[0,6:6+size_of_upper_tube] = green_tube[5:5+size_of_upper_tube]
                    puzzle[0,6+size_of_upper_tube:13] = 0

            if i == 1:
                # pdb.set_trace()
                if i+1 in dropped_tubes:
                    index_of_yellow_tube = np.where(dropped_tubes == i+1)[0][0]
                    size_of_upper_tube = len(tubes_that_fell[index_of_yellow_tube])
                    # index_of_first_empty_spot = np.where(black_tube == 1)[0][0]
                    # puzzle[5,min(index_of_first_empty_spot,1):min(index_of_first_empty_spot,1)+size_of_upper_tube] = tubes_that_fell[index_of_red_tube]
                    puzzle[1,5:5+size_of_upper_tube] = tubes_that_fell[index_of_yellow_tube]
                    puzzle[1,5+size_of_upper_tube:13] = 0
                else:
                    # index_of_first_empty_spot = np.where(black_tube == 1)[0][0]
                    size_of_upper_tube = len(yellow_tube[yellow_tube > 0]) - 4
                    puzzle[1,5:5+size_of_upper_tube] = yellow_tube[4:4+size_of_upper_tube]
                    puzzle[1,5+size_of_upper_tube:13] = 0

            if i == 2:
                if i+1 in dropped_tubes:
                    # tubes fell into the red tube from the black tube
                    # append to black tube
                    index_of_blue_tube = np.where(dropped_tubes == i+1)[0][0]
                    size_of_upper_tube = len(tubes_that_fell[index_of_blue_tube])
                    # index_of_first_empty_spot = np.where(black_tube == 1)[0][0]
                    # puzzle[5,min(index_of_first_empty_spot,1):min(index_of_first_empty_spot,1)+size_of_upper_tube] = tubes_that_fell[index_of_red_tube]
                    puzzle[i,4:4+size_of_upper_tube] = tubes_that_fell[index_of_blue_tube]
                    puzzle[i,4+size_of_upper_tube:13] = 0
                else:
                    # index_of_first_empty_spot = np.where(black_tube == 1)[0][0]
                    size_of_upper_tube = len(blue_tube[blue_tube > 0]) - 3
                    puzzle[i,4:4+size_of_upper_tube] = blue_tube[3:3+size_of_upper_tube]
                    puzzle[i,4+size_of_upper_tube:13] = 0

            if i == 3:
                # pdb.set_trace()
                if i+1 in dropped_tubes:
                    # tubes fell into the red tube from the black tube
                    # append to black tube
                    index_of_white_tube = np.where(dropped_tubes == i+1)[0][0]
                    size_of_upper_tube = len(tubes_that_fell[index_of_white_tube])
                    # index_of_first_empty_spot = np.where(black_tube == 1)[0][0]
                    # puzzle[5,min(index_of_first_empty_spot,1):min(index_of_first_empty_spot,1)+size_of_upper_tube] = tubes_that_fell[index_of_red_tube]
                    puzzle[i,3:3+size_of_upper_tube] = tubes_that_fell[index_of_white_tube]
                    puzzle[i,3+size_of_upper_tube:13] = 0
                else:
                    # index_of_first_empty_spot = np.where(black_tube == 1)[0][0]
                    size_of_upper_tube = len(white_tube[white_tube > 0]) - 2
                    puzzle[i,3:3+size_of_upper_tube] = white_tube[2:2+size_of_upper_tube]
                    puzzle[i,3+size_of_upper_tube:13] = 0

            if i == 4:
                # pdb.set_trace()
                if i+1 in dropped_tubes:
                    # tubes fell into the red tube from the black tube
                    # append to black tube
                    index_of_black_tube = np.where(dropped_tubes == i+1)[0][0]
                    size_of_upper_tube = len(tubes_that_fell[index_of_black_tube])
                    # index_of_first_empty_spot = np.where(black_tube == 1)[0][0]
                    # puzzle[5,min(index_of_first_empty_spot,1):min(index_of_first_empty_spot,1)+size_of_upper_tube] = tubes_that_fell[index_of_red_tube]
                    puzzle[i,2:2+size_of_upper_tube] = tubes_that_fell[index_of_black_tube]
                    puzzle[i,2+size_of_upper_tube:13] = 0
                else:
                    # index_of_first_empty_spot = np.where(black_tube == 1)[0][0]
                    size_of_upper_tube = len(black_tube[black_tube > 0]) - 1
                    puzzle[i,2:2+size_of_upper_tube] = black_tube[1:1+size_of_upper_tube]
                    puzzle[i,2+size_of_upper_tube:13] = 0

            if i == 5:
                # pdb.set_trace()
                if 0 in dropped_tubes:
                    # tubes fell into the red tube from the black tube
                    # append to black tube
                    index_of_red_tube = np.where(dropped_tubes == 0)[0][0]
                    size_of_upper_tube = len(tubes_that_fell[index_of_red_tube])
                    # index_of_first_empty_spot = np.where(black_tube == 1)[0][0]
                    # puzzle[5,min(index_of_first_empty_spot,1):min(index_of_first_empty_spot,1)+size_of_upper_tube] = tubes_that_fell[index_of_red_tube]
                    puzzle[i,1:1+size_of_upper_tube] = tubes_that_fell[index_of_red_tube]
                    puzzle[i,1+size_of_upper_tube:13] = 0
                else:
                    # index_of_first_empty_spot = np.where(black_tube == 1)[0][0]
                    size_of_upper_tube = len(red_tube[red_tube > 0]) - 6
                    puzzle[i,1:1+size_of_upper_tube] = red_tube[6:6+size_of_upper_tube]
                    puzzle[i,1+size_of_upper_tube:13] = 0

    except:
        pdb.set_trace()
        print "glass half full"

    for j in range(5,0,-1):
        temp = puzzle[j,:].copy()
        if len(temp[temp>0]) == j or len(temp[temp>0]) < 5-j:
            pdb.set_trace()
            print "wrong2.0"

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

k = input("Please enter the number of moves to shuffle the puzzle: ")
print "Number of moves = " + str(k)

for i in range(k):

    rand_move = np.random.randint(0,2)
    if rand_move == 0:
        puzzle = flip(puzzle)

    else:
        filled_tubes = find_filled_tubes(puzzle)
        filled_tubes_random = extract_rand_num_of_filled_tubes(filled_tubes)
        rand_direction = np.random.randint(2)
        filled_tubes_verified = verify_adjacent_tubes(filled_tubes_random, rand_direction)
        tubes_that_fell = generate_random_ball_drops(filled_tubes_verified, puzzle)
        # pdb.set_trace()
        print "iter = " + str(i)
        if rand_move == 1:
            puzzle = rotate_backwards_downwards(puzzle, tubes_that_fell, filled_tubes_verified)
        elif rand_move == 2:
            puzzle = rotate_backwards_upwards(puzzle, tubes_that_fell, filled_tubes_verified)

    for j in range(5,0,-1):
        temp = puzzle[j,:].copy()
        if len(temp[temp>0]) == 5-j:
            pdb.set_trace()
            print "wrong"

pdb.set_trace()
# filled_tubes = find_filled_tubes(puzzle)
# filled_tubes_random = extract_rand_num_of_filled_tubes(filled_tubes)
# filled_tubes_verified = verify_adjacent_tubes(filled_tubes_random, 0)
# tubes_that_fell = generate_random_ball_drops(filled_tubes_verified, puzzle)
# puzzle = rotate_backwards_downwards(puzzle, tubes_that_fell, filled_tubes_verified)
#
# pdb.set_trace()
#
# puzzle = flip(puzzle)
#
# filled_tubes = find_filled_tubes(puzzle)
# filled_tubes_random = extract_rand_num_of_filled_tubes(filled_tubes)
# filled_tubes_verified = verify_adjacent_tubes(filled_tubes_random, 0)
# tubes_that_fell = generate_random_ball_drops(filled_tubes_verified, puzzle)
# puzzle = rotate_backwards_downwards(puzzle, tubes_that_fell, filled_tubes_verified)
#
# pdb.set_trace()
#
# filled_tubes = find_filled_tubes(puzzle)
# filled_tubes_random = extract_rand_num_of_filled_tubes(filled_tubes)
# filled_tubes_verified = verify_adjacent_tubes(filled_tubes_random, 1)
# tubes_that_fell = generate_random_ball_drops(filled_tubes_verified, puzzle)
# puzzle = rotate_backwards_upwards(puzzle, tubes_that_fell, filled_tubes_verified)

pdb.set_trace()
print
