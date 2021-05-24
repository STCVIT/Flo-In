import numpy as np 
from PIL import Image
import os, cv2
import shutil
import time
from django.conf import settings


def delete_images(email):
    shutil.rmtree(os.path.join(settings.BASE_DIR,"data",email))


def train_classifier(email):
    path = []
    for i in range(100):
        try:
            if(os.path.exists(os.path.join(settings.BASE_DIR,"data",f"{email}_{i}.jpg"))):
                path.append(os.path.join(os.path.join(settings.BASE_DIR,"data",f"{email}_{i}.jpg")))
        except:
            pass    

    faces = []
    ids = []

    for image in path:
        img = Image.open(image).convert('L')
        imageNp = np.array(img, 'uint8')

        faces.append(imageNp)
        ids.append(1)
    
    ids = np.array(ids)

    clf = cv2.face.LBPHFaceRecognizer_create()
    clf.train(faces, ids)
    clf.write(os.path.join(settings.BASE_DIR,f"classifiers/{email}.xml"))

    delete_images(email)

