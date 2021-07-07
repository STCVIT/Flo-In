import cv2
import os
from django.conf import settings

# Loading classifier
faceCascade=cv2.CascadeClassifier(os.path.join(settings.BASE_DIR,'opencv_haarcascade_data/haarcascade_frontalface_default.xml'))

def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, clf):
    # Converting image to gray-scale
    img=cv2.normalize(img,img,0,255, cv2.NORM_MINMAX)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    img = clahe.apply(img)
    # detecting features in gray-scale image, returns coordinates, width and height of features
    for i in range(10):
        features = classifier.detectMultiScale(img, scaleFactor, minNeighbors)
        print(features)
        if not features==():
            break
    coords = []
    k = "Unauthorised"
    confidence = 1000
    # drawing rectangle around the feature and labeling it
    for (x, y, w, h) in features:
        img = cv2.rectangle(img, (x,y), (x+w, y+h), color, 2)
        # Predicting the id of the user
        idd, confidence = clf.predict(img[y:y+h, x:x+w])
        # Check for id of user and label the rectangle accordingly
        print(idd,"|||", confidence)
        if idd==1 and confidence<80:
            k = "Authorised"
        coords = [x, y, w, h]
    return img, coords, k

# Method to recognize the person
def recognize(img, clf, faceCascade):
    gray_img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    img, coords, k = draw_boundary(gray_img, faceCascade, 1.1, 10, (255, 255, 255), clf)
    return k

def authenticate_user(userID, image):
    # Loading custom classifier to recognize
    clf = cv2.face.LBPHFaceRecognizer_create()
    if(os.path.exists(os.path.join(settings.BASE_DIR,f"classifiers",userID+".xml"))):
        clf.read(os.path.join(settings.BASE_DIR,f"classifiers",userID+".xml"))
    # Capturing real time video stream. 0 for built-in web-cams, 0 or -1 for external web-cams
    img = cv2.imread(image)
    # img = cv2.resize(img,(400,500))
    # os.remove(image)
    print(img.shape)
    # Reading image from 
    img = recognize(img, clf, faceCascade)
    # os.remove(image)
    return img

