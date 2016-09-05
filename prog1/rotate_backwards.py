
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
    rand_size = np.random.randint(1,len(filled_tubes))
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
    try:
        try:
            filled_tubes_random = filled_tubes_random + 1
            for i in range(len(filled_tubes_random)-1):
                if filled_tubes_random[i]+1 == filled_tubes_random[i+1]:
                    rand_deletion = np.random.randint(2)
                    filled_tubes_random[i+rand_deletion] = 0
        except:
            pdb.set_trace()
            print "0"

        try:
            if filled_tubes_random[0] == filled_tubes_random[len(filled_tubes_random)-1]-5:
                try:
                    rand_deletion = np.random.randint(2)
                    if rand_deletion == 0:
                        filled_tubes_random[0] = 0
                    else:
                        filled_tubes_random[len(filled_tubes_random)-1] = 0
                except:
                    pdb.set_trace()
                    print "0.5"
        except:
            pdb.set_trace()
            print "1"

        filled_tubes_random = filled_tubes_random[filled_tubes_random > 0] - 1
        return filled_tubes_random
    except:
        pdb.set_trace()
        print "verify failed"

def generate_random_ball_drops(filled_tubes_verified, puzzle):
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
    for i in range(0,len(filled_tubes_verified)):
        temp_vector = puzzle[filled_tubes_verified[i],:]
        num_balls_in_tube = len(temp_vector[temp_vector > 1])
        end_of_tube = len(temp_vector[temp_vector > 0]) - 1
        size_of_upper_tube = end_of_tube - (5 - filled_tubes_verified[i])
        # if filled_tubes_verified[i] == 5:
        #we must loop back around to the red tube
        rand_num_balls = np.random.randint(min(num_balls_in_tube, size_of_upper_tube)+1)
        #extract the previous upper_tube
        prev_upper_tube = puzzle[filled_tubes_verified[i],
                    6-filled_tubes_verified[i]-rand_num_balls:min(6-filled_tubes_verified[i]-rand_num_balls+size_of_upper_tube, end_of_tube+1)].copy()
        #remove the rand_num_balls from the current tube
        puzzle[filled_tubes_verified[i],6-filled_tubes_verified[i]-rand_num_balls:end_of_tube+1] = 1
        if filled_tubes_verified[i] == 0:
            upper_red_tube = prev_upper_tube
        elif filled_tubes_verified[i] == 1:
            upper_green_tube = prev_upper_tube
        elif filled_tubes_verified[i] == 2:
            upper_yellow_tube = prev_upper_tube
        elif filled_tubes_verified[i] == 3:
            upper_blue_tube = prev_upper_tube
        elif filled_tubes_verified[i] == 4:
            upper_white_tube = prev_upper_tube
        elif filled_tubes_verified[i] == 5:
            upper_black_tube = prev_upper_tube

        print

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


