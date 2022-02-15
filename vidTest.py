import cv2
from djitellopy import tello
import time
drone = tello.Tello()
drone.connect()

drone.streamon()

pTime = time.time()

while True:

    # print(drone.get_battery())
    img = drone.get_frame_read().frame
    cTime = time.time()

    fps = 1 / (cTime - pTime)
    pTime = cTime
    print(fps,"FPS")
    cv2.imshow("Drone Cam", img)
    cv2.waitKey(1)