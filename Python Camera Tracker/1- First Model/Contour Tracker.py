import numpy as np
import cv2 as cv

def map( x, in_min,in_max, out_min, out_max):
    maps = -((x - in_max)*(out_max-out_min)/(in_max-in_min)+out_min)
    return maps
def nothing(x):
    pass    

webcam = cv.VideoCapture(0)
minf = np.array([20,169,63])
maxf = np.array([71,255,182])

################################################
while True:
    _,frame = webcam.read()
    mrkzy = int(len(frame)/2)
    mrkzx = int(len(frame[0])/2)
    
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    hsvblured = cv.GaussianBlur(hsv, (5, 5), 0)
    binary = cv.inRange(hsvblured, minf, maxf)
    medianed = cv.medianBlur(binary, 25)
    filtered = cv.bitwise_and(frame,frame, mask= medianed)
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
            
    except Exception as excerr:
        print(excerr)
################################################
    cv.imshow("frame", frame)
    #print(center)
################################################
    ikey = cv.waitKey(5)
    if (ikey==ord("q")):
        cv.destroyAllWindows()
        break
