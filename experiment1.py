#analyse and process each clip
#pipeline: https://www.draw.io/?state=%7B%22ids%22:%5B%221jtC9XGqnJuqxOkcRz7jqPCOd6H2ZsXp3%22%5D,%22action%22:%22open%22,%22userId%22:%22115019067398552559764%22%7D#G1jtC9XGqnJuqxOkcRz7jqPCOd6H2ZsXp3

import video_face_recognition
import face_recognition
import os
import face_recognition_models
import dlib
import cv2

# GET QUERY

EXPERIMENT_PATH = "~/Documents/FYP/Experiments/round1/21_jump_street/"
CLIPS_PATH = EXPERIMENT_PATH + "video_clips/"
SCENE = "scene_1"
FACES_PATH = "../../Experiments/round1/21_jump_street/faces/"

actor_kb = {}
name_mappings = {"channing_tatum":"jenko", "jonah_hill":"schmidt"}  #!!!!TEMPORARILY OVERWRITING PARAMETER, THIS SHOULD BE LOADED FROM ELSEWHERE

# CREATE KNOWLEDGE BASE OF ACTORS & FACES & CHARACTERS RELEVANT TO QUERY
# TODO: translate to dlib
for image_name in os.listdir(FACES_PATH):

    actor_name = image_name.rsplit('.')[0]
    if (actor_name[len(actor_name) - 1]).isdigit() :       # only use first image of each actor. TODO: make notes on face image filenames
        continue
    if actor_name not in name_mappings:
        name_mappings[actor_name] = actor_name + ":unknown_character"

    image = face_recognition.load_image_file(FACES_PATH + image_name)
    image = cv2.imread(FACES_PATH + image_name)
    encoding = face_recognition.face_encodings(image)[0]
    actor_kb[actor_name] = (dict({"character":name_mappings[actor_name.lower()], "encoding":encoding}))
    #print("encoded " + image_name)

# Initialize output table
# Result format: list of percentages, for each actor in query. Element (percentage) is added for each division searched. 
results = {}
for name, info in actor_kb.items():
    results[name] = []

# FOR DIVISION IN SCENE, RECOGNIZE FACES IN SELECTED DIVISION
# We query over a scene. Scene is divided into divisions.
for clip_name in os.listdir(CLIPS_PATH):
    
    percentages = video_face_recognition.getPercentages(CLIPS_PATH + clip_name, actor_kb)
    for name, percentage in percentages.items():
        results[name].append(percentage) 

# TODO: COMPILE & PROCESS THE RESULTS INTO TABLE FORMAT
# I want to display results immediately as a histogram
# And also pickle them for later analysis. The pickle should contain metadata about the experiment: Date, time, length of experiment vs length of video, the scene being analysed (eg: 21_jump_street_scene1, 21_jump_street_scene2)