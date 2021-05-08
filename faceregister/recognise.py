import cv2
import os
from django.conf import settings

def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text, clf):
    # Converting image to gray-scale
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # detecting features in gray-scale image, returns coordinates, width and height of features
    features = classifier.detectMultiScale(gray_img, scaleFactor, minNeighbors)
    coords = []
    k = False
    # drawing rectangle around the feature and labeling it
    for (x, y, w, h) in features:
        img = cv2.rectangle(img, (x,y), (x+w, y+h), color, 2)
        # Predicting the id of the user
        idd, confidence = clf.predict(gray_img[y:y+h, x:x+w])
        # Check for id of user and label the rectangle accordingly
        print(idd,"|||", confidence)
        if idd==1 and confidence<70:
            img = cv2.putText(img, "User Matched", (x, y-4), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 1, cv2.LINE_AA)
            k = True
        else:
            img = cv2.putText(img, "User Not Matched", (x, y-4), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 1, cv2.LINE_AA)
            k = False
        coords = [x, y, w, h]

    return img, coords, k

# Method to recognize the person
def recognize(img, clf, faceCascade):
    color = {"blue": (255, 0, 0), "red": (0, 0, 255), "green": (0, 255, 0), "white": (255, 255, 255)}
    img, coords, k = draw_boundary(img, faceCascade, 1.1, 10, color["white"], "Face", clf)
    print("Authenticated") if k else print("Not Authenticated")
    return img


# Loading classifier
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


def authenticate_user(username, userid):
    # Loading custom classifier to recognize
    clf = cv2.face.LBPHFaceRecognizer_create()
    if(os.path.exists(os.path.join(settings.BASE_DIR,f"classifiers/{email}.xml"))):
        clf.read(os.path.join(settings.BASE_DIR,f"classifiers/{email}.xml"))

    # Capturing real time video stream. 0 for built-in web-cams, 0 or -1 for external web-cams
    video_capture = cv2.VideoCapture(0)

    while True:
        # Reading image from video stream
        _, img = video_capture.read()
        # Call method we defined above
        img = recognize(img, clf, faceCascade)
        # Writing processed image in a new window
        cv2.imshow("face detection", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # releasing web-cam
    video_capture.release()
    # Destroying output window
    cv2.destroyAllWindows()
