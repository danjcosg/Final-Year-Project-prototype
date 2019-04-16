import face_recognition
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
    writes table1 and table2 data, stores final results in a pickle object

'''

def run(video_path, actor_kb):
    # This is a demo of running face recognition on a video file and saving the results to a new video file.
    #
    # PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
    # OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
    # specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

    # Open the input movie file
    input_movie = cv2.VideoCapture(video_path)
    length = int(input_movie.get(cv2.CAP_PROP_FRAME_COUNT))
    FPS = input_movie.get(cv2.CAP_PROP_FPS)
    width =  int(input_movie.get(cv2.CAP_PROP_FRAME_WIDTH)) #1280
    height = int(input_movie.get(cv2.CAP_PROP_FRAME_HEIGHT)) #720
    print(width)
    print(height)

    
    # Create an output movie file (make sure resolution/frame rate matches input video!)
    #fourcc = cv2.VideoWriter_fourcc(*'XVID')
    #output_movie = cv2.VideoWriter('output.avi', fourcc, FPS, (width, height))

    # split record list into lists of the columns (keeping order) for input into recognizer functions
    # maintaining order between the lists for easy referencing later on
    # eg: known_encodings[1] is from the same record as known_characters[1], etc
    known_encodings = []
    known_characters = []
    for record in actor_kb:
        known_encodings.append(record['encoding'])
        known_characters.append(record['character'])

    # Initialize some variables
    face_locations = []
    detected_faces_encodings = []
    recognized_faces_names = []
    frame_number = 0

    output_csv = open("output.csv", 'w')
    output_names = []

    while True:

        # READ FRAME IN (OpenCV)

        # Grab a single frame of video
        ret, frame = input_movie.read()
        frame_number += 1

        # Quit when the input video file ends
        if not ret:
            break

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_frame = frame[:, :, ::-1]

        # BEGIN FACE DETECTION & ENCODING OVER THE FRAME. (find ALL faces in the frame. NB: Encoding is like analysing a face. Recognition is encoding + comparing to some kb of encodings) 
        # TODO: REWRITE WITHOUT USING facial_recognition
        """
        Returns an array of bounding boxes of human faces in a image
        :param img: An image (as a numpy array)
        :param number_of_times_to_upsample: How many times to upsample the image looking for faces. Higher numbers find smaller faces.
        :param model: Which face detection model to use. "hog" is less accurate but faster on CPUs. "cnn" is a more accurate
                    deep-learning model which is GPU/CUDA accelerated (if available). The default is "hog".
        :return: A list of tuples of found face locations in css (top, right, bottom, left) order
        """
        face_locations = face_recognition.face_locations(rgb_frame)
        detected_faces_encodings = face_recognition.face_encodings(rgb_frame, face_locations, 2)

        # COMPARE FACES FOUND IN IMAGE TO KNOWN FACES, THEN SAVE NAMES OF THOSE RECOGNIZED  -- TODO: UNTESTED
        recognized_faces_names = []
        encodings_match = []
        tolerance = 0.6
        for face_encoding in detected_faces_encodings:
            # calculate Euclidian distance (similarity) between this face encoding and each known face encodings. 
            print("calculating encodings_match. Should be list of Booleans, size equal to No. the known faces")
            encodings_match = [np.linalg.norm(known_encodings[i] - face_encoding, 1) <= tolerance for i in range(0, len(known_encodings))]
            print("len encodings match: " + str(len(encodings_match)))
            name = None
            for i in range(0, len(known_encodings)):
                if encodings_match[i]:
                    name = known_characters[i]
                    break
            recognized_faces_names.append(name)

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
        '''
        print("{}, {}".format(frame_number/FPS, recognized_faces_names))
        output_csv.write("{}, {}\n".format(frame_number/FPS, recognized_faces_names))

        #append the output for this frame to list
        output_names.append(recognized_faces_names)


    input_movie.release()
    output_csv.close()
    cv2.destroyAllWindows()

    #calculate percentages & pickle results
    #processing.getPercentages(output_names) #default bucket size is entire clip