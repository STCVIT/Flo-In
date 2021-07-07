from time import time
from imutils.video import VideoStream
import imutils
import cv2,os
import time
import random
import numpy as np
from django.conf import settings

# Loading classifiers
faceCascade = cv2.CascadeClassifier(os.path.join(
			settings.BASE_DIR,'opencv_haarcascade_data/haarcascade_frontalface_default.xml'))

# Method to generate dataset to recognize a person
def generate_dataset(img, userID):
    # write image in data dir
    try:
        os.mkdir(os.path.join(settings.BASE_DIR,"data",userID))
    except:
        pass
    cv2.imwrite(os.path.join(settings.BASE_DIR,"data",userID,f"{random.randint(0,1000)}.jpg"), img)

# Method to draw boundary around the detected feature
def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text):
    # Converting image to gray-scale
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # detecting features in gray-scale image, returns coordinates, width and height of features
    features = classifier.detectMultiScale(gray_img, scaleFactor, minNeighbors, minSize=(30,30))
    coords = []
    print(features)
    # drawing rectangle around the feature and labeling it
    for (x, y, w, h) in features:
        cv2.rectangle(img, (x,y), (x+w, y+h), color, 2)
        cv2.putText(img, text, (x, y-4), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 1, cv2.LINE_AA)
        coords = [x, y, w, h]
    return coords

# Method to detect the features
def detect(img, faceCascade, userID):
    coords = draw_boundary(img, faceCascade, 1.1, 10, (255,0,0), "Face")
    # If feature is detected, the draw_boundary method will return the x,y coordinates and width and height of rectangle else the length of coords will be 0
    print(coords)
    if len(coords)==4:
        # Updating region of interest by cropping image
        roi_img = img[coords[1]:coords[1]+coords[3], coords[0]:coords[0]+coords[2]]
        # img_id to make the name of each image unique
        generate_dataset(roi_img, userID)
    return img


def collectTrainingData(userID):
    video_capture = cv2.VideoCapture(os.path.join(settings.BASE_DIR,"media","user","videos",userID+".mp4"))

    # Initialize img_id with 0
    img_id = 0
    while (video_capture.isOpened()):
        #print("Collected ", img_id," images")
        # Reading image from video stream
        success, img = video_capture.read()
        # img = imutils.resize(img, width=480)
        # print(np.array(img.shape))
        # Call method we defined above
        img_id += 1
        img = detect(img, faceCascade, userID)
        if img_id>15:
            break