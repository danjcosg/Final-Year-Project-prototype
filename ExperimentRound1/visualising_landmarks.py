import cv2
import face_recognition
import face_recognition_models
import numpy as np
import dlib
import os

print("starting visualization test")
# This is a demo of running face recognition on a video file and saving the results to a new video file.
#
# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Open the input movie file

video_path = "../video_clips/21_JUMP_STREET_DVS20.avi"
tatum_image_path = "./frame_1.png"
print("attempting to load image from rel path: {}. \nCurrent working dir: {}".format(tatum_image_path, os.getcwd()))
tatum_image = face_recognition.load_image_file(tatum_image_path)    #load image as numpy array in RGB format

predictor_path = face_recognition_models.pose_predictor_model_location()
face_rec_model_path = face_recognition_models.face_recognition_model_location()

# Load all the models we need: a detector to find the faces, a shape predictor
# to find face landmarks so we can precisely localize the face, and finally the
# face recognition model.
print("\nLoading models: ")
detector = dlib.get_frontal_face_detector()
sp = dlib.shape_predictor(predictor_path)
facerec = dlib.face_recognition_model_v1(face_rec_model_path)

print("Getting locations: ")
locations = detector(tatum_image)
print("Getting landmarks")
full_object = sp.__call__(tatum_image, locations[0])
print("Here are the landmarks:")
landmarks = full_object.parts()   #dlib.points object
print("Number of points: {}".format(full_object.num_parts))
for point in landmarks:
    print("{},{}".format(point.x, point.y),)

# DRAW THE LANDMARKS ON THE IMAGE AND WRITE AN IMAGE
# loop over the (x, y)-coordinates for the facial landmarks
# and draw each of them
for point in landmarks:
    x = point.x
    y = point.y
    cv2.circle(tatum_image, (x, y), 1, (0, 0, 255), -1)

print("writing image: ")
cv2.imwrite("frame_1_landmarked.png", tatum_image)
print("wrote it (apparently)")
