import time;
import tkinter;

top = tkinter.Tk()

def countdown(t):
	while t:
		mins, secs = divmod(t, 60)
		timeformat = '{:02d}:{:02d}'.format(mins, secs)
		print(timeformat, end='\r')
		time.sleep(1)
		t -= 1
def backToWork():
	print ("Please re-calibrate your posture.")
	B = tkinter.Button(top, text ="Calibrate", command = calibrate)
	B.pack()
	top.mainloop()
	
countdown(300)
backToWork()