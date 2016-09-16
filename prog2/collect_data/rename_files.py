import pdb
import os
import subprocess


path =  os.getcwd()
filenames = os.listdir("mixed_puzzles/")

for i in range(len(filenames)):
    filenames[i] = "mixed_puzzles/" + filenames[i]

print filenames

try:
    i = 101
    for filename in filenames:
        new_filename = filename
        os.rename(filename, filename.replace(" (" + str(i) + ")", "-" + str(i)))
        i = i + 1
except:
    pdb.set_trace()
    
#TODO:
    verify puzzle state is the same after changing values to 1,2,3,4,5,6
    # change mixed puzzles to only 5 states
    # collect data
    # rename
    # make sure the data collection program is only called number of files times
    