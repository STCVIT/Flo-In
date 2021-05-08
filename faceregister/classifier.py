import numpy as np 
from PIL import Image
import os, cv2
from django.conf import settings


def delete_images(email):
    for imgid in range(100):
        if(os.path.exists(os.path.join(settings.BASE_DIR,"data",f"{email}_{imgid}.jpg"))):
            os.remove(os.path.join(settings.BASE_DIR,"data",f"{email}_{imgid}.jpg"))



def train_classifier(email):
    path = []
    for i in range(100):
        if(os.path.exists(os.path.join(settings.BASE_DIR,"data",f"{email}_{i}.jpg"))):
            path.append(os.path.join(os.path.join(settings.BASE_DIR,"data",f"{email}_{i}.jpg")))
    

    faces = []
    ids = []

    for image in path:
        # print(image)
        img = Image.open(image).convert('L')
        imageNp = np.array(img, 'uint8')

        faces.append(imageNp)
        ids.append(1)
    
    ids = np.array(ids)

    clf = cv2.face.LBPHFaceRecognizer_create()
    clf.train(faces, ids)
    clf.write(os.path.join(settings.BASE_DIR,f"classifiers/{email}.xml"))

    delete_images(email)

