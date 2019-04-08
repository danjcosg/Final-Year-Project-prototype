import os
import 

known_actors = []
name_mappings = {"channing_tatum":"jenko", "jonah_hill":"schmidt"}  #!!!!TEMPORARILY OVERWRITING PARAMETER


for image_name in os.listdir(movie_path):
    actor_name = image_name.rsplit('.')[0]
    if( actor_name[len(actor_name) - 1]).isdigit() ):
        continue
    #image = face_recognition.load_image_file(FACES_PATH + image_name)
    #encoding = face_recognition.face_encodings(image)[0]
    
    known_actors.append((dict){"actor":actor_name, "character":name_mappings[actor_name.lower()], "encoding":"ENcODiNg hERe"})
