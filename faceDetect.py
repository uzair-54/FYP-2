import time

import cv2
import numpy as np
from djitellopy import tello
w, h = 800, 600 #360, 240 #800, 600

fbRange = [6200, 6800]
pId = [0.4, 0.4, 0]
pError = 0
# drone = tello.Tello()
# drone.connect()
# drone.streamon()
# drone.takeoff()
# drone.send_rc_control(0,0,25,0)
# time.sleep(2.2)
cap = cv2.VideoCapture(0)


def findFace(img):
    faceCascade = cv2.CascadeClassifier("additional Files//haarcascade_frontalface_default.xml")
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(imgGray,1.2,8)

    myFaceC = []
    myFaceArea = []

    for(x,y,w,h) in faces:
        cv2.rectangle(img,(x, y),(x + w, y + h),(0,255,0),3)
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

def faceTrack(drone, info, w, pId, pError):

    area = info[1]
    x, y = info[0]
    fb = 0
    error = x - w // 2
    speed = pId[0] * error + pId[1] * (error - pError)
    speed = int(np.clip(speed, -100, 100))


    if area > fbRange[0] and area < fbRange[1]:
        fb = 0

    elif area > fbRange[1]:
        fb = -35

    elif area < fbRange[0] and area != 0:
        fb = 35
    print(fb,error)
    if x == 0:
        speed = 0
        error = 0

    # drone.send_rc_control(0, fb, 0, speed)
    return error

while True:

    _, img = cap.read()
    # img = drone.get_frame_read().frame
    img = cv2.resize(img,(w, h))
    img, info = findFace(img)
    pError = faceTrack("drone", info, w, pId, pError)
    cv2.imshow("test",img)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        # drone.land()
        break