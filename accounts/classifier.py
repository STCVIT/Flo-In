import numpy as np              # Imports
from PIL import Image
import os, cv2
import shutil
import time
from django.conf import settings


def delete_images(userID):      
    shutil.rmtree(os.path.join(settings.BASE_DIR,"data",userID))
    
def train_classifier(userID):
    print(userID)
    pth = os.path.join(settings.BASE_DIR,"data",userID)
    dir_list = os.listdir(pth)  

    faces = []
    ids = []

    for image in dir_list:
        img = Image.open(os.path.join(settings.BASE_DIR,"data",userID,image)).convert('L')
        imageNp = np.array(img, 'uint8')
        faces.append(imageNp)
        ids.append(1)
    
    ids = np.array(ids)

    clf = cv2.face.LBPHFaceRecognizer_create()
    clf.train(faces, ids)
    clf.write(os.path.join(settings.BASE_DIR,"classifiers",userID+".xml"))

    delete_images(userID)

