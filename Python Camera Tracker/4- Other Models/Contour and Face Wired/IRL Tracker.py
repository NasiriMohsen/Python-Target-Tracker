import serial
import time
import numpy as np
import cv2 as cv

def millis():
    return time.time()

def Limiter(x,a):
    if a ==2:
        if x >= 175:
            return 175   
        elif x <= 150:
            return 150
        else:
            return int(x) 
    else :
        if x >= 180:
            return 180   
        elif x <= 20:
            return 20
        else:
            return int(x) 
    

Arduino = serial.Serial("COM3",115200)

time.sleep(2)

def Servos(Sdata):
    x,y = Sdata
    Arduino.write(bytes(str(x)+","+str(y)+".", 'utf-8'))
    data = Arduino.readline()
    return data.decode("UTF-8").rstrip()

XServo = 95
YServo = 155
Servos((95,155))

newdata = (95,155)
olddata = (95,155)

Kp = 1
Kd = 0.2
Ki = 0.01
smt = 80

XError = 0
OldXError = 0
DeltaXError = 0 
SlopeXError = 0
AreaXError = 0

YError = 0
OldYError = 0
DeltaYError = 0 
SlopeYError = 0
AreaYError = 0

TargetCascade = cv.CascadeClassifier('./Face.xml')

webcam = cv.VideoCapture(1)

Frame = webcam.read()[1]
YcFrame = int(len(Frame)/2)
XcFrame = int(len(Frame[0])/2)

NewTime = millis()


hsvmin = np.array([110, 45, 0])
hsvmax = np.array([125, 255, 255])


while True:
    RealFrame = webcam.read()[1]
    Frame = np.copy(RealFrame)
    RealFrame = cv.medianBlur(RealFrame,25)
    hsv = cv.cvtColor(RealFrame,cv.COLOR_RGB2HSV)
    binaried = cv.inRange(hsv,hsvmin,hsvmax)
    filtered = cv.bitwise_and(RealFrame,RealFrame,mask = binaried)

    contours = cv.findContours(binaried,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)[0]

    if len(contours) > 0:
        contour = max(contours, key = cv.contourArea)
        (x,y),radius = cv.minEnclosingCircle(contour)
        cv.circle(Frame,(int(x),int(y)),int(radius),(0,150,0),5)

        #(x,y,w,h) = cv.boundingRect(contour) 
        #cv.rectangle(Frame,(x,y),(x+w,y+h+2),(0,0,240),2)
        #cv.rectangle(Frame,(x+w,y+h),(x,y+h+32),(0,0,240),cv.FILLED)
        #cv.putText(Frame,'Target',(x,y+h+24),cv.FONT_HERSHEY_DUPLEX,1.0,(255,255,255),1)
        #cv.putText(Frame,str((int(x+(w/2)),int(y+(h/2)))),(0,60),cv.FONT_HERSHEY_DUPLEX,1.0,(0,255,255),1)
        #cv.circle(Frame,(int(x+(w/2)),int(y+(h/2))),4,(0,150,0),5)
        
        XcFace = int(x)
        YcFace = int(y)

        OldTime = NewTime
        NewTime = millis()
        DeltaTime = NewTime - OldTime
        
        OldXError = XError
        XError = (XcFrame/smt) - (XcFace/smt)
        DeltaXError = XError - OldXError
        SlopeXError = DeltaXError / DeltaTime
        AreaXError = AreaXError + XError * DeltaTime
        PIDx = (Kp * DeltaXError) + (Kd *SlopeXError) + (Ki * AreaXError)
        XServo = Limiter(XServo + PIDx,0)

        OldYError = YError
        YError = (YcFrame/smt) - (YcFace/smt)
        DeltaYError = YError - OldYError
        SlopeYError = DeltaYError / DeltaTime
        AreaYError = AreaYError + YError * DeltaTime
        PIDy = (Kp * DeltaYError) + (Kd *SlopeYError) + (Ki * AreaYError)
        YServo = Limiter(YServo - PIDy,2)
        
        #print(YError)
        print(int(PIDx),"  ",int((Kp * DeltaXError)),"  ",int((Kd *SlopeXError)),"  ",int((Ki * AreaXError)))

    #if len(face) <= 0:
    #    XServo = 95
    #    YServo = 155

    olddata = newdata
    newdata = (XServo,YServo)
    if olddata != newdata:
        #print(newdata)
        Servos(newdata)

    cv.imshow("Frame",Frame)
    cv.imshow("Frame5",binaried)
    key = cv.waitKey(1)
    if ord("q") == key:
        cv.destroyAllWindows()
        break
