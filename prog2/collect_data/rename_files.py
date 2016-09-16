import pdb
import os
import subprocess


path =  os.getcwd()
filenames = os.listdir("temp_mixed_puzzles/")

for i in range(len(filenames)):
    filenames[i] = "temp_mixed_puzzles/" + filenames[i]

print filenames

try:
    for filename in filenames:
        os.rename(filename, filename.replace(" ", "-"))
except:
    pdb.set_trace()
    
pdb.set_trace()
print