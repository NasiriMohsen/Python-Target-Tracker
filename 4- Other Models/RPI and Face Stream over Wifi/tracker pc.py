import numpy as np
import cv2 as cv

#video capture device
webcam = cv.VideoCapture(0)
cv.namedWindow('frame',cv.WINDOW_FREERATIO)
#making a loop
while True:
    
#capturing every frame and turning it into np.array
    _,frame = webcam.read()

# finding the center of all frames
    mrkzy = int(len(frame)/2)
    mrkzx = int(len(frame[0])/2)

# bgr to hsv
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

# array of the color to filter
    minf = np.array([170,55,65])
    maxf = np.array([255,255,255])

# filtering and mixing ...
    binary = cv.inRange(hsv, minf, maxf)

# removing binarry errores 
    medianed = cv.medianBlur(binary, 25) 

# filtering color on frame and into filtered 

    filterd = cv.bitwise_and(frame,frame, mask= medianed)

# finding contours of binary and asigning them to contours variable and im2 is litrarly medianed and hierarchy is for when its found
    im2, contours, hierarchy = cv.findContours(medianed,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)  

# drawing circles around contoures and getting cordinants
    try:  
   #the if XD
        if len(contours) > 0:
            
    #chosing the bigest contour   
            #cnt is the bigest contour wich is going to be the thing we are looking for :)
            cnt = max(contours, key = cv.contourArea)

    #center and radius    
            #the center of the contour we found by using a circle and asigning it in to x1,y1 and getting the radius that it was found by
            (x1,y1), radius=cv.minEnclosingCircle(cnt)

    #seprating the coordinates and mixing them
            cntx = int(x1)
            cnty = int(y1)
            center = (int(x1),int(y1))
            radius = int(radius)

    #drawing circle and rectangle to specigy the contour
            #getting the cordinants needed to make a rectangle over the contour
            x,y,w,h = cv.boundingRect(cnt)

            #green rectangel to show the boundry or smt
            cv.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

            #red circle to show the boundry
            cv.circle(frame,center,radius,(0,0,255),2)

            #blue circle(dot) to show the center
            cv.circle(frame,center,2,(255,0,0),4) 

    #the if's that tell us wher to look 
        if(mrkzy > cnty):
            print("kaley robot be samt (bala) nega kon")
        elif(mrkzy < cnty):
            print("kaley robot be samt (paen) nega kon")
        if(mrkzx > cntx):
            print("kaley robot be samt (chap) nega kon")
        elif(mrkzx < cntx):
            print("kaley robot be samt (rast) nega kon")
    except:
        print("nthin found")

# displaying stuff    
    cv.imshow('frame',frame)
    #cv.imshow('medianed',im2)
    #cv.imshow('filtered',filterd)
    #cv.imshow('somelse',madian)

# interupt key and closing
    a = cv.waitKey(1)
    if (a==ord("q")):
        cv.destroyAllWindows()
        break
