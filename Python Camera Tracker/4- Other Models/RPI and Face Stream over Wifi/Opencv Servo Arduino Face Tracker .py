import cv2 as cv
import pygame as pg
import numpy as np
from pygameframe import framer
from Arduino import Arduino
import time

previousTime = 0
lasterrx = 0
lasterry = 0
Kp = 0.01
Kd = 0.03

def pid(currtime,previousTime,err,lasterr,Kp,Kd):
    etime = currtime-previousTime               
    rateError = (err-lasterr)/etime   
    pid = (Kp*err)+(Kd*rateError)
    return pid

stime = time.time()
targetcas = cv.CascadeClassifier("C:/Users/Asus/Desktop/Code/Python-Opencv-clean-codes-master/Haarcascade/haarcascade_frontalface_alt.xml")

webcam = framer(1)
frame = webcam.frameread()
yframe = len(frame)
xframe = len(frame[0])
servox = 9
servoy = 10
servxp = 90
servyp = 150

arduino = Arduino()
arduino.Servos.attach(servox)
arduino.Servos.attach(servoy)
arduino.Servos.write(servox, servxp)
arduino.Servos.write(servoy, servyp)
#############################################
while True:
    frame = webcam.frameread()
    gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY) 
    target = targetcas.detectMultiScale(gray,1.1,8)    
    for (x,y,w,h) in target:
        targx = int(x+w/2)
        targy = int(y+h/2)
        cv.rectangle(frame,(x,y),(x+w,y+h),(255,255,0),2)
#############################################
        currtime = int(round((time.time()-stime)*1000))
        errx = int((xframe/2)-targx)
        erry = int((yframe/2)-targy)
        pidx = pid(currtime,previousTime,errx,lasterrx,Kp,Kd)
        pidy = pid(currtime,previousTime,erry,lasterry,Kp,Kd)
        print(int(pidx*100)/100,int(pidy*100)/100)
        lasterrx = errx
        lasterry = erry 
        previousTime = currtime
#############################################
        servxp = servxp + pidx
        servyp = servyp - pidy
    arduino.Servos.write(servox, servxp)
    arduino.Servos.write(servoy, servyp)
#############################################
    webcam.imshowrgb(frame)
    #cv.imshow("Window",frame)
    if ord("q") == cv.waitKey(1):
        arduino.Servos.detach(servox)
        arduino.Servos.detach(servoy)
        cv.destroyAllWindows()
        break