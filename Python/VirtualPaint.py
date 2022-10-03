# Project 1, Virtual Paint
import cv2
import numpy as np

cap = cv2.VideoCapture(0)
frameWidth = 640
frameHeight = 480
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10,150)
#find color using mask thing as shown in chapter7.py
myColors = [[0,157,102,61,255,255],
           [60,102,102,111,255,255],
           [162,126,128,179,255,255]]

myColorValues = [[51,153,255],
                 [255,0,0],
                 [255,0,255]]

myPoints = []   ## [x,y,colorId]

def findColor(img,myColors,myColorValues):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0
    newPoints = []
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)
        x, y =getContours(mask)
        cv2.circle(imgResult,(x,y),10,myColorValues[count],cv2.FILLED)
        if x!=0 and y!=0:
            newPoints.append([x,y,count])
        count+=1
        # cv2.imshow(str(color[0]),mask)
    return newPoints

def getContours(img):
    contours,hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x, y, width, height = 0,0,0,0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        # print(area)
        if area>500:
            cv2.drawContours(imgResult, cnt, -1, (255,0,0), 3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
            x , y, width, height = cv2.boundingRect(approx)
    return x+width//2 , y

def drawOnCanvas(myPoints, myColorValues):
    for points in myPoints:
        cv2.circle(imgResult, (points[0],points[1]), 10, myColorValues[points[2]], cv2.FILLED)

while True:
    success, img = cap.read()
    imgResult = img.copy()
    newPoints = findColor(img, myColors,myColorValues)
    if len(newPoints)!=0:
        for newP in newPoints:
            myPoints.append(newP)
    if len(myPoints)!=0:
        drawOnCanvas(myPoints,myColorValues)
    cv2.imshow("Result", imgResult)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Thankyou for Using Virtual Paint")
        break