import numpy as np              # Imports
from PIL import Image
import os, cv2
import shutil
import time
from django.conf import settings
import statistics


def delete_images(userID):      
    shutil.rmtree(os.path.join(settings.BASE_DIR,"data",userID))


def split_data(userID):
    pth = os.path.join(settings.BASE_DIR,"data",userID)
    dir_list = os.listdir(pth)
    os.mkdir(os.path.join(settings.BASE_DIR,"data",userID,"train"))
    os.mkdir(os.path.join(settings.BASE_DIR,"data",userID,"test"))

    for i in range(30):
        orignal = dir_list[i]
        orignal = os.path.join(settings.BASE_DIR,"data",userID,orignal)
        if(i<15):
            target = os.path.join(settings.BASE_DIR,"data",userID,"train")
            shutil.move(orignal, target)
        else:
            target = os.path.join(settings.BASE_DIR,"data",userID,"test")
            shutil.move(orignal, target)


def generate_confidense_level(userID):
    pth = os.path.join(settings.BASE_DIR,"data",userID,"test")
    dir_list = os.listdir(pth)
    
    clf = cv2.face.LBPHFaceRecognizer_create()
    if(os.path.exists(os.path.join(settings.BASE_DIR,f"classifiers",userID+".xml"))):
        clf.read(os.path.join(settings.BASE_DIR,f"classifiers",userID+".xml"))

    
    confidence = []
    for image in dir_list:
        img = Image.open(os.path.join(settings.BASE_DIR,"data",userID,"test",image)).convert('L')
        imageNp = np.array(img, 'uint8')
        idd, conf = clf.predict(imageNp)
        if idd == 1:
            # print("yes")
            print(conf)
            confidence.append(conf)

    mean_conf = statistics.mean(confidence)
    sd_conf = statistics.stdev(confidence)

    return mean_conf + sd_conf
    
    

    
def train_classifier(userID):
    #print(userID)
    pth = os.path.join(settings.BASE_DIR,"data",userID,"train")
    dir_list = os.listdir(pth)  

    faces = []
    ids = []

    for image in dir_list:
        img = Image.open(os.path.join(settings.BASE_DIR,"data",userID,"train",image)).convert('L')
        imageNp = np.array(img, 'uint8')
        faces.append(imageNp)
        ids.append(1)
    
    ids = np.array(ids)

    clf = cv2.face.LBPHFaceRecognizer_create()
    clf.train(faces, ids)
    clf.write(os.path.join(settings.BASE_DIR,"classifiers",userID+".xml"))

    # delete_images(userID)

def generate_classifier(userID):
    split_data(userID)
    train_classifier(userID)
    conf = generate_confidense_level(userID)
    #delete_images(userID)
    return conf


