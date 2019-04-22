import cv2
import face_recognition
import face_recognition_models
import numpy as np
import dlib
import os

print("starting visualization test")

image_path = "/Users/Daniel/Desktop/pips1.jpg"
print("attempting to load image from path: {}. \nCurrent working dir: {}".format(image_path, os.getcwd()))
image = face_recognition.load_image_file(image_path)    #load image as numpy array in RGB format
#image = image[::-1]
for i, row in enumerate(image):
    for j, p in enumerate(row):
        image[i][j] = p[::-1]
'''
for i, row in enumerate(image):
    image[i] = row[::-1]
'''
predictor_path = face_recognition_models.pose_predictor_model_location()    # 68 points
face_rec_model_path = face_recognition_models.face_recognition_model_location()

# Load all the models we need: a detector to find the faces, a shape predictor
# to find face landmarks so we can precisely localize the face, and finally the
# face recognition model.
print("\nLoading models: ")
#detector_path = face_recognition_models.cnn_face_detector_model_location()
#detector = dlib.cnn_face_detection_model_v1(detector_path)
detector = dlib.get_frontal_face_detector()
sp = dlib.shape_predictor(predictor_path)
# facerec = dlib.face_recognition_model_v1(face_rec_model_path)


print("\nGetting locations of faces: ")
locations = detector(image)
print("Getting landmarks")
landmarks = []
for i, rectangle in enumerate(locations):
    full_object = sp.__call__(image, locations[i])
    landmarks.append(full_object.parts())

# DRAW THE LOCATIONS FOUND BY THE DETECTOR
for location in locations:
    cv2.rectangle(image, (location.bl_corner().x, location.bl_corner().y), (location.br_corner().x, location.br_corner().y - location.height()), (0,0,255), 1)

# DRAW THE LANDMARKS ON THE IMAGE AND WRITE AN IMAGE
# loop over the (x, y)-coordinates for the facial landmarks
# and draw each of them
for points in landmarks:
    for point in points:
        cv2.circle(image, (point.x, point.y), 1, (0, 0, 255), -1)


print("writing image: ")
cv2.imwrite("pips1_landmarked_frontal_detector.png", image)
print("wrote it (apparently)")
