import os


known_actors = []
name_mappings = {"channing_tatum":"jenko", "jonah_hill":"schmidt"}  #!!!!TEMPORARILY OVERWRITING PARAMETER
FACES_PATH = "../../Experiments/round1/21_jump_street/faces/"

for image_name in os.listdir(FACES_PATH):
    actor_name = image_name.rsplit('.')[0]
    if (actor_name[len(actor_name) - 1]).isdigit() :       #only use first image of each actor
        continue
    if actor_name not in name_mappings:
        name_mappings[actor_name] = actor_name + ":unknown_character"
    print("image name: " + image_name)
    #image = face_recognition.load_image_file(FACES_PATH + image_name)
    #encoding = face_recognition.face_encodings(image)[0]
    
    known_actors.append(dict({"actor":actor_name, "character":name_mappings[actor_name.lower()], "encoding":"ENcODiNg hERe"}))

for record in known_actors:
    print(record)