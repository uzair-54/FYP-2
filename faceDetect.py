import cv2
import numpy as np

cap = cv2.VideoCapture(0)

def findFace(img):
    faceCascade = cv2.CascadeClassifier("additional Files//haarcascade_frontalface_default.xml")
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(imgGray,1.2,8)

    myFaceC = []
    myFaceArea = []

    for(x,y,w,h) in faces:
        cv2.rectangle(img,(x, y),(x + w, y + h),(0,255,0),cv2.FILLED)
        cx = x + w //2
        cy = y + h //2
        area = w * h
        cv2.circle(img,(cx, cy), 5, (0,0,255),cv2.FILLED)

        myFaceC.append([cx,cy])
        myFaceArea.append(area)

    if len(myFaceC) != 0:
        i = myFaceArea.index(max(myFaceArea))
        return img, [myFaceC[i],myFaceArea[i]]
    else:
        return img, [[0, 0], 0]
while True:
    _,img = cap.read()

    img, info = findFace()
    cv2.imshow("test",img)
    cv2.waitKey(1)