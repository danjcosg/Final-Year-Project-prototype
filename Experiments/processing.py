#read in the output lines.
#lines are comma separated values:
#   FRAME, []
#Line is an list containing list of names

lines = [['None'],['Terry','None'],[]]

def getPercentages(lines, FPS = len(lines)):
    n_frames = len(lines)
    frames_per_bucket = int(FPS) #round up or down? This is crude if FPS isn't integer
    n_buckets = int(n_frames // frames_per_bucket) + 1
    buckets = [[] for i in range(0, n_buckets)]

    for frame_number, value in enumerate(lines, 1):
        buckets[int(frame_number//frames_per_bucket)].append(lines[frame_number - 1])
    for elem in buckets.__iter__():
        print(elem)
