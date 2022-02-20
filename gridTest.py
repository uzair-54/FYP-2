import cv2
import numpy as np
import time
import helperFunctions as hf

thres = 0.58  # Threshold to detect object
nms_threshold = 0.15

classNames = hf.getFileNames()

net = hf.nnSetup()
pTime = time.time()

frameWidth = hf.width
frameHeight = hf.height

cap = cv2.VideoCapture(0)

def faceTrack(drone, info, w, pId, pError):

    area = info[1]
    x, y = info[0]
    fb = 0
    error = x - w // 2
    speed = pId[0] * error + pId[1] * (error - pError)
    speed = int(np.clip(speed, -100, 100))


    if area > hf.fbRange[0] and area < hf.fbRange[1]:
        fb = 0

    elif area > hf.fbRange[1]:
        fb = -35

    elif area < hf.fbRange[0] and area != 0:
        fb = 35

    if x == 0:
        speed = 0
        error = 0

    drone.send_rc_control(0, fb, 0, speed)
    return error


while True:

    success, img = cap.read()
    img = cv2.resize(img,(frameWidth,frameHeight))
    _, g, x, y = hf.findFace(img)

    if x < hf.x1 and x != 0:
        print("go left", time.ctime())

    if x > hf.x2 and x != 0:
        print("go right", time.ctime())

    if y < hf.y1 and y != 0:
        print("go up", time.ctime())

    if y > hf.y2 and y != 0:
        print("go down", time.ctime())

    hf.display(img)
    cv2.imshow("Output", img)
    cv2.waitKey(1)

cap.release()
cv2.destroyAllWindows()