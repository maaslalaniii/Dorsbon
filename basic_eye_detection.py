import numpy as np
import cv2
from matplotlib import pyplot as plt
import time


face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

cap = cv2.VideoCapture(0)

eye_position_values = [0,0,0,0,0,0,0,0,0,0,0]
proper_posture_position = 35

def detect_and_draw(img, gray):
    
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    # cv2.line(img, (0, 175), (600, 175), (0,255,0), 1)                


    for (x,y,w,h) in faces:
        img = cv2.rectangle(img, (x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        max_eyes = 2
        cnt_eye = 0
        for (ex,ey,ew,eh) in eyes:
            if(cnt_eye == max_eyes):
                break;

            #change dimensions
            ex = int(ex + (ew/6))
            ew = int(ew - (ew/6))
            ey = int(ey + (eh/3))
            eh = int(eh/3)
            
            print(ey)

            if ey > proper_posture_position + 5:
                print("you are slouching")
            else: 
                print("you are not slouching")

            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),1)
            
            cnt_eye = cnt_eye + 1


            
    cv2.imshow('frame', img)

if __name__ == '__main__':
    starttime = time.time()
    while(True):
        if (time.time() - starttime > 100):
            print("You have been working too long, take a break!")
            starttime = time.time()
        ret, frame = cap.read()
        frame = cv2.resize(frame, (600, 350))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        detect_and_draw(frame, gray)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # When everything done, release the capture
    cv2.destroyAllWindows()