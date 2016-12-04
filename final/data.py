import numpy as np
import os
import cv2
import pdb

#TODO:
    # read in videos
    #     read in classification directories
    #     iterate through directories
    #         read in videos

directories = os.listdir("/home/kendall/Documents/UCF-101/")
n_classes = 0
n_input_x = 240
n_input_y = 320
n_input_z = 3
n_videos = 0

for i in range(len(directories)):
    files = os.listdir("/home/kendall/Documents/UCF-101/" + directories[i] + "/")
    n_videos = n_videos + len(files)
    n_classes = n_classes + 1

# input_data = np.array((n_videos, n_input_x, n_input_y, n_input_z))
ground_truth = np.zeros((n_videos, n_classes))

input_data = []

video_index = 0
for i in range(len(directories)):
    files = os.listdir("/home/kendall/Documents/UCF-101/" + directories[i] + "/")
    for j in range(len(files)):
        cap = cv2.VideoCapture("/home/kendall/Documents/UCF-101/" + directories[i] + "/" + files[i])
        # pdb.set_trace()
        video = []
        ret = True
        while(ret):
            # Capture frame-by-frame
            ret, frame = cap.read()
            video.append(frame)

        input_data.append(video)
        ground_truth[video_index,i] = 1
        video_index = video_index + 1

        print "Reading video number: " + str(video_index)


input_data = np.array(input_data)
