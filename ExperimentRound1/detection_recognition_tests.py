import cv2
import face_recognition
import face_recognition_models
import numpy as np
import dlib


print("starting detection & recognition tests")
# This is a demo of running face recognition on a video file and saving the results to a new video file.
#
# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Open the input movie file

video_path = "../video_clips/21_JUMP_STREET_DVS20.avi"
name_mappings = {"channing_tatum":"Jenko"}
actor_name = "channing_tatum"
actor_kb = []

print("video path: " + video_path)
print("name_mappings: \n\t{}".format(name_mappings))
print("actor_name: {} (single value for this test)".format(actor_name))

tatum_image_path = "./frame_1.png"
tatum_image = face_recognition.load_image_file(tatum_image_path)    #load image as numpy array in RGB format

predictor_path = face_recognition_models.models.shape_predictor_68_face_landmarks
face_rec_model_path = face_recognition_models.face_recognition_model_location()

# Load all the models we need: a detector to find the faces, a shape predictor
# to find face landmarks so we can precisely localize the face, and finally the
# face recognition model.
detector = dlib.get_frontal_face_detector() #HOG-Based
sp = dlib.shape_predictor(predictor_path)
facerec = dlib.face_recognition_model_v1(face_rec_model_path)

locations = detector(tatum_image)
landmarks = sp.__call__(tatum_image, locations[0])

# Using location of face, and shape predictor, generate the 128-Vector encoding of the face (the face descriptor)

encoding = facerec.compute_face_descriptor(tatum_image, )

actor_kb.append(dict({"actor":actor_name, "character":name_mappings[actor_name.lower()], "encoding":"some encoding"}))
print("actor knowledge base: \n\t{} \n(we're skipping the encoding for the moment)".format(actor_kb))

print("Attempting to capture movie from \n\t{}".format(video_path))
input_movie = cv2.VideoCapture(video_path)
length = int(input_movie.get(cv2.CAP_PROP_FRAME_COUNT))
FPS = input_movie.get(cv2.CAP_PROP_FPS)
width =  int(input_movie.get(cv2.CAP_PROP_FRAME_WIDTH)) #720
height = int(input_movie.get(cv2.CAP_PROP_FRAME_HEIGHT)) #320
print("fps: {}".format(FPS))
print("(should be around 23.9)")
print("Width: {}".format(width))
print("(should be 720)")
print("height: {}".format(height))
print("(should be 320)\n")

print("attempting to create output video file")
# Create an output movie file (make sure resolution/frame rate matches input video!)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_movie = cv2.VideoWriter('test_output.avi', fourcc, FPS, (width, height))
print("created output video file (whether it works is another issue)\n")

# split record list into lists of the columns (keeping order) for input into recognizer functions
# maintaining order between the lists for easy referencing later on
# eg: known_encodings[1] is from the same record as known_characters[1], etc
known_encodings = []
known_characters = []
for record in actor_kb:
    known_encodings.append(record['encoding'])
    known_characters.append(record['character'])
print("splat KB into columns")
print("known_encodings: \n\t{}".format(known_encodings))
print("known_characters: \n\t{}".format(known_characters))

# Initialize some variables
face_locations = []
detected_faces_encodings = []
recognized_faces_names = []
frame_number = 0

print("\n--------\nSetup Complete. Manually verify it! \nEntering loop:\n\n")
while True:
    # Grab a single frame of video
    ret, frame = input_movie.read()
    frame_number += 1
    # Quit when the input video file ends
    if not ret:
        break
    print("readed a frame")
    print("writing frame: ")
    cv2.imwrite("frame_{}.png".format(frame_number), frame)
    print("wrote it (apparently)")
    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_frame = frame[:, :, ::-1]

    # BEGIN FACE DETECTION & ENCODING OVER THE FRAME. (find ALL faces in the frame. NB: Encoding is like analysing a face. Recognition is encoding + comparing to some kb of encodings) 
    # TODO: REWRITE WITHOUT USING facial_recognition

    print("getting face locations:")
    print('----------')
    face_locations = face_recognition.face_locations(rgb_frame)
    print("face locations: ")
    for face_loc in face_locations:
        print(face_loc)
    print('----------')

    print('getting face encodings')
    detected_faces_encodings = face_recognition.face_encodings(rgb_frame, face_locations, 2)
    print("got face encodings. \n Size: {}".format(len(detected_faces_encodings)))

    print('\nStarting to compare detected to known')
    # COMPARE FACES FOUND IN IMAGE TO KNOWN FACES, THEN SAVE NAMES OF THOSE RECOGNIZED  -- TODO: UNTESTED
    recognized_faces_names = []
    encodings_match = []
    tolerance = 0.6
    for face_encoding in detected_faces_encodings:
        # calculate Euclidian distance (similarity) between this face encoding and each known face encodings. 
        print("\n\tcalculating encodings_match. Should be list of Booleans, size equal to No. the known faces")
        print("Comparing this encoding \n\t{0}\n to this encoding \n\t {1}".format(known_encodings[0], face_encoding))
        encodings_match = [np.linalg.norm(known_encodings[i] - face_encoding, 1) <= tolerance for i in range(0, len(known_encodings))]
        print("len encodings match: " + str(len(encodings_match)))
        print("encodings_match: {}".format(encodings_match))
        
        print("Now to just match this encoding to a name")
        name = None
        for i in range(0, len(known_encodings)):
            if encodings_match[i]:
                name = known_characters[i]
                break
        recognized_faces_names.append(name)

    if not detected_faces_encodings:
        continue
    else:
        input("continue?")

input_movie.release()
cv2.destroyAllWindows()