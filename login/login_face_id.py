import cv2
from matplotlib import pyplot
from mtcnn.mtcnn import MTCNN
import numpy as np
import os

def log_face(img, faces, user):
    '''
        Description:  Detect the face. 
        *image: name user
        *faces: detector of faces
            
        For detect the faces and return the pixels 
    '''
    user_login = user
    data = pyplot.imread(img)
    for i in range(len(faces)):
        x1,y1, width, height = faces[i]['box']
        x2,y2 = x1 + width, y1 + height
        pyplot.subplot(1, len(faces), i+1)
        pyplot.axis('off')
        face_reg = data[y1:y2, x1:x2]
        face_reg = cv2.resize(face_reg,(150,200), interpolation = cv2.INTER_CUBIC)
        cv2.imwrite(user_login+"LOG.jpg",face_reg)
        return pyplot.imshow(data[y1:y2, x1:x2])
    pyplot.show()
    
def check_similarity(imageA, imageB):
    '''
        Description:  Verify that the person who is entering is registered.
        *imageA: image of register
        *imageB: image of login
    
        Compare the key points of the registration image and the login image, returns the percentage of similarity  
    '''
    orb = cv2.ORB_create()
    kpa, first_decrip = orb.detectAndCompute(imageA, None)
    kpb, second_descrip = orb.detectAndCompute(imageB, None) 
    comp = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = True) 
    matches = comp.match(first_decrip, second_descrip)
    key_points = [i for i in matches if i.distance < 70]
    if len(matches) == 0:
        return 0
    return len(key_points)/len(matches) 


def facial_log(user):
    '''
    Description:  Function general for the facial login.
    *user: name user
    
    For capture the face with camera and save image like a login.
    '''
    capture = cv2.VideoCapture(0)            
    while(True):
        ret,frame = capture.read()              
        cv2.imshow('Facial Login',frame)        
        if cv2.waitKey(1) == 27:            
            break
    user_login = user    
    cv2.imwrite(user_login+"LOG.jpg",frame)     
    capture.release()                              
    cv2.destroyAllWindows()
    

    image = user_login + "LOG.jpg"
    pixels = pyplot.imread(image)
    detector = MTCNN()
    faces = detector.detect_faces(pixels)
    log_face(image, faces, user)

    
    files = os.listdir() 
    if user_login +".jpg" in files:   
        face_reg = cv2.imread(user_login+".jpg",0)  
        face_log = cv2.imread(user_login+"LOG.jpg",0)  
        seem = check_similarity(face_reg, face_log)
        if seem >= 0.975:
            return 1
        else:
            return 0
    else:
        return "User not found"
