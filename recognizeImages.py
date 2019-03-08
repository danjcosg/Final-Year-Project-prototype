#given movie name & video: get images of actors
#0. Assume movie is live-action
#1. get face from web
#2. input face into face recognizer (FOV one)
#3. run face recognizer over movie

#For now: 
#	get the top 50 images from Google
#	Preprocess - 	detect face
#					Crop or whatever so that it can be input into the recognizer
#					(Optional) Select the best face


import face_recognition

cast = ["Terry Crews", "Tom Cruise"]

# Load the jpg files into numpy arrays
crews_image = face_recognition.load_image_file("input_faces/TerryCrews.jpg")
cruise_image = face_recognition.load_image_file("input_faces/TomCruise.jpg")
#These images need to eventually become frames
unknown_image1 = face_recognition.load_image_file("unknown_faces/terryCrewsUnknown.jpg")
unknown_image2 = face_recognition.load_image_file("unknown_faces/TomCruiseUnknown.jpg")

# Get the face encodings for each face in each image file
# Since there could be more than one face in each image, it returns a list of encodings.
# But since I know each image only has one face, I only care about the first encoding in each image, so I grab index 0.
try:
    crews_face_encoding = face_recognition.face_encodings(crews_image)[0]
    cruise_face_encoding = face_recognition.face_encodings(cruise_image)[0]
except IndexError:
    print("I wasn't able to locate any faces in at least one of the INPUT images. Check the image files. Aborting...")
    quit()

known_faces = [
    crews_face_encoding,
    cruise_face_encoding
]

try:
    unknown_face_encoding1 = face_recognition.face_encodings(unknown_image1)[0]
    unknown_face_encoding2 = face_recognition.face_encodings(unknown_image2)[0]
except IndexError:
    print("I wasn't able to locate any faces in at least one of the UNKNOWN images. Check the image files. Aborting...")
    quit()

# results is an array of True/False telling if the unknown face matched anyone in the known_faces array
results1 = face_recognition.compare_faces(known_faces, unknown_face_encoding1)
results2 = face_recognition.compare_faces(known_faces, unknown_face_encoding2)

print("Is the first unknown face a picture of Terry Crews?? {}".format(results1[0]))
print("Is the first unknown face a picture of Tom Cruise? {}".format(results1[1]))
print("Is the first unknown face a new person that we've never seen before? {}".format(not True in results1))

print("Is the Second unknown face a picture of Terry Crews?? {}".format(results2[0]))
print("Is the Second unknown face a picture of Tom Cruise? {}".format(results2[1]))
print("Is the Second unknown face a new person that we've never seen before? {}".format(not True in results2))