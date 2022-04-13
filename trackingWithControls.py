import cv2
from djitellopy import tello
import time
import mediapipe as mp
import getKeyPress as kp
import helperFunctions as hf

flag = False
frameWidth, frameHeight = hf.width, hf.height

fbRange = [15000, 53500]


mpFace = mp.solutions.face_detection
faceDet = mpFace.FaceDetection(min_detection_confidence=0.7)
cap = cv2.VideoCapture(0)

drone = tello.Tello()
drone.connect()
kp.init()
drone.streamon()

pTime = 0

def faceTrackUserDefined(drone, info):

    fb = 0
    rl = 0
    ud = 0

    area = info[1]
    x = info[0][0]
    y = info[0][1]

    if hf.fbRange[0] < area < hf.fbRange[1]:
        fb = 0

    if area > hf.fbRange[1]:
        fb = -45

    if area < hf.fbRange[0] and area != 0:
        fb = 20

    if x < hf.x1 and x != 0:
        rl = -30 # positive number will go to right

    if x > hf.x2 and x != 0:
        rl = 30

    if y < hf.y1 and y != 0:
        ud = -20

    if y > hf.y2 and y != 0:
        ud = 20

    drone.send_rc_control(0, fb, 0, 0)
    # drone.send_rc_control(rl, 0, 0, 0)

    return rl

def getKeyboardInput(drone):
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
    vals, flag = getKeyboardInput(drone)
    img = cv2.resize(img, (frameWidth, frameHeight))
    info = hf.findFace(img, faceDet)
    # print(info[1])
    # print(info, "INFO")

    # print(vals, flag)
    if flag:

        speed = faceTrackUserDefined(drone, info)
        time.sleep(0.05)

        if speed > 0:
            cv2.putText(img, "RIGHT", (hf.width // 2, 40), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 255), 2)

        else:
            cv2.putText(img, "LEFT", (hf.width // 2, 40), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 255), 2)

        print(2)

    else:
        drone.send_rc_control(vals[0], vals[1], vals[2], vals[3])
        time.sleep(0.05)
        print(1)
    cTime = time.time()
    fps = 1 / (cTime - pTime)

    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 255), 5)
    img = hf.putDataOnFrame(img, drone)
    cv2.imshow("Drone Cam", img)
    cv2.waitKey(1)