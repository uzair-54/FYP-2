from djitellopy import tello
import getKeyPress as kp
import time
import cv2

kp.init()
me = tello.Tello()
me.connect()
me.streamon()
print(me.get_battery())


def getKeyboardInput():
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
        me.land()
        # sleep(3)
    if kp.getKey("e"):
        me.takeoff()

    return [lr, fb, ud, yv]
fps = 0
pTime = time.time()
while True:

    cTime = time.time()
    if (cTime - pTime) != 0:
        fps = 1 / (cTime - pTime)
    pTime = cTime
    print(fps,"FPS")
    vals = getKeyboardInput()
    me.send_rc_control(vals[0], vals[1], vals[2], vals[3])
    time.sleep(0.05)
    img = me.get_frame_read().frame
    cv2.putText(img,"HEIGHT " + str(me.get_height()),(30, 35), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 125, 105), 2)
    cv2.putText(img,"YAW " + str(me.get_yaw()), (30, 65), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 125, 105), 1)
    cv2.putText(img, "PITCH " + str(me.get_pitch()), (30, 95), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 125, 105), 2)
    cv2.putText(img, "SPEED X " + str(me.get_speed_x()), (30, 125), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 125, 105), 2)
    cv2.imshow("Drone Cam", img)
    cv2.waitKey(1)