import cv2
import os
from mtcnn.mtcnn import MTCNN
from matplotlib import pyplot
import numpy as np

def detect_face(image, faces, user):
    '''
    Description:  Detect the face. 
        *image: name user
        *faces: detector of faces
            
        For detect the faces and export the pixels 
    '''
    user_image = user
    data = pyplot.imread(image)
    for i in range(len(faces)):
        x1,y1,ancho, alto = faces[i]['box']
        x2,y2 = x1 + ancho, y1 + alto
        pyplot.subplot(1, len(faces), i+1)
        pyplot.axis('off')
        face_reg = data[y1:y2, x1:x2]
        face_reg = cv2.resize(face_reg,(150,200), interpolation = cv2.INTER_CUBIC)
        cv2.imwrite(user_image+".jpg", face_reg)
        pyplot.imshow(data[y1:y2, x1:x2])
    pyplot.show()

def facial_register(user):
    '''
    Description:  Function general for the facial register.
    *user: name user
    
    For capture the face with camera and save image like a register.
    '''
    capture = cv2.VideoCapture(0)               
    while True:
        ret, frame = capture.read()              
        cv2.imshow('Facial Register',frame)         
        if cv2.waitKey(1) == 27:            
            break
    user_image = user
    cv2.imwrite(user_image +".jpg",frame)       
    capture.release()                               
    cv2.destroyAllWindows()
    
    
    
    image = user_image + ".jpg"
    pixels = pyplot.imread(image)
    detector = MTCNN()
    faces = detector.detect_faces(pixels)
    detect_face(image, faces, user) 