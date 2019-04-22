    # READ FRAME IN (OpenCV)

    # Grab a single frame of video
    ret, frame = input_movie.read()
    frame_number += 1

    # Quit when the input video file ends
    if not ret:
        break

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_frame = frame[:, :, ::-1]

    # BEGIN FACE DETECTION & ENCODING OVER THE FRAME. (find ALL faces in the frame. NB: Encoding is like analysing a face. Recognition is encoding + comparing to some kb of encodings)
    """
    Returns an array of bounding boxes of human faces in a image
    :param img: An image (as a numpy array)
    :param number_of_times_to_upsample: How many times to upsample the image looking for faces. Higher numbers find smaller faces.
    :param model: Which face detection model to use. "hog" is less accurate but faster on CPUs. "cnn" is a more accurate
                  deep-learning model which is GPU/CUDA accelerated (if available). The default is "hog".
    :return: A list of tuples of found face locations in css (top, right, bottom, left) order
    """
    face_locations = face_recognition.face_locations(rgb_frame)
    detected_faces_encodings = face_recognition.face_encodings(rgb_frame, face_locations, 2)

    # COMPARE FACES FOUND IN IMAGE TO KNOWN FACES, THEN SAVE NAMES OF THOSE RECOGNIZED
    recognized_faces_names = []
    encodings_match = []
    tolerance = 0.6
    for face_encoding in detected_faces_encodings:

        # calculate Euclidian distance (similarity) between this face encoding and each known face encodings. 
        print("calculating encodings_match. Should be list of Booleans, size equal to No. the known faces")
        encodings_match = [np.linalg.norm(known_encodings[i] - face_encoding, 1) <= tolerance for i in range(0, len(known_encodings))]
        print("len encodings match: ")
        name = None
        for i in range(0, len(known_encodings)):
            if encodings_match[i]:
                name = known_characters[i]
                break
        recognized_faces_names.append(name)
