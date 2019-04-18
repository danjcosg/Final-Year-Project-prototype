import face_recognition_models
import dlib
import cv2
import Experiments.processing
import os
import numpy as np

'''
Requirements: 
    str video_path - video path of video to run detections over

    [dict] - face "knowledge" of characters to be detected:
        # actor knowledge base structure => [ {"actor":<actor name>, "character":<character name>, "encoding":<dlib face_encoding>} ]
Output:


Side-Effects:
    prints results of each frame analysis
    TODO: Writes table1 and table2 data, stores final results in a pickle object
'''

REC_JITTER = 0
COMPARISON_TOLERANCE = 0.6
DEFAULT_VIDEO_PATH = "/Users/daniel/Documents/FYP/Prototype/video_clips/21_JUMP_STREET_DVS20.avi" 
TEST_IMAGE_PATH = "/Users/daniel/Documents/FYP/Experiments/round1_symlink/21_jump_street/faces/channing_tatum.jpg"
if not os.path.exists("/Users/daniel/Documents/FYP/Experiments/round1_symlink/21_jump_street/faces"):
    TEST_IMAGE_PATH = "/Users/daniel/Documents/FYP/Prototype/input_faces/channing_tatum.jpg"

default_kb = {}

def run(video_path, actor_kb):

    # Open the input movie file
    input_movie = cv2.VideoCapture(video_path)
    length = int(input_movie.get(cv2.CAP_PROP_FRAME_COUNT))
    FPS = input_movie.get(cv2.CAP_PROP_FPS)
    width =  int(input_movie.get(cv2.CAP_PROP_FRAME_WIDTH)) #1280
    height = int(input_movie.get(cv2.CAP_PROP_FRAME_HEIGHT)) #720

    # split record list into lists of the columns (keeping order) for input into recognizer functions
    # maintaining order between the lists for easy referencing later on
    # eg: known_encodings[1] is from the same record as known_characters[1], etc
    known_encodings = []
    known_characters = []
    for actor_name, record in actor_kb.items():
        known_encodings.append(record['encoding'])
        known_characters.append(record['character'])

    # setup the face detector & encoder for use on each frame
    detector = dlib.get_frontal_face_detector()
    shape_predictor_path = face_recognition_models.pose_predictor_model_location()
    sp = dlib.shape_predictor(shape_predictor_path)
    facerec_model_path = face_recognition_models.face_recognition_model_location()
    recognizer = dlib.face_recognition_model_v1(facerec_model_path)

    # Initialize some variables
    face_locations = []
    detected_faces_encodings = []
    recognized_faces_names = []
    frame_number = 0
    '''
        output_csv = open("output.csv", 'w')
        output_names = []
    '''
    print("-\n-\n-\n***\nFinished Setup, entering loop!\n")
    while True:

        # READ FRAME IN
        # Grab a single frame of video
        ret, frame = input_movie.read()
        frame_number += 1
        frame_copy = frame.copy()

        # Quit when the input video file ends
        if not ret:
            break

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_frame = frame[:, :, ::-1]

        # BEGIN FACE DETECTION & ENCODING OVER THE FRAME. (find ALL faces in the frame. NB: Encoding is like analysing a face. Recognition is encoding + comparing to some kb of encodings) 
        # -- TODO: UNTESTED. Compare to face_recognition.py
        print("Getting locations:")
        locations = detector(rgb_frame)
        print("Done. Found {} faces".format(len(locations)))
        print("\nRunning shape predictor over each face:")
        full_object_detections = []
        for location in locations:
            full_object_detections.append(sp(rgb_frame, location))  # An array of type full_object_detection[]. This object contains fields like the landmark points, but we pass the full thing to the recognizer
        print("Done. Got shapes for {} faces".format(len(full_object_detections)))
        print("\nTrying to create descriptors for each face")
        detected_faces_encodings = []
        # For each detected face, compute the face descriptor
        # Jitter can improve quality of encoding, but increases the time taken in direct proportion to the number of jitters (jitter of 100 -> 100x as long)
        if REC_JITTER == 0:
            for landmarks in full_object_detections:
                detected_faces_encodings.append(recognizer.compute_face_descriptor(rgb_frame, landmarks))
        else:
            for landmarks in full_object_detections:
                detected_faces_encodings.append(recognizer.compute_face_descriptor(rgb_frame, landmarks, REC_JITTER))
        print("Done. Got encodings for {} faces, from {} object detections".format(len(detected_faces_encodings),len(full_object_detections)))
        print("Drawing on & Writing image")

        # DRAW THE LOCATIONS FOUND BY THE DETECTOR
        for location in locations:
            cv2.rectangle(frame_copy, (location.bl_corner().x, location.bl_corner().y), (location.br_corner().x, location.br_corner().y - location.height()), (0,0,255), 1)

        # DRAW THE LANDMARKS ON THE IMAGE AND WRITE AN IMAGE
        # loop over the (x, y)-coordinates for the facial landmarks
        # and draw each of them
        print("Enumerating Full_object_detections: ")
        for i, full_object_detection in enumerate(full_object_detections):
            print("\tDrawing landmarks for face {}\n\tnum_parts: {}".format(i,full_object_detection.num_parts))
            for point in full_object_detection.parts():
                cv2.circle(frame_copy, (point.x, point.y), 1, (0, 0, 255), -1)

        cv2.imwrite("frame_test1.jpg", frame_copy)
        input("Continue?")

        print("\nStarting to compare the encodings in knowledge base to those found in the image")
        # COMPARE FACES FOUND IN IMAGE TO KNOWN FACES, THEN SAVE NAMES OF THOSE RECOGNIZED  -- TODO: UNTESTED
        recognized_faces_names = []
        encodings_match = []
        print("\tskipping euclidean distance for initial test, \n\tjust print the encodings instead")
        for count, face_encoding in enumerate(detected_faces_encodings):
            print("\t\tdetected_faces_encodings[{}] == {}".format(count,face_encoding))
            '''
            # calculate Euclidian distance (similarity) between this face encoding and each known face encodings. 
            print("\tcalculating encodings_match. Should be list of Booleans, size equal to No. the known faces")
            encodings_match = [np.linalg.norm(known_encodings[i] - face_encoding, 1) <= COMPARISON_TOLERANCE for i in range(0, len(known_encodings))]
            print("\tlen encodings match: " + str(len(encodings_match)))
            '''
            name = None
            
            for i in range(0, len(encodings_match)):
                if encodings_match[i]:
                    name = known_characters[i]
                    break
            recognized_faces_names.append(name)
        print("\nDone Comparing")
        print("Recognized_faces_names: {}".format(recognized_faces_names))
        print("Finished Iteration\n\n")
        # FINISHED RECOGNIZING

        # OUTPUT RESULTS
        '''
        # Label the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            if not name:
                continue

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 25), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

        # Write the resulting image to the output video file
        print("Writing frame {} / {}".format(frame_number, length))
        #output_movie.write(frame)
        
        print("{}, {}".format(frame_number/FPS, recognized_faces_names))
        output_csv.write("{}, {}\n".format(frame_number/FPS, recognized_faces_names))

        #append the output for this frame to list
        output_names.append(recognized_faces_names)
        '''

    input_movie.release()
    #output_csv.close()
    cv2.destroyAllWindows()

    #calculate percentages & pickle results
    #processing.getPercentages(output_names) #default bucket size is entire clip

if __name__ == '__main__':
    # Setup encodings for the KB
    # eg:
    detector = dlib.get_frontal_face_detector()
    sp_path = face_recognition_models.pose_predictor_model_location()
    sp = dlib.shape_predictor(sp_path)
    rec_path = face_recognition_models.face_recognition_model_location()
    rec = dlib.face_recognition_model_v1(rec_path)

    input_face = cv2.imread(TEST_IMAGE_PATH)
    input_face = input_face[:,:,::-1]

    # Assume there's just one face
    locations = detector(input_face)
    detection_object = sp(input_face, locations[0])
    encoding = rec.compute_face_descriptor(input_face, detection_object, REC_JITTER)
    default_kb["channing_tatum"] = dict({"character":"Jenko","encoding":encoding})

    run(DEFAULT_VIDEO_PATH, default_kb)