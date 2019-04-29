#analyse and process each clip
#pipeline: https://www.draw.io/?state=%7B%22ids%22:%5B%221jtC9XGqnJuqxOkcRz7jqPCOd6H2ZsXp3%22%5D,%22action%22:%22open%22,%22userId%22:%22115019067398552559764%22%7D#G1jtC9XGqnJuqxOkcRz7jqPCOd6H2ZsXp3

import video_face_recognition
import face_recognition
import os
import face_recognition_models
import dlib
import cv2
import time
import pickle

FILM_NAME = "captain_america"
OUTPUT_DIR = "../results/round_2/" + FILM_NAME + "/"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# GET QUERY

EXPERIMENT_DIR = "./"
FILM_DATA_DIR = "../data/round1_symlink/" + FILM_NAME + "/"
VIDEO_DIR = FILM_DATA_DIR + "video_clips/"
FACES_DIR = FILM_DATA_DIR + "faces/manual_poor/"
SCENES = ["scene_0","scene_1","scene_2","scene_3","scene_4"]

def get_div_dir(scene_number):
    return VIDEO_DIR + SCENES[scene_number] + '/'

# actor_kb structure: {"actor_name" : {"character_name":"", "image_path":""}}
actor_kb = {}
#name_mappings = {"channing_tatum":"jenko", "jonah_hill":"schmidt", "brie_larson" : "molly_tracey", "dave_franco":"eric_molson"}
name_mappings = {"chris_evans":"steve_rogers","hayley_atwell":"peggy_carter","sebastian_stan":"james_buchanan_barnes","tommy_lee_jones":"col_chester_phillips"}
# CREATE KNOWLEDGE BASE OF ACTORS & REFERENCE IMAGE PATHS & CHARACTERS RELEVANT TO QUERY
for name in name_mappings:
    actor_kb[name] = dict({"character":"","image_path":""})
    actor_kb[name]["character"] = name_mappings[name]
    if os.path.exists(FACES_DIR + name + ".jpg"):
        actor_kb[name]["image_path"] = FACES_DIR + name + ".jpg"
    else:
        for filename in os.listdir(FACES_DIR):
            parts = filename.split('.')
            if parts[0] == name:
                actor_kb[name]["image_path"] = FACES_DIR + name + parts[1]
                break
        else:
            print("\tWarning: couldn't find reference image for " + name)
            del actor_kb[name]

print("\n\nTried to create KB for actors, please verify:")
for key, data in actor_kb.items():
    print("\t{}:{}".format(key,data))

input("continue?")

# TODO: CHECK THAT WE CAN ACCESS VIDEOS
print("Checking that we can access video paths")
for i, scene in enumerate(SCENES):
    print("\n\tTesting for scene " + str(i))
    count = 0
    for vid_path in os.listdir(get_div_dir(i)):
        if os.path.exists(get_div_dir(i) + vid_path):
            count += 1
            print("\tgot path " + get_div_dir(i) + vid_path)
        else:
            print("\tcouldn't find path " + get_div_dir(i) + vid_path)
    print("\tFound {} paths".format(count))
    input("continue?")

# USING QUERY, THE VIDEO IS SPLIT INTO DIVISIONS, EACH DIVISION GETS A PERCENTAGE
# FOR DIVISION IN SCENE, RECOGNIZE FACES IN SELECTED DIVISION
for i, scene in enumerate(SCENES):
    # Initialize output stuff for this scene
    # Result format: list of percentages, for each actor in query. Element (percentage) is added for each division searched. 
    if not os.path.exists(OUTPUT_DIR + scene):
        os.makedirs(OUTPUT_DIR + scene)
    #print("trying to make output dir for scene {}".format(i))
    #input("continue?")
    results = {}
    for name in name_mappings:
        results[name] = []
    #print("Initialized results: \n\t{}".format(results))
    #input("Continue?")

    start_time = time.time()
    div_dir = get_div_dir(i)
    for j, video_path in enumerate(os.listdir(div_dir)):
        print("vid path : " + video_path)
        if video_path[0] == '.':
            continue
        # From this video division, get the percentage for each actor
        #print("iterating through videos. Video {}, vid path {}, div_dir {}".format(j, video_path, div_dir))
        info = video_face_recognition.getPercentages(div_dir + video_path, actor_kb, 3)
        percentages = info[0]
        for name, percentage in percentages.items():
            results[name].append(percentage) 
    stop_time = time.time()
    if os.path.exists(OUTPUT_DIR):
        dir = OUTPUT_DIR + scene + "/" 
    else:
        print("Couldn't find output directory for scene_{}".format(i))
        dir = OUTPUT_DIR
    out = open(dir + FILM_NAME + '_' + scene + "_results.csv", 'w')
    print("Writing results for scene {}".format(i))
    for actor, val in results.items():
        out.write("{},{}\n".format(actor,val))
    out.write("\nTime to process/sec, {}".format(stop_time - start_time))
    out.write("\nFrames analysed: {}/{}".format(info[1], info[2]))
    out.close()

    # TODO: COMPILE & PROCESS THE RESULTS INTO TABLE FORMAT
    # I want to DISPLAY results immediately as a histogram
    # And also PICKLE them for later analysis. The pickle should contain metadata about the experiment: Date, time, length of experiment vs length of video, the scene being analysed (eg: 21_jump_street_scene1, 21_jump_street_scene2)
    #pickle(results, i, SCENES[i], getTime, )
    #write a table to a new pickle file
    pickle_storage = {}
    pickle_filename = FILM_NAME + "_" + scene + "_info.pkl"
    for actor, val in results.items():
        pickle_storage[actor] = val
    #pickle_data = info + tuple(dict({"time": (stop_time - start_time), "film_name":FILM_NAME, "scene":scene}))
    with open(OUTPUT_DIR + scene + "/" + pickle_filename, 'w+b') as pfile:
        pickle.dump(pickle_storage, pfile)