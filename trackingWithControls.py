import cv2
from djitellopy import tello
import time

import numpy as np
import getKeyPress as kp
import helperFunctions as hf

w, h = 800, 600

fbRange = [6200, 6800]
pId = [0.4, 0.4, 0]
pError = 0
flag = False
cap = cv2.VideoCapture(0)

drone = tello.Tello()
drone.connect()
kp.init()
drone.streamon()

# pTime = time.time()

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
    # print(fb,error)
    if x == 0:
        speed = 0
        error = 0

    drone.send_rc_control(0, fb, 0, speed)
    return error



def getKeyboardInput():
    global flag

    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 75

    if kp.getKey("LEFT"):
        lr = -speed

    elif kp.getKey("RIGHT"):
        lr = speed

    if kp.getKey("UP"):
        fb = speed

    elif kp.getKey("DOWN"):
        fb = -speed

    if kp.getKey("w"):
        ud = speed

    elif kp.getKey("s"):
        ud = -speed

    if kp.getKey("a"):
        yv = -speed

    elif kp.getKey("d"):
        yv = speed

    if kp.getKey("q"):
        drone.land()
        # pass
        # sleep(3)

    if kp.getKey("e"):
        drone.takeoff()
        # pass

    if kp.getKey("SPACE"):
        flag = True

    if kp.getKey("n"):
        flag = False

    return [lr, fb, ud, yv], flag

while True:

    img = drone.get_frame_read().frame
    vals, flag = getKeyboardInput()

    # print(vals, flag)
    if flag:
        img = cv2.resize(img, (w, h))
        img, info = findFace(img)
        pError = faceTrack(drone, info, w, pId, pError)
        print(2)

    else:
        drone.send_rc_control(vals[0], vals[1], vals[2], vals[3])
        time.sleep(0.05)
        print(1)

    cv2.putText(img, "HEIGHT " + str(drone.get_height()), (30, 35), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 125, 105), 2)
    cv2.putText(img, "YAW " + str(drone.get_yaw()), (30, 65), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 125, 105), 1)
    cv2.putText(img, "PITCH " + str(drone.get_pitch()), (30, 95), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 125, 105), 2)
    cv2.putText(img, "SPEED X " + str(drone.get_speed_x()), (30, 125), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 125, 105), 2)
    cv2.imshow("Drone Cam", img)
    if cv2.waitKey(1) & 0xFF == ord("z"):
        break