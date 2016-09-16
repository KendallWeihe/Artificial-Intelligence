import pdb
import os
import subprocess


path =  os.getcwd()
filenames = os.listdir("mixed_puzzles/")

for i in range(len(filenames)):
    filenames[i] = "mixed_puzzles/" + filenames[i]

# print filenames

# try:
i = 1
for filename in filenames:
    new_filename = filename
    # pdb.set_trace()
    try:
        file_number = filename[filename.find("(")+1:filename.find(")")]
        temp = int(file_number) + 900
        os.rename(filename, filename.replace(" (" + file_number + ")", "-" + str(temp)))
        i = i + 1
    except:
        print "there was an error"
# except:
#     pdb.set_trace()

#TODO:
    # verify puzzle state is the same after changing values to 1,2,3,4,5,6
    # change mixed puzzles to only 5 states
    # collect data
    # rename
    # make sure the data collection program is only called number of files times
