import json
import pickle
import sys

MVAD_DATA_DIR = "/Users/daniel/Documents/FYP/M_Vad_Names/"
MVAD_TRACK_FILENAME = "mvad-names.pkl"
SCENE_METADATA_PATH = "scene_mvad_data.json"
MOVIE_NAME = "21_JUMP_STREET"
CHARACTER_NAMES = ["Molly","Schmidt", "Jenko"]

scene_gs_metadata = []
with open(SCENE_METADATA_PATH,'r') as data_file:
    scene_gs_metadata = json.load(data_file)
'''
for i in range(0,len(scene_gs_metadata)):
    print(scene_gs_metadata[i]["mvad_clip_numbers"])
    print(len(scene_gs_metadata[i]["mvad_clip_numbers"]))
'''
'''
### Technical details

The dataset file is a pickle object containing a python dictionary, structured as follows:

```
mvad-names.pkl
 └── <MOVIE>
      ├── 'characters'
      |    └── <CHARACTER>
      |         └── 'DVS<CLIP-ID>'  -> tracks
      └── 'videos'
           └── 'DVS<CLIP-ID>'
                └── <CHARACTER>  -> tracks
```

where `tracks` is a list of bounding boxes containing the face of the character in the form `(frame-id, x_min, y_min, x_max, y_max)`.

'''
def get_highest_frame_index(tracks):
    max = tracks[0][0][0]
    for child_list in tracks:
        for track in child_list:
            if track[0] > max:
                max = track[0]
    return max

def get_track_count(tracks):
    count = 0
    for child_list in tracks:
        count += len(child_list)
    return count

scene_gs = []
with open(MVAD_DATA_DIR + MVAD_TRACK_FILENAME, 'r+b') as data_file:
    
    mvad_info = pickle.load(data_file)
    mvad_info_vids = {}
    mvad_info_vids = mvad_info[MOVIE_NAME]["videos"]
    del mvad_info
    scene_dvs_lists = [scene_gs_metadata[i]["mvad_clip_numbers"] for i in range(0,len(scene_gs_metadata))]
    print(scene_dvs_lists)
    max_scene_frame_index = -1
    for i in range(0,len(scene_dvs_lists[1])):
        print("\nFor scene 1 DVS {}".format(scene_dvs_lists[1][i]))
        #print(mvad_info_vids["DVS" + str(scene_dvs_lists[1][i])].keys())
        for name, tracks in mvad_info_vids["DVS" + str(scene_dvs_lists[1][i])].items():
            #print("\tHighest frame index for {}: ".format(name) + str(get_highest_frame_index(tracks)))
            track_max = get_highest_frame_index(tracks)
            if track_max > max_scene_frame_index:
                max_scene_frame_index = track_max
            #print("Track count for {}: {}".format(name, get_track_count(tracks) ))
        #print("Estimate number of frames in scene 1 DVS{}: {}".format(scene_dvs_lists[1][i],max_scene_frame_index + 1))
        frame_count_estimate = max_scene_frame_index + 1
        for name in CHARACTER_NAMES:
            <if name not in data append min value to table>
            print("\t{}: {}".format(name, (float(get_track_count( mvad_info_vids["DVS" + str(scene_dvs_lists[1][i]) ][name] )) / frame_count_estimate )*100 ) )

    #print("sc.1, first DVS for Molly: " + str(mvad_info_vids["DVS" + str(scene_dvs_lists[1][1])]["Molly"]))


    '''
    TODO: get table of these results, row for each actor, each column a GS scene percentage. Plot these in bar chart (not stacked, but side-by-side bars for each scene) 
    '''
