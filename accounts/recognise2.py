import cv2
import os
import numpy as np
from django.conf import settings
from PIL import Image
import mediapipe as mp
from typing import NamedTuple

mp_face_detection = mp.solutions.face_detection


# Loading classifier
faceCascade=cv2.CascadeClassifier(os.path.join(settings.BASE_DIR,'opencv_haarcascade_data/haarcascade_frontalface_default.xml'))

def prep(image): 
	image = cv2.GaussianBlur(image, (3,3), 0)
	image = cv2.normalize(image, image, 0, 255, cv2.NORM_MINMAX)
	#image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	#image = cv2.equalizeHist(image)
	clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
	image = clahe.apply(image)
	return image

def draw_boundary(img  , clf , userCONF):
    print("detect")
    height , width, _dim = img.shape
    with mp_face_detection.FaceDetection(min_detection_confidence=0.5) as face_detection:

        results = face_detection.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        # print(results)
        coords = []
        for detection in results.detections:
            x = int(detection.location_data.relative_bounding_box.xmin * width)
            y = int(detection.location_data.relative_bounding_box.ymin * height)
            w = int(detection.location_data.relative_bounding_box.width * width)
            h = int(detection.location_data.relative_bounding_box.height * height)
            coords=[x,y,w,h]
        print(coords)

    
    
    k = "Unauthorised"
    
    # Predicting the id of the user
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    roi_img = img[y:y+h, x:x+w]
    roi_img=prep(roi_img)
    roi_img = cv2.resize(roi_img, (100 , 100))
    print("------recognise dimension------ ", roi_img.shape)
    #img=cv2.equalizeHist(img)
    # img=cv2.normalize(img,img,0,255, cv2.NORM_MINMAX)
    # clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    # img = clahe.apply(img)
    cv2.imwrite("test.png", roi_img)
    idd, confidence = clf.predict(roi_img)
    # Check for id of user and label the rectangle accordingly
    print(idd,"|||", confidence)
    if idd==1 and confidence<userCONF:
        k = "Authorised"
    coords = [x, y, w, h]
    return img, coords, k

# Method to recognize the person
def recognize(img, clf, faceCascade, userCONF):
#    gray_img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    img, coords, k = draw_boundary(img,clf, userCONF)
    return k

def authenticate_user(userID, userCONF ,image):
    # Loading custom classifier to recognize
    clf = cv2.face.LBPHFaceRecognizer_create()
    if(os.path.exists(os.path.join(settings.BASE_DIR,f"classifiers",userID+".xml"))):
        clf.read(os.path.join(settings.BASE_DIR,f"classifiers",userID+".xml"))
    # Capturing real time video stream. 0 for built-in web-cams, 0 or -1 for external web-cams
    img = cv2.imread(image)
    # img = Image.open(os.path.join(settings.BASE_DIR,"682.jpg")).convert('L')
    # img = np.array(img, 'uint8')
    os.remove(image)
    # Reading image from 
    k = recognize(img, clf, faceCascade, userCONF)
    return k
