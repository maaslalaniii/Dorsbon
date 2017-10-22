import cv2;
import numpy as np;
import tkinter;
import time;

top = tkinter.Tk()

def calibrate():
  startTime = time.time()
  eye_position_values = []
  
  while (time.time() - startTime <= 3):
  	#eye_position_values.append(ey)
  	pass

  average = sum(eye_position_values) / len(eye_position_values)

# Code to add widgets will go here...
B = tkinter.Button(top, text ="Calibrate", command = calibrate)

B.pack()
top.mainloop()