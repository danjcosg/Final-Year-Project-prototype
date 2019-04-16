#analyse and process each clip
#pipeline: https://www.draw.io/?state=%7B%22ids%22:%5B%221jtC9XGqnJuqxOkcRz7jqPCOd6H2ZsXp3%22%5D,%22action%22:%22open%22,%22userId%22:%22115019067398552559764%22%7D#G1jtC9XGqnJuqxOkcRz7jqPCOd6H2ZsXp3

import video_face_recognition
import os
import face_recognition
import cv2

EXPERIMENT_PATH = "~/Documents/FYP/Experiments/round1/21_jump_street/"
CLIPS_PATH = EXPERIMENT_PATH + "video_clips/"
FACES_PATH = "../../Experiments/round1/21_jump_street/faces/"

actor_kb = []
name_mappings = {"channing_tatum":"jenko", "jonah_hill":"schmidt"}  #!!!!TEMPORARILY OVERWRITING PARAMETER, THIS SHOULD BE LOADED FROM ELSEWHERE


# CREATE KNOWLEDGE BASE OF ACTORS & FACES & CHARACTERS
for image_name in os.listdir(FACES_PATH):

    actor_name = image_name.rsplit('.')[0]
    if (actor_name[len(actor_name) - 1]).isdigit() :       # only use first image of each actor. TODO: make notes on face image filenames
        continue
    if actor_name not in name_mappings:
        name_mappings[actor_name] = actor_name + ":unknown_character"

    image = face_recognition.load_image_file(FACES_PATH + image_name)
    encoding = face_recognition.face_encodings(image)[0]
    actor_kb.append(dict({"actor":actor_name, "character":name_mappings[actor_name.lower()], "encoding":encoding}))
    #print("encoded " + image_name)

for record in actor_kb:
    print(record)

# TODO: RECOGNIZE FACES IN SELECTED SCENE
for clip_name in os.listdir(CLIPS_PATH):
    print('running recognizer over path: ' + CLIPS_PATH + clip_name)
    print('with knowledge base: '  + actor_kb)
    video_face_recognition.run(CLIPS_PATH + clip_name, actor_kb)

# TODO: COMPILE & PROCESS THE RESULTS INTO TABLE FORMAT
