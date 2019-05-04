import os
import ast
import sys

FILM_NAME = "captain_america"

ROUND1_SCENES_DIR = "./round_1/" + FILM_NAME + "/"
ROUND2_SCENES_DIR = "./round_2/" + FILM_NAME + "/"
N_SCENES = 5

round1_data = []
round2_data = []
for i in range(0,5):
    print("**\nAttempting to open file at directory: {}".format( ROUND1_SCENES_DIR + 'scene_{}/'.format(i) + "{}_scene_{}_results.csv".format(FILM_NAME, i) ) )
    if not os.path.exists(ROUND1_SCENES_DIR + 'scene_{}/'.format(i) + "{}_scene_{}_results.csv".format(FILM_NAME, i)):
        print("Error: Path does not exist")
        sys.exit()
    file1 = open(ROUND1_SCENES_DIR + 'scene_{}/'.format(i) + "{}_scene_{}_results.csv".format(FILM_NAME, i), 'r')
    file2 = open(ROUND2_SCENES_DIR + 'scene_{}/'.format(i) + "{}_scene_{}_results.csv".format(FILM_NAME, i), 'r')
    print("Done\n")

    lines1 = []
    lines2 = []
    print("attempting to read first 4 lines of files:")
    for j in range(0,4):
        #print("file1[{}]:".format(j))
        lines1.append(file1.readline())
        #print(lines1[j])

        #print("file2[{}]:".format(j))
        lines2.append(file2.readline())
        #print(lines2[j])

    
    print("\n**Trying to convert lines in lines list to a <NAME:PERCENTAGE_LIST> dict ")
    print("\tLines1 => {}".format(lines1))
    # Lines look like this: ['channing_tatum,[0.0]\n', 'jonah_hill,[0.0]\n', 'brie_larson,[0.0]\n', 'dave_franco,[0.0]\n']
    r1_lines_as_dict = {}
    for string in lines1:
        parts = string.split(',')
        name = parts[0]   
        ##########
        data_list_string = ""
        if len(parts) > 2:
            for j in range(1,len(parts) - 1):
                data_list_string = data_list_string + parts[j] + ','
            data_list_string += parts[len(parts) - 1][:-1]
        else:
            data_list_string += parts[1][:-1]
        data_list = ast.literal_eval( data_list_string ) # Convert string representation of list to list'
        ##########

        r1_lines_as_dict[name] = data_list

    r2_lines_as_dict = {}
    for string in lines2:
        parts = string.split(',')
        name = parts[0]    
        ##########
        data_list_string = ""
        if len(parts) > 2:
            for j in range(1,len(parts) - 1):
                data_list_string = data_list_string + parts[j] + ','
            data_list_string += parts[len(parts) - 1][:-1]
        else:
            data_list_string += parts[1][:-1]
        data_list = ast.literal_eval( data_list_string ) # Convert string representation of list to list'
        ##########
        r2_lines_as_dict[name] = data_list
    '''
    print("Tried converting data for scene {}, round 1 & 2. please verify for round 1:".format(i))
    print()
    for name, percentage_list in r1_lines_as_dict.items():
        print("\t" + name + ': {}'.format(percentage_list))
        print("type of key: {}".format(type(percentage_list)))
    input("Continue?")
    #for string in lines2:
    '''

    print("\n**OK, Appending dictionary of results to round1 & round2 data lists")
    round1_data.append(r1_lines_as_dict)
    round2_data.append(r2_lines_as_dict)

    file1.close()
    file2.close()
    print("\n**Successfully read all rounds for scene {}!".format(i))

print()

for i in range(0,5):
    print("Data for scene {}".format(i))
    print("\tround1_data[{}] : ".format(i))
    for name, percentages in round1_data[i].items():
        print("\t\t{}:{}".format(name,percentages))
    print("\tround2_data[{}] :".format(i))
    for name, percentages in round2_data[i].items():
        print("\t\t{}:{}".format(name,percentages))

differences = []
for scene_index in range(0,len(round1_data)):
    differences.append({})
    for actor_name, percentages in round1_data[scene_index].items():
        differences[scene_index][actor_name] = []
        for i in range(0, len(percentages)):
            difference = round1_data[scene_index][actor_name][i] - round2_data[scene_index][actor_name][i]
            differences[scene_index][actor_name].append(difference)

print("\n--Differences calculated for each scene")
for i in range(0, N_SCENES):
    print("Differences for scene {} in {}:".format(i,FILM_NAME))
    for name, percentages in differences[i].items():
        print("\t" + name + ": {}".format(percentages))
