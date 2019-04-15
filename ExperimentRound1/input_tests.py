import os
import face_recognition
import cv2

'''

What does contract expect?
What does contract guarantee?

 - return a list of records of info about an actor and the character they play. 
 For now this must be hand-coded for each film (ie: no relational database for cross referncing actor with all characters)
 - 

 
What does contract maintain?

'''

known_actors = []
name_mappings = {"channing_tatum":"jenko", "jonah_hill":"schmidt"}  #!!!!TEMPORARILY OVERWRITING PARAMETER
FACES_PATH = "../../Experiments/round1/21_jump_street/faces/"

for image_name in os.listdir(FACES_PATH):
    actor_name = image_name.rsplit('.')[0]
    if (actor_name[len(actor_name) - 1]).isdigit() :       #only use first image of each actor
        continue
    if actor_name not in name_mappings:
        name_mappings[actor_name] = actor_name + ":unknown_character"
    image = face_recognition.load_image_file(FACES_PATH + image_name)
    encoding = face_recognition.face_encodings(image)[0]
    known_actors.append(dict({"actor":actor_name, "character":name_mappings[actor_name.lower()], "encoding":encoding}))
    print("encoded " + image_name)

for record in known_actors:
    print(record)