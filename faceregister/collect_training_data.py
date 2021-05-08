from imutils.video import VideoStream
import imutils
import cv2,os,urllib.request
import time
from django.conf import settings

# Loading classifiers
faceCascade = cv2.CascadeClassifier(os.path.join(
			settings.BASE_DIR,'opencv_haarcascade_data/haarcascade_frontalface_default.xml'))

# Method to generate dataset to recognize a person
def generate_dataset(img, email, img_id):
    # write image in data dir
    cv2.imwrite(os.path.join(settings.BASE_DIR,"data",f"{email}_{img_id}.jpg"), img)

# Method to draw boundary around the detected feature
def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text):
    # Converting image to gray-scale
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # detecting features in gray-scale image, returns coordinates, width and height of features
    features = classifier.detectMultiScale(gray_img, scaleFactor, minNeighbors)
    coords = []
    # drawing rectangle around the feature and labeling it
    for (x, y, w, h) in features:
        cv2.rectangle(img, (x,y), (x+w, y+h), color, 2)
        cv2.putText(img, text, (x, y-4), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 1, cv2.LINE_AA)
        coords = [x, y, w, h]
    return coords

# Method to detect the features
def detect(img, faceCascade, email, img_id, check=False):
    coords = draw_boundary(img, faceCascade, 1.1, 10, (255,0,0), "Face")
    # If feature is detected, the draw_boundary method will return the x,y coordinates and width and height of rectangle else the length of coords will be 0
    if len(coords)==4:
        # Updating region of interest by cropping image
        roi_img = img[coords[1]:coords[1]+coords[3], coords[0]:coords[0]+coords[2]]
        # img_id to make the name of each image unique
        generate_dataset(roi_img, email, img_id)
        check=True

    return img, check

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
    
    def __del__(self):
        self.video.release()
	
    def get_frame(self, img_id):
        success, image = self.video.read()
        img, check = detect(image, faceCascade, "swarukharul", img_id)
        # Writing processed image in a new window
        cv2.imshow("face detection", img)
        ret, jpeg = cv2.imencode('.jpg', img)
        return jpeg.tobytes(), check


