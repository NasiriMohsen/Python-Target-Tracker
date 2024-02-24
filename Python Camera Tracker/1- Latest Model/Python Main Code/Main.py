import serial
import time 
import cv2 as cv
import time

#Servo Home Values. Set yours based on your desigred position.
ServoValueX = 50 
ServoValueY = 150

#PID Control values. Modify at your own risk!
Kp = 0.02
Ki = 0.0000001
Kd = 0.03


#Connect or Pair to the ESP before running the code and use its "Port" below
Bluetooth = serial.Serial('COM6', 115200)
#You may use diffrent Cascades based on your needs. I have provide more "Face" Cascades in this folder!
Cascade = cv.CascadeClassifier("./frontalface_alt.xml")

def Servos(LastTime, XServo, YServo):
    XServo = int(XServo)
    YServo = int(YServo)
    if XServo >= 180:
        XServo = 180
    elif XServo <= 0:
        XServo = 0
    if YServo >= 180:
        YServo = 180
    elif YServo <= 0:
        YServo = 0        
    Data = str(XServo) + "," + str(YServo)
    while (time.time() - LastTime) <= 0.002:
        pass    
    Bluetooth.write(Data.encode('utf-8'))
    return time.time()

def PIDCalculator(CurrentTimeMilliS, PreviousTime, Error, PastError, PastErrorFine, Kp, Ki, Kd):
    ElapesedTime = CurrentTimeMilliS - PreviousTime             
    ErrorRate = (Error - PastError) / ElapesedTime   #Derivative
    ErrorFine = PastErrorFine + (Error * ElapesedTime) #Integral
    PIDValue = (Kp * Error) + (Ki * ErrorFine) + (Kd * ErrorRate)
    return PIDValue,ErrorFine

#Change the number below if u have multiple Webcams. 0 is the main Webcam!
Webcam = cv.VideoCapture(1)
Frame = Webcam.read()[1]
YMidFrame = int(len(Frame) / 2)
XMidFrame = int(len(Frame[0]) / 2)
StartTime = time.time()

BluetoothPastTime = 0
PreviousTime = 0
PreviousErrorX = 0
PreviousErrorY = 0
PreviousErrorFineX = 0
PreviousErrorFineY = 0

BluetoothPastTime = Servos(BluetoothPastTime,ServoValueX,ServoValueY)
while True:
    Frame = Webcam.read()[1]
    GrayFrame = cv.cvtColor(Frame, cv.COLOR_BGR2GRAY) 
    Target = Cascade.detectMultiScale(GrayFrame, 1.1, 8)    
    for (XPoint, YPoint, Width, Height) in Target:
        cv.rectangle(Frame, (XPoint, YPoint), (XPoint + Width, YPoint + Height), (0, 255, 0), 2)
#############################################
        CurrentTimeMilliS = int(round((time.time() - StartTime) * 1000))
        ErrorX = XMidFrame - int(XPoint + (Width / 2))
        ErrorY = YMidFrame - int(YPoint + (Height / 2))
        XPIDValue,PreviousErrorFineX = PIDCalculator(CurrentTimeMilliS, PreviousTime, ErrorX, PreviousErrorX, PreviousErrorFineX, Kp, Ki, Kd)        
        YPIDValue,PreviousErrorFineY = PIDCalculator(CurrentTimeMilliS, PreviousTime, ErrorY, PreviousErrorY, PreviousErrorFineY, Kp, Ki, Kd)
        PreviousErrorX = ErrorX
        PreviousErrorY = ErrorY 
        PreviousTime = CurrentTimeMilliS
#############################################
        if (int(ServoValueX + XPIDValue) != ServoValueX) or (int(ServoValueY - YPIDValue) != ServoValueY):
            ServoValueX = ServoValueX + XPIDValue
            ServoValueY = ServoValueY - YPIDValue
            BluetoothPastTime = Servos(BluetoothPastTime,ServoValueX,ServoValueY)
#############################################
    cv.imshow("Window",Frame)
    if ord("q") == cv.waitKey(1):
        cv.destroyAllWindows()
        break

