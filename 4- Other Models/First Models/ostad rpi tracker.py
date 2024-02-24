import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2 as cv
import RPi.GPIO as rp
from time import sleep

kp = 100
servo1 = 21
servo2 = 20
deltadt = 0.1
dt1 = 4
dt2 = 7
rp.setmode(rp.BCM)
rp.setwarnings(False)
rp.setup(servo1,rp.OUT)
rp.setup(servo2,rp.OUT)
pwm1 = rp.PWM(servo1,50)
pwm2 = rp.PWM(servo2,50)
pwm1.start(4)
pwm2.start(7)

webcam = PiCamera()
webcam.resolution = (1296,730)
webcam.framerate = 30
video = PiRGBArray(webcam,size=(1296,730))

for frames in webcam.capture_continuous(video, format="bgr", use_video_port=True):
    
    frame = frames.array

    mrkzy = int(len(frame)/2)
    mrkzx = int(len(frame[0])/2)

    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    minf = np.array([100,165,0])
    maxf = np.array([165,255,255])

    binary = cv.inRange(hsv, minf, maxf)
    medianed = cv.medianBlur(binary, 25)  

    filterd = cv.bitwise_and(frame,frame, mask= medianed)
    im2, contours, hierarchy = cv.findContours(medianed,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)  
    try:
        if len(contours) > 0:
            cnt = max(contours, key = cv.contourArea)
            (x1,y1), radius=cv.minEnclosingCircle(cnt)
            cntx = int(x1)  
            cnty = int(y1)
            center = (int(x1),int(y1))
            radius = int(radius)
            x,y,w,h = cv.boundingRect(cnt)
            cv.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            cv.circle(frame,center,radius,(0,0,255),2)
            cv.circle(frame,center,2,(255,0,0),4) 
    errorx = mrkzx - cntx
    pwmx = kp*errorx
    
    rpwm1.ChangeDutyCycle(dt1)
    pwm2.ChangeDutyCycle(dt2)
    cv.imshow('frame',frame)
    
    ikey = cv.waitKey(5)
    video.truncate(0)
    if (ikey==ord("q")):
        cv.destroyAllWindows()
        pwm1.stop()
        pwm2.stop()
        rp.cleanup()
        break