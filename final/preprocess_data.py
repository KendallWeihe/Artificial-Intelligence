import numpy as np
import os
import cv2
import pdb
import sys

if len(sys.argv) != 2:
    print "Wrong arguments"
    sys.exit(0)

directories = os.listdir("/home/kendall/Documents/UCF-101/")
directories.sort()
n_classes = 0
n_input_x = 240
n_input_y = 320
n_input_z = 3
n_videos = 0

for i in range(12):
    files = os.listdir("/home/kendall/Documents/UCF-101/" + directories[i] + "/")
    n_videos = n_videos + len(files)
    n_classes = n_classes + 1
    os.system("mkdir /home/kendall/Desktop/temp/" + directories[i])


# input_data = np.array((n_videos, n_input_x, n_input_y, n_input_z))
ground_truth = np.zeros((n_videos, n_classes))

input_data = []

video_index = 0
for i in range(12):
    filepath = "/home/kendall/Documents/UCF-101/" + directories[i] + "/"
    files = os.listdir(filepath)
    files.sort()
    for j in range(len(files)):
        os.system("avconv -i " + filepath + str(files[j]) + " -s 60x80 /home/kendall/Desktop/temp/" + str(directories[i]) + "/" + str(j) + ".avi")
        if int(sys.argv[1]) == 0:
            os.system("python save_data_late_fusion.py " + directories[i] + " " + str(j) + ".avi " + str(video_index) + " " + str(n_classes) + " " + str(i))
        elif int(sys.argv[1]) == 1:
            os.system("python save_data_slow_fusion.py " + directories[i] + " " + str(j) + ".avi " + str(video_index) + " " + str(n_classes) + " " + str(i))
        elif int(sys.argv[1]) == 2:
            os.system("python save_data_single_frame.py " + directories[i] + " " + str(j) + ".avi " + str(video_index) + " " + str(n_classes) + " " + str(i))            
        else:
            print "Missing or incorrect command line arguments"
        # ground_truth_filename = "/home/kendall/Documents/Development/CS463G/final/data/60x80/late_fusion/ground_truth/" + str(video_index) + ".csv"
        # ground_truth = np.zeros(len(directories), dtype=np.float16)
        # ground_truth[i] = 1.0
        # np.savetxt(ground_truth_filename, ground_truth, delimiter=",", fmt="%d")
        print "\n"
        print "Reading video number: " + str(video_index)
        print "Total number of videos = " + str(n_videos)
        print "\n"
        video_index = video_index + 1

input_data = np.array(input_data)
