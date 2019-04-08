#analyse and process each clip
#pipeline: https://www.draw.io/?state=%7B%22ids%22:%5B%221jtC9XGqnJuqxOkcRz7jqPCOd6H2ZsXp3%22%5D,%22action%22:%22open%22,%22userId%22:%22115019067398552559764%22%7D#G1jtC9XGqnJuqxOkcRz7jqPCOd6H2ZsXp3
import feature_extractor
import video_face_recognition

#TODO: Practice programming by contract during this project. Teach to Ben on Thursday

clips_filepath = "./video_clips/"
faces_dir = "./face_images/"

#dict mapping character name to the actor's name and facial features data. Start by adding character names from images folder
for filename in faces_dir:

    features = #get features from open(filename)

    name = (re.search("(*).+", filename)).group()
    character_info[name] = {"features":, 
                            "actor_name":"whatever", 
                            "filmname":""
                            }

for face_image in images:


for clip in clips_filepath:
    video_face_recognition