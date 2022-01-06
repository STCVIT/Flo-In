import face_recognition as fr
import os
import cv2 as cv2
from django.conf import settings
import mediapipe as mp
from typing import NamedTuple

mp_face_detection = mp.solutions.face_detection


def encoding_recognise(userID, image):
    """
    This Function is used to authentticate the person face by comparing the encodings of
    image passed as parameter and image saved in database.

    userID -> unique Id of the user (used to get the image saved in database).
    image -> PATH of the iamge use to get the image to compare.

    """
    
    try:
        pth = os.path.join(settings.BASE_DIR, "data", userID)
        dir_list = os.listdir(pth)
        img_path = os.path.join(settings.BASE_DIR, "data", userID, "train.jpg")
        train_image = fr.load_image_file(img_path)

    except:
        resp = {"Success": False, "Message": "Please register your face!"}
        return resp

    img = cv2.imread(image)
    height, width, _dim = img.shape

    resp = {"Success": False, "Message": "Face not found . Please try again."}

    with mp_face_detection.FaceDetection(
        min_detection_confidence=0.5
    ) as face_detection:
        results = face_detection.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        print(results)
        coords = []

        # Can throw error if result.detction is NULL
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
            print(coords)
        except:
            return resp
        if len(coords) != 4:
            return resp

    roi_img = img[y : y + h, x : x + w]
    roi_img = cv2.resize(roi_img, (100, 100))
    cv2.imwrite(os.path.join(pth, "toVerify.jpg"), roi_img)
    testImage = fr.load_image_file(os.path.join(pth, "toVerify.jpg"))

    trainEncoding = fr.face_encodings(train_image)[0]

    """
    If face is not detected in the test image, below code will 
    throw out of range error.   
    """
    try:
        testEncoding = fr.face_encodings(testImage)[0]
    except:
        return resp

    distance = fr.face_distance([testEncoding], trainEncoding)
    print(f"=======>{distance}")
    if distance[0] < 0.45:
        resp = {
            "Success": True,
            "Message": "You are good to go! You can go ahead and set pin.",
        }
    else:
        resp = {
            "Success": False,
            "Message": "There is some error , Please register your face again ",
        }

    os.remove(image)
    return resp
