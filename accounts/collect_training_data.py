# imports
from time import time
import imutils
import cv2, os
import sys
import random
import numpy as np
from django.conf import settings
import mediapipe as mp
from typing import NamedTuple
import face_recognition as fr

# calling mediapipe face detection
mp_face_detection = mp.solutions.face_detection


def generate_dataset(img, userID):
    """ "Function to save the reference frameage"""
    # try block to write the image in the directory
    try:
        os.mkdir(os.path.join(settings.BASE_DIR, "data", userID))
    except:
        pass

    # try block to catch if encoded is extracted from the first image
    try:
        train_encoding = fr.face_encodings(img)[0]

        cv2.imwrite(
            os.path.join(settings.BASE_DIR, "data", userID, "train.jpg"),
            img,
        )
        return True
    except:
        return False


def draw_boundary(img):
    """function to get region of interest from the face"""

    print(detect)
    height, width, _ = img.shape
    with mp_face_detection.FaceDetection(
        min_detection_confidence=0.5
    ) as face_detection:

        results = face_detection.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        # try block if no coordinate is extracted from the frame
        try:
            for detection in results.detections:
                x = int(detection.location_data.relative_bounding_box.xmin * width) - 10
                y = (
                    int(detection.location_data.relative_bounding_box.ymin * height)
                    - 10
                )
                w = (
                    int(detection.location_data.relative_bounding_box.width * width)
                    + 20
                )
                h = (
                    int(detection.location_data.relative_bounding_box.height * height)
                    + 20
                )
                coords = [x, y, w, h]
        except:
            coords = []
        print(coords)
    return coords


def detect(img, userID):
    """Method to detect the features"""

    # Return the x,y coordinates and width and height of rectangle if face is detected
    coords = draw_boundary(img)

    if len(coords) == 4:
        # Updating region of interest by cropping image
        roi_img = img[
            coords[1] : coords[1] + coords[3], coords[0] : coords[0] + coords[2]
        ]
        # resizing the image
        roi_img = cv2.resize(roi_img, (100, 100))
        # img_id to make the name of each image unique
        isImageOk = generate_dataset(roi_img, userID)
        return isImageOk
    return False


def collectTrainingData(userID):
    """function to get the reference"""

    video_capture = cv2.VideoCapture(
        os.path.join(settings.BASE_DIR, "media", "user", "videos", userID + ".mp4")
    )

    # Initialize img_id with 0
    fps = video_capture.get(cv2.CAP_PROP_FPS)
    amountOfFrames = video_capture.get(cv2.CAP_PROP_FRAME_COUNT)
    # debug statement
    print("fps ===> ", fps, "total frames ==> ", amountOfFrames)
    resp = {"Success": False, "Message": "Face not registered. Please try again."}
    while video_capture.isOpened():

        # Reading image from video stream
        success, img = video_capture.read()
        if not success:
            video_capture.grab()
            break

        isImageOk = detect(img, userID)
        if isImageOk:
            resp = {"Success": True, "Message": "Face registered."}
            break

    # removing the video once frame is extracted
    os.remove(
        os.path.join(settings.BASE_DIR, "media", "user", "videos", userID + ".mp4")
    )
    return resp
