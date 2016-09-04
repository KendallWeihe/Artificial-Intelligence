#psuedocode

    #the first move from a solved state to an unsolved state...
    #WHICH TUBES DROPPED BALLS?
        #generate random number of tubes that dropped
        #iterate through array from above generator
            #if index's exist that are adjacent -- including the first and last
                #generate random 0/1
                #delete the above index ^
                #recheck that no tubes are adjacent
            #by this point we would have an array that looked like the following examples
                #[0,2,4]
                #[1,3,5]
                #[0,5]
                #[2] ..
                #these are the indexes that had a drop
    #HOW MANY BALLS DROPPED?
        #generate random number in range --> min(tube_1,tube_2)
        #this is the number of balls that dropped

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
            filled_tubes_random[5] = 0
    pdb.set_trace()

    filled_tubes_random = filled_tubes_random[filled_tubes_random > 0] - 1
    return filled_tubes_random

pdb.set_trace()
filled_tubes = find_filled_tubes(puzzle)
filled_tubes_random = extract_rand_num_of_filled_tubes(filled_tubes)
filled_tubes_verified = verify_adjacent_tubes(filled_tubes_random)
