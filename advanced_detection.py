import numpy as np
import copy
import cv2
from matplotlib import pyplot as plt

import time
import tkinter

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

cap = cv2.VideoCapture(0)

eye_position_values = [0,0,0,0,0,0,0,0,0,0,0]
initial_position = []
proper_posture_position = 35

top = tkinter.Tk()
starttime = time.time()

def calibrate_position(img, gray):
    
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
			
			new_ey = copy.deepcopy(ey)
			initial_position.append(new_ey)
			
			print(ey)
			print("calibration")
			
			cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),1)
			
			cnt_eye = cnt_eye + 1
		

	cv2.imshow('frame', img)
	
def calibration_loop():
	starttime = time.time()
	while (time.time() - starttime < 10):
		ret, frame = cap.read()
		frame = cv2.resize(frame, (600, 350))
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		calibrate_position(frame, gray)
	proper_posture_position = sum(initial_position) / len(initial_position)
	print(proper_posture_position)
	print ("calibrated")
	
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
			print (ey > proper_posture_position + 5)
			if ey > proper_posture_position + 5:
				print("you are slouching")
			else: 
				print("you are not slouching")

			cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),1)
            
			cnt_eye = cnt_eye + 1


            
	cv2.imshow('frame', img)
	
def countdown(t):
	while t:
		mins, secs = divmod(t, 60)
		timeformat = '{:02d}:{:02d}'.format(mins, secs)
		print(timeformat, end='\r')
		time.sleep(1)
		t -= 1
	print ("Break is over.")
	
def backToWork():
	print ("Please re-calibrate your posture.")
	B = tkinter.Button(top, text ="Calibrate", command = calibration_loop)
	B.pack()

if __name__ == '__main__':
	calibration_loop()
	
	while(True):
		starttime = time.time()
		while (time.time() - starttime < 60):
			ret, frame = cap.read()
			frame = cv2.resize(frame, (600, 350))
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			
			detect_and_draw(frame, gray)
			if cv2.waitKey(1) & 0xFF == ord('q'):
				quit()
		print ("You have been working for one hour. Take a break!")
		countdown(15)
		backToWork()
		if cv2.waitKey(1) & 0xFF == ord('q'):
			quit()
    # When everything done, release the capture
	cv2.destroyAllWindows()