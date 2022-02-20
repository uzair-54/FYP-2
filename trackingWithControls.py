import cv2
from djitellopy import tello
import time
import numpy as np
import getKeyPress as kp
import helperFunctions as hf

frameWidth, frameHeight = hf.width, hf.height

fbRange = [60000, 85000]
pId = [0.4, 0.4, 0]
pError = 0

cap = cv2.VideoCapture(0)

drone = tello.Tello()
drone.connect()
kp.init()
drone.streamon()

# pTime = time.time()

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

    if x == 0:
        speed = 0
        error = 0

    drone.send_rc_control(0, fb, 0, speed)
    return error

while True:

    img = drone.get_frame_read().frame
    vals, flag = hf.getKeyboardInput(drone)
    img = cv2.resize(img, (frameWidth, frameHeight))
    img, info, x, y = hf.findFace(img)
    # print(info, "INFO")

    # print(vals, flag)
    if flag:
        # img = cv2.resize(img, (w, h))
        # img, info = findFace(img)
        pError = faceTrack(drone, info, frameWidth, pId, pError)
        print(2)

    else:
        drone.send_rc_control(vals[0], vals[1], vals[2], vals[3])
        time.sleep(0.05)
        print(1)

    img = hf.putDataOnFrame()
    cv2.imshow("Drone Cam", img)
    cv2.waitKey(1)