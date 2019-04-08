import face_recognition
import cv2
import Experiments.processing
import os

'''
Requirements: 
    movie_path of video to run detections over
    path to images of the faces to be detected (.jpg)
        names of actors must be written as the filename, with either a space or an underscore separating first& last name
    The images in the input faces path should only have one face in them: the face of the actor the file is named after
    filenames of images must be lower case and have spaces replaced with '_'

Output:

Side-Effects:
    prints results of each frame analysis
    writes table1 and table2 data, stores final results in a pickle object

'''

def recognize_faces(movie_path, faces_path, name_mappings)
# This is a demo of running face recognition on a video file and saving the results to a new video file.
#
# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Open the input movie file
input_movie = cv2.VideoCapture(movie_path)
length = int(input_movie.get(cv2.CAP_PROP_FRAME_COUNT))
FPS = input_movie.get(cv2.CAP_PROP_FPS)
FACES_PATH = faces_path
width =  int(input_movie.get(cv2.CAP_PROP_FRAME_WIDTH)) #1280
height = int(input_movie.get(cv2.CAP_PROP_FRAME_HEIGHT)) #720
print(width)
print(height)


# Create an output movie file (make sure resolution/frame rate matches input video!)
#fourcc = cv2.VideoWriter_fourcc(*'XVID')
#output_movie = cv2.VideoWriter('output.avi', fourcc, FPS, (width, height))

# Load pictures from faces folder, make record of name-features pair and learn how to recognize them.
# known actor record => {"actor":"actor name", "character":"character name", "encoding":face_encoding}
known_actors = []
name_mappings = {"channing_tatum":"jenko", "jonah_hill":"schmidt"}  #!!!!TEMPORARILY OVERWRITING PARAMETER

for image_name in os.listdir(movie_path):
    image = face_recognition.load_image_file(FACES_PATH + image_name)
    encoding = face_recognition.face_encodings(image)[0]
    actor_name = image_name.rsplit('.')[0]
    known_actors.append((dict){"actor":actor_name, "character":name_mappings[actor_name.lower()], "encoding":face_encoding})

terry_crews_image = face_recognition.load_image_file(FACES_PATH + "terry_crews.jpg")
terry_crews_encoding = face_recognition.face_encodings(terry_crews_image)[0]

rosa_image = face_recognition.load_image_file(FACES_PATH + "stephanie_beatriz.jpg")
rosa_encoding = face_recognition.face_encodings(rosa_image)[0]


known_faces_list = [
    terry_crews_encoding,
    rosa_encoding
    ]


# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
frame_number = 0

output_csv = open("output.csv", 'w')
output_names_list = []

while True:
    # Grab a single frame of video
    ret, frame = input_movie.read()
    frame_number += 1

    # Quit when the input video file ends
    if not ret:
        break

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_frame = frame[:, :, ::-1]

    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    face_names = []
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        match = face_recognition.compare_faces(known_faces_list, face_encoding, tolerance=0.50)

        # If you had more than 2 faces, you could TODO: MAKE THIS LOGIC A LOT PRETTIER
        # but I kept it simple for the demo
        name = None
        if match[0]:
            name = "Terry Crews"
            name = known_faces[] ##########!!!!!!!!!!!!!!!!!!!!!
        elif match[1]:
            name = "Stephanie Beatriz"

        face_names.append(name)

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
    print("{}, {}".format(frame_number/FPS, face_names))
    #output_movie.write(frame)
    output_csv.write("{}, {}\n".format(frame_number/FPS, face_names)

    #append the output for this frame to list
    output_names.append(face_names)

# All done!

input_movie.release()
output_csv.close()
cv2.destroyAllWindows()

#calculate percentages & pickle results
processing.getPercentages(output_names) #default bucket size is entire clip