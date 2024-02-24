#Code To send 2 Servo Positions To NodeMcu ESP32 Using built in Bluetooth
import serial
import time 

#Connect or Pair to the ESP before running the code and use its "Port" below
Bluetooth = serial.Serial('COM6', 115200)

def Servos(PreviousTime,XServo,YServo):
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
    while (time.time() - PreviousTime) <= 0.002:
        pass    
    Bluetooth.write(Data.encode('utf-8'))
    return time.time()



PastTime = time.time()

while True:
    print("Enter Two number from the range 0 - 180 and seperate them with a Comma in between. eg: 180,90")
    Data = input("Numbers: ")
    Bluetooth.write(Data.encode('utf-8'))


