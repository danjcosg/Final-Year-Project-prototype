import face_recognition_models
import dlib
import cv2
import os
import numpy as np
import face_recognition

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
DEFAULT_VIDEO_DIR = "/Users/daniel/Documents/FYP/data/round1_symlink/captain_america/video_clips/scene_1/" 
DEFAULT_FACES_DIR = "/Users/daniel/Documents/FYP/data/round1_symlink/captain_america/faces/manual_best/"
STRIDE = 3

default_name_mappings = {"chris_evans":"steve_rogers","hayley_atwell":"peggy_carter","sebastian_stan":"james_buchanan_barnes","tommy_lee_jones":"col_chester_phillips"}

FILM_NAME = "captain_america"
OUTPUT_DIR = "./sample_video/"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def write_sample_frames(locations, frame_copy, full_object_detections, frame_number):
    # WRITE SOME IMAGES FOR VERIFICATION
    # Draw the locations found by the detector
    for location in locations:
        cv2.rectangle(frame_copy, (location.bl_corner().x, location.bl_corner().y), (location.br_corner().x, location.br_corner().y - location.height()), (0,0,255), 1)

    # TODO: DRAW THE LANDMARKS ON THE IMAGE AND WRITE AN IMAGE FOR EVERY nth FRAME, m TIMES PER SCENE
    # loop over the (x, y)-coordinates for the facial landmarks
    # and draw each of them
    for i, full_object_detection in enumerate(full_object_detections):
        for point in full_object_detection.parts():
            cv2.circle(frame_copy, (point.x, point.y), 1, (0, 0, 255), -1)
    
    if locations:
        # Draw the name of the detected character
        for i, location in enumerate(locations):
            width = locations[i].width()
            height = locations[i].height()
            bl_corner = locations[i].bl_corner()
            cv2.rectangle(frame_copy, (bl_corner.x, bl_corner.y - height), (bl_corner.x + width, bl_corner.y - height - 23), (0,0,255), 1 )
            cv2.putText(frame_copy, recognized_faces_names[i],(locations[i].bl_corner().x,locations[i].bl_corner().y - locations[i].height()), cv2.FONT_HERSHEY_SIMPLEX, 1, (200,255,155))
    if frame_number < 10:
        cv2.imwrite(OUTPUT_DIR + "frame_00" + str(frame_number) + ".jpg", frame_copy)
    elif frame_number < 100:
        cv2.imwrite(OUTPUT_DIR + "frame_0" + str(frame_number) + ".jpg", frame_copy)
    else:
        cv2.imwrite(OUTPUT_DIR + "frame_" + str(frame_number) + ".jpg", frame_copy)

