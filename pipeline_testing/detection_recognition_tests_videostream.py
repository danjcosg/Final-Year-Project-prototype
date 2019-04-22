import cv2
import face_recognition
import face_recognition_models
import numpy as np
import dlib

from imutils.video import VideoStream
from imutils import face_utils
import imutils
import time

print("starting detection & recognition tests")

# LOAD MODELS

predictor_path = face_recognition_models.pose_predictor_model_location()
face_rec_model_path = face_recognition_models.face_recognition_model_location()

# Load all the models we need: a detector to find the faces, a shape predictor
# to find face landmarks so we can precisely localize the face, and finally the
# face recognition model.
detector = dlib.get_frontal_face_detector() #HOG+LINEAR SVM-Based
sp = dlib.shape_predictor(predictor_path)
#facerec = dlib.face_recognition_model_v1(face_rec_model_path)

# ACCESS WEBCAM

# initialize the video stream and sleep for a bit, allowing the
# camera sensor to warm up
print("[INFO] camera sensor warming up...")
vs = VideoStream(src=0).start()
time.sleep(2.0)

white_frame_path = "./white_frame.png"
white_frame = cv2.imread(white_frame_path)
#white_frame = imutils.resize(white_frame, width=800)
#cv2.startWindowThread()
#cv2.namedWindow("Frame")
white_frame_buff = white_frame.copy()
MIDPOINT = int(white_frame_buff.shape[1] / 2)

while True:
    frame = vs.read()
    frame = imutils.resize(frame, width=800)
    
    locations = detector(frame)
    landmarks = []
    
    if locations:
        white_frame_buff = white_frame.copy()
        for i in range(0,len(locations)):
            full_object = sp.__call__(frame, locations[i])
            landmarks.append(full_object.parts())   #dlib.points object

        # DRAW THE LANDMARKS ON THE IMAGE AND OUTPUT THE IMAGE TO SCREEN
        # loop over the (x, y)-coordinates for the facial landmarks
        # and draw each of them
        
        count = 0
        r = 0
        g = 0
        b = 0
        for group in landmarks:
            if count == 0:
                r = 255
                b = 0
            else:
                r = 0
                b = 255
            for point in group:
                point.x = (( point.x - MIDPOINT) * -1 ) + MIDPOINT
                '''if point.x >= WIDTH
                    point.x = WIDTH - 1'''
            for point in group:
                x = point.x
                y = point.y
                cv2.circle(white_frame_buff, (x, y), 3, (b,g,r), -1)

        print("writing image with {} points to screen: ".format(full_object.num_parts))
    else:
        print("No Face Found")

    cv2.imshow("Frame", white_frame_buff)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

cv2.destroyAllWindows()
vs.stop()
