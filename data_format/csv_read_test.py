import os

FILM_NAME = "21_jump_street"

ROUND1_SCENES_DIR = "./round_1/" + FILM_NAME + "/"
ROUND2_SCENES_DIR = "./round_2/" + FILM_NAME + "/"


round1_data = []
round2_data = []
for i in range(0,5):
    print("**\nAttempting to open file at directory: {}".format( ROUND1_SCENES_DIR + 'scene_{}/'.format(i) + "{}_scene_{}_info.pkl".format(FILM_NAME, i) ) )
    file1 = open(ROUND1_SCENES_DIR + 'scene_{}/'.format(i) + "{}_scene_{}_results.csv".format(FILM_NAME, i), 'r')
    file2 = open(ROUND2_SCENES_DIR + 'scene_{}/'.format(i) + "{}_scene_{}_results.csv".format(FILM_NAME, i), 'r')
    print("Done\n")

    lines1 = []
    lines2 = []
    print("attempting to read first 4 lines of files:")
    for i in range(0,4):
        print("file1[{}]:".format(i))
        lines1.append(file1.readline())
        print(lines1[i])

        print("file2[{}]:".format(i))
        lines2.append(file2.readline())
        print(lines2[i])
        input("continue?")

    print("\nAdded all actor lines from scene {} data".format(i))
    print("\tLines 1:")
    print(lines1)
    print("\tLines 2:")
    print(lines2)

    input("continue?")

    '''
    CONVERT LINES TO A <NAME:PERCENTAGE_LIST> DICTIONARY 
    round1_data.append(lines1[0])
    round2_data.append(lines2[0])
    '''

    file1.close()
    file2.close()
    print("Successfully read all rounds for scene {}".format(i))

'''
differences = []
for scene_index in range(0,len(round1_data)):
    differences.append({})
    for actor_name, percentages in round1_data[scene_index].items():
        differences[scene_index][actor_name] = []
        for i in range(0, len(percentages)):
            difference = round1_data[scene_index][actor_name][i] - round2_data[scene_index][actor_name][i]
            differences[scene_index][actor_name].append(difference)
'''