# TODO: Output SAMPLE of each scene as video
def run(video_path, actor_kb, stride = 3):

    # setup the face detector & encoder for use on each frame
    detector = dlib.get_frontal_face_detector()
    shape_predictor_path = face_recognition_models.pose_predictor_model_location()
    sp = dlib.shape_predictor(shape_predictor_path)
    facerec_model_path = face_recognition_models.face_recognition_model_location()
    recognizer = dlib.face_recognition_model_v1(facerec_model_path)

    # Add face reference encodings to our version of KB
    # TODO: untested
    detector = dlib.get_frontal_face_detector()
    sp_path = face_recognition_models.pose_predictor_model_location()
    sp = dlib.shape_predictor(sp_path)
    rec_path = face_recognition_models.face_recognition_model_location()
    rec = dlib.face_recognition_model_v1(rec_path)

    for actor_name, actor_info in actor_kb.items():

        image = cv2.imread(actor_info["image_path"])
        face_rgb = image[:,:,::-1]
    
        locations = detector(face_rgb)
        # Assume there's only one face in the reference image
        detection_object = sp(face_rgb, locations[0])
        encoding = rec.compute_face_descriptor(face_rgb, detection_object, REC_JITTER)
        actor_kb[actor_name]["encoding"] = encoding

    # split record list into lists of the columns (keeping order) for input into recognizer functions
    # maintaining order between the lists for easy referencing later on
    # eg: known_encodings[1] is from the same record as known_characters[1], etc
    known_encodings = []
    known_characters = []
    counts = []
    for actor_name, record in actor_kb.items():
        known_encodings.append(record['encoding'])
        known_characters.append(record['character'])
        counts.append(0)

    # Open the input movie file
    input_movie = cv2.VideoCapture(video_path)
    length = int(input_movie.get(cv2.CAP_PROP_FRAME_COUNT))
    FPS = input_movie.get(cv2.CAP_PROP_FPS)
    width =  int(input_movie.get(cv2.CAP_PROP_FRAME_WIDTH)) #1280
    height = int(input_movie.get(cv2.CAP_PROP_FRAME_HEIGHT)) #720

    # Initialize some variables
    face_locations = []
    detected_faces_encodings = []
    recognized_faces_names = []
    frame_number = 0
    for actor_name, actor_info in actor_kb.items():
        actor_kb[actor_name]["count"] = 0
    
    frames_analysed = 0
    print("\n\trecognizer: Finished Setup, entering loop!\n\tINPUT VIDEO: {}".format(video_path))
    while True:
        # READ FRAME IN
        # Grab a single frame of video
        ret, frame = input_movie.read()
        
        # Quit when the input video file ends
        if not ret:
            break

        frame_number += 1
        if not frame_number % stride == 0:
            continue
        
        frames_analysed += 1

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_frame = frame[:, :, ::-1]
        frame_copy = frame.copy()
        # BEGIN FACE DETECTION & ENCODING OVER THE FRAME. (find ALL faces in the frame. NB: Encoding is like analysing a face. Recognition is encoding + comparing to some kb of encodings) 
        locations = detector(rgb_frame)
        full_object_detections = []
        for location in locations:
            full_object_detections.append(sp(rgb_frame, location))  # An array of type full_object_detection[]. This object contains fields like the landmark points, but we pass the full thing to the recognizer
        detected_faces_encodings = []
        # For each detected face, compute the face descriptor
        # Jitter can improve quality of encoding, but increases the time taken in direct proportion to the number of jitters (jitter of 100 -> 100x as long)
        if REC_JITTER == 0:
            for landmarks in full_object_detections:
                detected_faces_encodings.append(recognizer.compute_face_descriptor(rgb_frame, landmarks))
        else:
            for landmarks in full_object_detections:
                detected_faces_encodings.append(recognizer.compute_face_descriptor(rgb_frame, landmarks, REC_JITTER))
        # print("Done. Got encodings for {} faces, from {} object detections".format(len(detected_faces_encodings),len(full_object_detections)))
        # print("\nStarting to compare the encodings in knowledge base to those found in the image")
        
        # COMPARE FACES FOUND IN IMAGE TO KNOWN FACES, THEN SAVE NAMES OF THOSE RECOGNIZED
        recognized_faces_names = []
        encodings_match = []
        for count, face_encoding in enumerate(detected_faces_encodings):
            
            # calculate Euclidian distance (similarity) between this face encoding and each known face encodings. 
            encodings_match = [np.linalg.norm(np.array(known_encodings[i]) - np.array(face_encoding)) <= COMPARISON_TOLERANCE for i in range(0, len(known_encodings))]
            # finally, match any recognized encoding to the associated name. 
            name = None
            for i in range(0, len(encodings_match)):
                if encodings_match[i]:
                    name = known_characters[i]
                    counts[i] += 1
                    break
            recognized_faces_names.append(name)
        print("\n***Recognized: {}".format(recognized_faces_names))
        #print("\nDone Comparing")
        #print("\tCurrent count: ")
        #for i, character_name in enumerate(known_characters):
        #    print("\t{} : {}".format(character_name , counts[i]))
        # FINISHED RECOGNIZING

        if __name__ == "__main__":
            write_sample_frames(locations, frame_copy, full_object_detections, frame_number)
            
        
        #print("{}, {}".format(frame_number/FPS, recognized_faces_names))
    #print("\n\tRecognizer: Finished processing {}".format(video_path))
    input_movie.release()
    cv2.destroyAllWindows()

    # Store counts for each actor in an updated knowledge base
    characters_to_actors = {}
    for actor_name, info in actor_kb.items():
        characters_to_actors[info["character"]] = actor_name

    for i, name in enumerate(known_characters):
        actor_kb[characters_to_actors[name]]["count"] = counts[i]
        del actor_kb[characters_to_actors[name]]["encoding"]
    print("\tRecognizer: getPercentages:run:\n\t\ttotal_frames == {}\n\t\tStride == {}\n\t\tReturning tuple: (actor_kb, frames_analysed) == ({},{})".format(frame_number,STRIDE, actor_kb, frames_analysed))
    input("Continue?")
    return (actor_kb, frames_analysed, frame_number)

#
# parameters: (path_to_video, actor_data_mapping, frame_stride)
# returns: (actor_percentage_map, n_frames_analysed, n_frames)
# side effects: print to stdout
def getPercentages(video_path, actor_kb, stride = 1):
    #processing.getPercentages(output_names) #default bucket size is entire clip
    tup = run(video_path, actor_kb, stride)
    length = tup[1]
    ret = {}
    for name, data in actor_kb.items():
        ret[name] = (float(data["count"]) / float(length)) * 100.0
    print("\trecognizer: Get Percentages: \n\t\tConverted counts from run() to percentages. \n\t\t Returning dictionary: \n\t\tret=={}".format(ret))
    #input("Continue?")
    return (ret, tup[1], tup[2])

if __name__ == '__main__':
    default_kb = {}

    # CREATE KNOWLEDGE BASE OF ACTORS & REFERENCE IMAGE PATHS & CHARACTERS RELEVANT TO QUERY
    for name in default_name_mappings:
        default_kb[name] = dict({"character":"","image_path":""})
        default_kb[name]["character"] = default_name_mappings[name]
        if os.path.exists(DEFAULT_FACES_DIR + name + ".jpg"):
            default_kb[name]["image_path"] = DEFAULT_FACES_DIR + name + ".jpg"
        else:
            for filename in os.listdir(DEFAULT_FACES_DIR):
                parts = filename.split('.')
                if parts[0] == name:
                    default_kb[name]["image_path"] = DEFAULT_FACES_DIR + name + parts[1]
                    break
            else:
                print("\tWarning: couldn't find reference image for " + name)
                del default_kb[name]

    print("\n\nTried to create KB for actors, please verify:")
    for key, data in default_kb.items():
        print("\t{}:{}".format(key,data))

    input("continue?")
    for video_path in os.listdir(DEFAULT_VIDEO_DIR):
        run(DEFAULT_VIDEO_DIR + video_path, default_kb, STRIDE)
    #print("{} : {}".format(name, percentage) for name, percentage in getPercentages(DEFAULT_VIDEO_PATH, default_kb).items()[0])
