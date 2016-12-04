import pdb

filename = "./v_PizzaTossing_g01_c01.avi"

import numpy as np
import cv2

cap = cv2.VideoCapture(filename)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    pdb.set_trace()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

