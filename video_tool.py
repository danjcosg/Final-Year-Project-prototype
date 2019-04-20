from moviepy.editor import *

# video_path = "path/to/video"
# start = (h,m,s)
# end = (h,m,s)
# division_length = int in seconds
def writeSceneAsDivisions(video_path, output_dir, output_prefix, output_extension, start, end, division_length):
    # LOAD VIDEO TO CLIP OBJECT, FROM START TO END
    # Load video at video_path and select the subclip 00:00:50 - 00:00:60
    start_seconds = start[0]*60*60 + start[1]*60 + start[2]
    end_seconds = end[0]*60*60 + end[1]*60 + end[2]
    scene = VideoFileClip(video_path).subclip(start_seconds,end_seconds)
    print("\n\n**SUCCESSFULLY LOADED VIDEO**\n\n")
    # SPLIT THIS SCENE INTO ~ int(end - start / division_length) + 1 CLIPS
    # THEN WRITE TO OUTPUT DIRECTORY
    n = int( (end_seconds - start_seconds) / division_length)
    if end_seconds - start_seconds > division_length:
        for i in range(0,n):
            if i == n-1:
                subclip = scene.subclip(i*division_length, end_seconds - start_seconds)
            else:
                subclip = scene.subclip(i*division_length, (i+1) * division_length)
            if not output_dir[len(output_dir) - 1] == '/':
                output_dir.append('/')
            if not output_extension[0] == '.':
                output_extension = '.' + output_extension
            print("trying to write video file:\n")
            subclip.write_videofile(output_dir + output_prefix + "_" + str(i) + output_extension)
    else:
        scene.write_videofile(output_dir + output_prefix + "_" + str(i) + output_extension)

if __name__ == "__main__":
    video_path = "/Volumes/COSGRODATCD/FYP/21_jump_street/21_jump_street.mp4"
    output_dir = "/Volumes/COSGRODATCD/FYP/round1/21_jump_street/video_clips/"
    output_prefix = "scene_"
    output_extension = ".mp4"
    starts = [(1,31,16),(1,1,15),(0,55,48),(1,10,3),(0,51,9)]
    ends = [(1,31,28),(1,4,2),(0,56,20),(1,11,9),(0,52,12)]
    division_length = 10
    for i in range(0,5):    
        writeSceneAsDivisions(video_path, output_dir, output_prefix + str(i) + "division", output_extension, starts[i], ends[i], division_length)