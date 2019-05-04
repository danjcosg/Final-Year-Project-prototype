import pickle
import os

FILM_NAME = "21_jump_street"

ROUND1_SCENES_DIR = "./round_1/" + FILM_NAME + "/"
ROUND2_SCENES_DIR = "./round_2/" + FILM_NAME + "/"


round1_data = []
round2_data = []
for i in range(0,5):
    print("attempting to get pickle at directory: {}".format( ROUND1_SCENES_DIR + 'scene_{}/'.format(i) + "{}_scene_{}_info.pkl".format(FILM_NAME, i) ) )
    pfile1 = open(ROUND1_SCENES_DIR + 'scene_{}/'.format(i) + "{}_scene_{}_info.pkl".format(FILM_NAME, i), 'r+b')
    pfile2 = open(ROUND2_SCENES_DIR + 'scene_{}/'.format(i) + "{}_scene_{}_info.pkl".format(FILM_NAME, i), 'r+b')
    
    data1 = pickle.load(pfile1)
    data2 = pickle.load(pfile2)
    print(data1)
    input("continue?")
    round1_data.append(data1[0])
    round2_data.append(data2[0])

    pfile1.close()
    pfile2.close()
    print("Successfully read all rounds for scene {}".format(i))

differences = []
for scene_index in range(0,len(round1_data)):
    differences.append({})
    for actor_name, percentages in round1_data[scene_index].items():
        differences[scene_index][actor_name] = []
        for i in range(0, len(percentages)):
            difference = round1_data[scene_index][actor_name][i] - round2_data[scene_index][actor_name][i]
            differences[scene_index][actor_name].append(difference)