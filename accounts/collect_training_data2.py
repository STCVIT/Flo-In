from time import time
import imutils
import cv2,os
import sys
import random
import numpy as np
from django.conf import settings
import mediapipe as mp
from typing import NamedTuple

mp_face_detection = mp.solutions.face_detection

# Loading classifiers
faceCascade = cv2.CascadeClassifier(os.path.join(settings.BASE_DIR,'opencv_haarcascade_data','haarcascade_frontalface_default.xml'))
#Preprocessing function

def prep(image): 
    image = cv2.GaussianBlur(image, (3,3), 0)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.normalize(image, image, 0, 255, cv2.NORM_MINMAX)
    image = cv2.equalizeHist(image)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    image = clahe.apply(image)
    return image

# Method to generate dataset to recognize a person
def generate_dataset(img, userID):
    # write image in data dir
    try:
        os.mkdir(os.path.join(settings.BASE_DIR,"data",userID))
    except:
        pass
    cv2.imwrite(os.path.join(settings.BASE_DIR,"data",userID,f"{random.randint(0,1000)}.jpg"), img)

def draw_boundary(img):
    print(detect)
    height , width = img.shape
    with mp_face_detection.FaceDetection(min_detection_confidence=0.5) as face_detection:

        results = face_detection.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        # print(results)
        try:
            for detection in results.detections:
                x = int(detection.location_data.relative_bounding_box.xmin * width)
                y = int(detection.location_data.relative_bounding_box.ymin * height)
                w = int(detection.location_data.relative_bounding_box.width * width)
                h = int(detection.location_data.relative_bounding_box.height * height)
                coords=[x,y,w,h]
        except:
            coords = []
        print(coords)
        print("----------------------------------")
    return coords



# Method to detect the features
def detect(img, userID):
    #print("detect")
    #img = preprocess(img)
    coords = draw_boundary(img)
    # If feature is detected, the draw_boundary method will return the x,y coordinates and width and height of rectangle else the length of coords will be 0
   # print(coords)
    if len(coords)==4:
        # Updating region of interest by cropping image
        roi_img = img[coords[1]:coords[1]+coords[3], coords[0]:coords[0]+coords[2]]
        #resizing the image 
        roi_img = cv2.resize(roi_img, (100 , 100))
        # img_id to make the name of each image unique
        generate_dataset(roi_img, userID)
    return img


def collectTrainingData(userID):
   # print("Collect Train")
    video_capture = cv2.VideoCapture(os.path.join(settings.BASE_DIR,"media","user","videos",userID+".mp4"))

    # Initialize img_id with 0
    img_id = 0
    while (video_capture.isOpened()):
        # Reading image from video stream
        success, img = video_capture.read()
        # Call method we defined above
       
        img = prep(img)  #preprocessing function
        img = detect(img, userID)
        img_id += 1
        #changed the no of images to 30 for custom confidense level
        if img_id>35:
            break
    os.remove(os.path.join(settings.BASE_DIR,"media","user","videos",userID+".mp4"))