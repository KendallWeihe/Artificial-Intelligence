import pdb
import os
import subprocess


path =  os.getcwd()
filenames = os.listdir("mixed_puzzles/")

for i in range(len(filenames)):
    filenames[i] = "mixed_puzzles/" + filenames[i]

print filenames

try:
    for filename in filenames:
        new_filename = filename
        os.rename(filename, filename.replace(" (" + str(i) + ")", "-" + str(i))
except:
    pdb.set_trace()
    
pdb.set_trace()
print