def rotate_backwards(puzzle, tubes_that_fell, filled_tubes_verified):
    # store puzzle vectors in temp vectors
    # iterate through puzzle
    # if i+1 = filled_tubes_verified
    #     append tubes that fell to the fill line
    # else
    #     append temp vector to the fill line

    red_tube = puzzle[0,:].copy()
    green_tube = puzzle[1,:].copy()
    yellow_tube = puzzle[2,:].copy()
    blue_tube = puzzle[3,:].copy()
    white_tube = puzzle[4,:].copy()
    black_tube = puzzle[5,:].copy()

    # pdb.set_trace()
    # #ROTATE UPWARDS!!!
    # for i in range(len(puzzle[:,0])):
    #     if i == 0:
    #         # from red tube to black tube
    #         # loop back to the black tube
    #         if i in filled_tubes_verified:
    #             # tubes fell into the red tube from the black tube
    #             # append to black tube
    #             index_of_red_tube = np.where(filled_tubes_verified == i)[0][0]
    #             size_of_upper_tube = len(tubes_that_fell[index_of_red_tube])
    #             # index_of_first_empty_spot = np.where(black_tube == 1)[0][0]
    #             # puzzle[5,min(index_of_first_empty_spot,1):min(index_of_first_empty_spot,1)+size_of_upper_tube] = tubes_that_fell[index_of_red_tube]
    #             puzzle[5,1:1+size_of_upper_tube] = tubes_that_fell[index_of_red_tube]
    #             puzzle[5,1+size_of_upper_tube:13] = 0
    #         else:
    #             # index_of_first_empty_spot = np.where(black_tube == 1)[0][0]
    #             puzzle[5,1:1+len(red_tube[red_tube == 1])] = red_tube[red_tube == 1]
    #             puzzle[5,1+len(red_tube[red_tube == 1]):13] = 0
    #     elif i == 1:
    #         # from green tube to red tube
    #         if i in filled_tubes_verified:
    #             index_of_green_tube = np.where(filled_tubes_verified == i)[0][0]
    #             size_of_upper_tube = len(tubes_that_fell[index_of_green_tube])
    #             # index_of_first_empty_spot = np.where(red_tube == 1)[0][0]
    #             puzzle[0,6:6+size_of_upper_tube] = tubes_that_fell[index_of_green_tube]
    #             puzzle[0,6+size_of_upper_tube:13] = 0
    #         else:
    #             # index_of_first_empty_spot = np.where(red_tube == 1)[0][0]
    #             puzzle[0,6:6+len(green_tube[green_tube == 1])] = green_tube[green_tube == 1]
    #             puzzle[0,6+len(green_tube[green_tube == 1]):13] = 0
    #     elif i == 2:
    #         #from yellow to to green tube
    #         if i in filled_tubes_verified:
    #             index_of_yellow_tube = np.where(filled_tubes_verified == i)[0][0]
    #             size_of_upper_tube = len(tubes_that_fell[index_of_yellow_tube])
    #             # index_of_first_empty_spot = np.where(green_tube == 1)[0][0]
    #             puzzle[1,5:5+size_of_upper_tube] = tubes_that_fell[index_of_yellow_tube]
    #             puzzle[1,5+size_of_upper_tube:13] = 0
    #         else:
    #             # index_of_first_empty_spot = np.where(green_tube == 1)[0][0]
    #             puzzle[1,5:5+len(yellow_tube[yellow_tube == 1])] = yellow_tube[yellow_tube == 1]
    #             puzzle[1,5+len(yellow_tube[yellow_tube == 1]):13] = 0
    #     elif i == 3:
    #         # from blue tube to yellow tube
    #         # index_of_first_empty_spot = np.where(yellow_tube == 1)[0][0]
    #         if i in filled_tubes_verified:
    #             index_of_blue_tube = np.where(filled_tubes_verified == i)[0][0]
    #             size_of_upper_tube = len(tubes_that_fell[index_of_blue_tube])
    #             puzzle[2,4:4+size_of_upper_tube] = tubes_that_fell[index_of_blue_tube]
    #             puzzle[2,4+size_of_upper_tube:13] = 0
    #         else:
    #             puzzle[2,4:4+len(blue_tube[blue_tube == 1])] = blue_tube[blue_tube == 1]
    #             puzzle[2,4+len(blue_tube[blue_tube == 1]):13] = 0
    #     elif i == 4:
    #         # from white tube to blue tube
    #         # index_of_first_empty_spot = np.where(blue_tube == 1)[0][0]
    #         if i in filled_tubes_verified:
    #             index_of_white_tube = np.where(filled_tubes_verified == i)[0][0]
    #             size_of_upper_tube = len(tubes_that_fell[index_of_white_tube])
    #             puzzle[3,3:3+size_of_upper_tube] = tubes_that_fell[index_of_white_tube]
    #             puzzle[3,3+size_of_upper_tube:13] = 0
    #         else:
    #             puzzle[3,3:3+len(white_tube[white_tube == 1])] = white_tube[white_tube == 1]
    #             puzzle[3,3+len(white_tube[white_tube == 1]):13] = 0
    #
    #     elif i == 5:
    #         # from black tube to white tube
    #         # index_of_first_empty_spot = np.where(white_tube == 1)[0][0]
    #         if i in filled_tubes_verified:
    #             index_of_black_tube = np.where(filled_tubes_verified == i)[0][0]
    #             size_of_upper_tube = len(tubes_that_fell[index_of_black_tube])
    #             puzzle[4,2:2+size_of_upper_tube] = tubes_that_fell[index_of_black_tube]
    #             puzzle[4,2+size_of_upper_tube:13] = 0
    #         else:
    #             puzzle[4,2:2+len(black_tube[black_tube == 1])] = black_tube[black_tube == 1]
    #             puzzle[4,2+len(black_tube[black_tube == 1]):13] = 0

    pdb.set_trace()
    #ROTATE DOWNWARDS!!!
    for i in range(len(puzzle[:,0])):
        if i == 0:
            # from red tube to black tube
            # loop back to the black tube
            if i in filled_tubes_verified:
                # tubes fell into the red tube from the black tube
                # append to black tube
                index_of_black_tube = np.where(filled_tubes_verified == i)[0][0]
                size_of_upper_tube = len(tubes_that_fell[index_of_black_tube])
                # index_of_first_empty_spot = np.where(black_tube == 1)[0][0]
                # puzzle[5,min(index_of_first_empty_spot,1):min(index_of_first_empty_spot,1)+size_of_upper_tube] = tubes_that_fell[index_of_red_tube]
                puzzle[0,6:6+size_of_upper_tube] = tubes_that_fell[index_of_black_tube]
                puzzle[0,6+size_of_upper_tube:13] = 0
            else:
                # index_of_first_empty_spot = np.where(black_tube == 1)[0][0]
                puzzle[0,6:6+len(black_tube[black_tube == 1])] = black_tube[black_tube == 1]
                puzzle[0,6+len(black_tube[black_tube == 1]):13] = 0
        elif i == 1:
            # from green tube to red tube
            pdb.set_trace()
            if i in filled_tubes_verified:
                index_of_red_tube = np.where(filled_tubes_verified == i)[0][0]
                size_of_upper_tube = len(tubes_that_fell[index_of_red_tube])
                # index_of_first_empty_spot = np.where(red_tube == 1)[0][0]
                puzzle[1,5:5+size_of_upper_tube] = tubes_that_fell[index_of_red_tube]
                puzzle[1,5+size_of_upper_tube:13] = 0
            else:
                # index_of_first_empty_spot = np.where(red_tube == 1)[0][0]
                puzzle[1,5:5+len(red_tube[red_tube == 1])] = red_tube[red_tube == 1]
                puzzle[1,5+len(red_tube[red_tube == 1]):13] = 0
        elif i == 2:
            #from yellow to to green tube
            if i in filled_tubes_verified:
                index_of_green_tube = np.where(filled_tubes_verified == i)[0][0]
                size_of_upper_tube = len(tubes_that_fell[index_of_green_tube])
                # index_of_first_empty_spot = np.where(green_tube == 1)[0][0]
                puzzle[2,4:4+size_of_upper_tube] = tubes_that_fell[index_of_green_tube]
                puzzle[2,4+size_of_upper_tube:13] = 0
            else:
                # index_of_first_empty_spot = np.where(green_tube == 1)[0][0]
                puzzle[2,4:4+len(green_tube[green_tube == 1])] = green_tube[green_tube == 1]
                puzzle[2,4+len(green_tube[green_tube == 1]):13] = 0
        elif i == 3:
            # from blue tube to yellow tube
            # index_of_first_empty_spot = np.where(yellow_tube == 1)[0][0]
            if i in filled_tubes_verified:
                index_of_yellow_tube = np.where(filled_tubes_verified == i)[0][0]
                size_of_upper_tube = len(tubes_that_fell[index_of_yellow_tube])
                puzzle[3,3:3+size_of_upper_tube] = tubes_that_fell[index_of_yellow_tube]
                puzzle[3,3+size_of_upper_tube:13] = 0
            else:
                puzzle[3,3:3+len(yellow_tube[yellow_tube == 1])] = yellow_tube[yellow_tube == 1]
                puzzle[3,3+len(yellow_tube[yellow_tube == 1]):13] = 0
        elif i == 4:
            # from white tube to blue tube
            # index_of_first_empty_spot = np.where(blue_tube == 1)[0][0]
            if i in filled_tubes_verified:
                index_of_blue_tube = np.where(filled_tubes_verified == i)[0][0]
                size_of_upper_tube = len(tubes_that_fell[index_of_blue_tube])
                puzzle[4,2:2+size_of_upper_tube] = tubes_that_fell[index_of_blue_tube]
                puzzle[4,2+size_of_upper_tube:13] = 0
            else:
                puzzle[4,2:2+len(blue_tube[blue_tube == 1])] = blue_tube[blue_tube == 1]
                puzzle[4,2+len(blue_tube[blue_tube == 1]):13] = 0

        elif i == 5:
            # from black tube to white tube
            # index_of_first_empty_spot = np.where(white_tube == 1)[0][0]
            if i in filled_tubes_verified:
                index_of_white_tube = np.where(filled_tubes_verified == i)[0][0]
                size_of_upper_tube = len(tubes_that_fell[index_of_white_tube])
                puzzle[5,1:1+size_of_upper_tube] = tubes_that_fell[index_of_white_tube]
                puzzle[5,1+size_of_upper_tube:13] = 0
            else:
                puzzle[5,1:1+len(white_tube[white_tube == 1])] = white_tube[white_tube == 1]
                puzzle[5,1+len(white_tube[white_tube == 1]):13] = 0



    pdb.set_trace()
    print


pdb.set_trace()
filled_tubes = find_filled_tubes(puzzle)
filled_tubes_random = extract_rand_num_of_filled_tubes(filled_tubes)
filled_tubes_verified = verify_adjacent_tubes(filled_tubes_random)
tubes_that_fell = generate_random_ball_drops(filled_tubes_verified, puzzle)
rotated_puzzle = rotate_backwards(puzzle, tubes_that_fell, filled_tubes_verified)
pdb.set_trace()
print
