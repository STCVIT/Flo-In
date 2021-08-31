import numpy as np                                                           # Imports
from PIL import Image
import os, cv2
import shutil
import time
from django.conf import settings
import statistics


def delete_images(userID):                                                   # function to delete images after use 
    shutil.rmtree(os.path.join(settings.BASE_DIR,"data",userID))

def split_data(userID):                                                      # function to distribute images to test and train folders of a user
    pth = os.path.join(settings.BASE_DIR,"data",userID)                      
    dir_list = os.listdir(pth)
    size = len(dir_list)
    os.mkdir(os.path.join(settings.BASE_DIR,"data",userID,"train"))
    os.mkdir(os.path.join(settings.BASE_DIR,"data",userID,"test"))           

    for i in range(size):
        orignal = dir_list[i]
        orignal = os.path.join(settings.BASE_DIR,"data",userID,orignal)
        if(i<15):
            target = os.path.join(settings.BASE_DIR,"data",userID,"train")
            shutil.move(orignal, target)
        else:
            target = os.path.join(settings.BASE_DIR,"data",userID,"test")
            shutil.move(orignal, target)


def generate_confidense_level(userID):                                        #function for generating threshold confidence level for authentication
    pth = os.path.join(settings.BASE_DIR,"data",userID,"test")
    dir_list = os.listdir(pth)
    
    clf = cv2.face.LBPHFaceRecognizer_create()
    if(os.path.exists(os.path.join(settings.BASE_DIR,f"classifiers",userID+".xml"))):              #loading user classifier xml file
        clf.read(os.path.join(settings.BASE_DIR,f"classifiers",userID+".xml"))

    
    confidence = []
    for image in dir_list:
        img = Image.open(os.path.join(settings.BASE_DIR,"data",userID,"test",image)).convert('L')      #opening test images and converting them to grayscale
        imageNp = np.array(img, 'uint8')                                                               #converting images to array
        idd, conf = clf.predict(imageNp)                                                               #calling predict function
        if idd == 1:
            print(str(conf) + "       confi--------------------------------------")
            confidence.append(conf)

    mean_conf = statistics.mean(confidence)
    sd_conf = statistics.stdev(confidence)                                                            #calculating standard deviation of confidence level generated

    custom_confidence = mean_conf + (sd_conf) + 30                                                 #calculating variance of confidence level generated and adding buffer for threshold authentication
    
    return 85 if (custom_confidence<=85) else custom_confidence                                       #setting 85 as threshold if calculated level is less than 85
    
    

    
def train_classifier(userID):                                                 #function to extract embeddings from train images
    pth = os.path.join(settings.BASE_DIR,"data",userID,"train")
    dir_list = os.listdir(pth)  

    faces = []
    ids = []

    for image in dir_list:
        img = Image.open(os.path.join(settings.BASE_DIR,"data",userID,"train",image)).convert('L')      #opening and converting images to grayscale
        imageNp = np.array(img, 'uint8')                                                                #converting images to array
        faces.append(imageNp)
        ids.append(1)
    
    ids = np.array(ids)

    clf = cv2.face.LBPHFaceRecognizer_create()                                                          #calling lbphf recognizer
    clf.train(faces, ids)                                                                               #training recognizer
    clf.write(os.path.join(settings.BASE_DIR,"classifiers",userID+".xml"))                              #saving embeddings in xml file


def generate_classifier(userID):                                                                        #calling functions
    resp = {"Success":True, "Message":"Face registered successfully"}
    try:
        os.remove(os.path.join(settings.BASE_DIR,"classifiers",userID+".xml"))
    except: 
        pass
    split_data(userID)
    conf=80
    train_classifier(userID)
    # try:
    conf = generate_confidense_level(userID)
    delete_images(userID)
    # except:
    #     resp=resp = {"Success":False, "Message":"Face not registered. Please try again."}
    if not os.path.isfile(os.path.join(settings.BASE_DIR,"classifiers",userID+".xml")):
        resp = {"Success":False, "Message":"Face not registered. Please try again."}
    return conf, resp


