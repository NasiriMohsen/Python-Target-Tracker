import Streamclass2 as SC
import cv2 as cv
import time

def pid(currtime,previousTime,err,lasterr,Kp,Kd):
    etime = currtime-previousTime               
    rateError = (err-lasterr)/etime   
    pid = (Kp*err)+(Kd*rateError)
    return pid

targetcas = cv.CascadeClassifier("C:/Users/Asus/Desktop/Code/Python-Opencv-clean-codes-master/Haarcascade/haarcascade_frontalface_alt.xml")

previousTime = 0
lasterrx = 0
lasterry = 0
Kp = 0.01
Kd = 0.03
servxp = 90
servyp = 120
stime = time.time()

cv.namedWindow('frame',cv.WINDOW_FREERATIO)

server = SC.Socket()
server.Server(IP='192.168.1.8')

while True:
    frame = server.ServerRStream()
    gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY) 
    target = targetcas.detectMultiScale(gray,1.1,8)    
    for (x,y,w,h) in target:
        targx = int(x+w/2)
        targy = int(y+h/2)
        cv.rectangle(frame,(x,y),(x+w,y+h),(255,255,0),2)
#############################################
        currtime = int(round((time.time()-stime)*1000))
        errx = int((len(frame[0])/2)-targx)
        erry = int((len(frame)/2)-targy)
        pidx = pid(currtime,previousTime,errx,lasterrx,Kp,Kd)
        pidy = pid(currtime,previousTime,erry,lasterry,Kp,Kd)
        print(int(pidx*100)/100,int(pidy*100)/100)
        lasterrx = errx
        lasterry = erry 
        previousTime = currtime
#############################################
        servxp = servxp + pidx
        servyp = servyp - pidy
        int(pidy*100)/100
        
    servxp = int(servxp*100)/100
    servyp = int(servyp*100)/100
    msg = str(servxp)+'-'+str(servyp)
    server.Serversend(msg=msg)
#############################################
    cv.imshow("frame",frame)
    if ord("q") == cv.waitKey(1):
    	cv.destroyAllWindows()
    	break



    