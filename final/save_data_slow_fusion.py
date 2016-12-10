import numpy as np
import cv2
import sys
import pdb

# ARGV INPUTS:
#     directory name
#     file name
#     video number
    # number of classes
    # directory index

cap = cv2.VideoCapture("/home/kendall/Desktop/temp/" + sys.argv[1] + "/" + sys.argv[2])
# pdb.set_trace()
video = []
ret = True
while(ret):
    # Capture frame-by-frame
    ret, frame = cap.read()
    if frame != []:
        video.append(frame)

del video[len(video)-1]
video = np.array(video)
late_fusion = []
for i in range(int(video.shape[0]/2)-5, int(video.shape[0]/2)+5):
    late_fusion.append(video[i,:,:,:])

input_filename = "/home/kendall/Documents/Development/CS463G/final/data/60x80/slow_fusion/input_data/" + sys.argv[3] + ".csv"
late_fusion = np.array(late_fusion, dtype=np.float16).reshape(10*80*3, 60)
np.savetxt(input_filename, late_fusion, delimiter=",", fmt="%d")

ground_truth_filename = "/home/kendall/Documents/Development/CS463G/final/data/60x80/slow_fusion/ground_truth/" + sys.argv[3] + ".csv"
ground_truth = np.zeros((int(sys.argv[4])), dtype=np.float16)
ground_truth[int(sys.argv[5])] = 1.0
np.savetxt(ground_truth_filename, ground_truth, delimiter=",", fmt="%d")
