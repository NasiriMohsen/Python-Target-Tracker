import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2 as cv
import RPi.GPIO as rp
from time import sleep

def map( x, in_min,in_max, out_min, out_max):
    maps = ((x - in_max)*(out_max-out_min)/(in_max-in_min)+out_min+10)
    return maps

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
pwm2.start(2)

webcam = PiCamera()
webcam.resolution = (640,480)
webcam.framerate = 90
video = PiRGBArray(webcam,size=(640,480))
pwm2.ChangeDutyCycle(2)
for i in range (2,12,1):
    #pwm1.ChangeDutyCycle(dty)
    pwm2.ChangeDutyCycle(i)
    sleep(1)
