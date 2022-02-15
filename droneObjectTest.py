import cv2
from djitellopy import tello
import time
import numpy as np
import helperFunctions as hf

thres = 0.58  # Threshold to detect object
nms_threshold = 0.15
drone = tello.Tello()
drone.connect()

drone.streamon()

classNames = hf.getFileNames()

net = hf.nnSetup()
net.setInputSize(320, 320)
net.setInputScale(0.5 / 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

pTime = time.time()

while True:
    img = drone.get_frame_read().frame
    classIds, confs, bbox = net.detect(img, confThreshold=thres)
    bbox = list(bbox)
    confs = list(np.array(confs).reshape(1, -1)[0])
    confs = list(map(float, confs))
    indices = cv2.dnn.NMSBoxes(bbox, confs, thres, nms_threshold)

    cTime = time.time()

    fps = 1 / (cTime - pTime)
    pTime = cTime
    print(fps,"FPS")
    # print(confs)
    for i in indices:

        box = bbox[int(i)]
        x, y, w, h = box[0], box[1], box[2], box[3]
        cenerCords = x + w // 2, y + h // 2
        if classNames[classIds[int(i)] - 1] == "person":
            cv2.rectangle(img, (x, y), (x + w, h + y), (0, 128, 0), 5)
            cv2.circle(img, cenerCords, 15, (0, 0, 255), -1)
        else:
            cv2.rectangle(img, (x, y), (x + w, h + y), (255, 0, 0), 5)
            cv2.circle(img, cenerCords, 15, (0, 0, 255), -1)
            cv2.putText(img, classNames[classIds[int(i)] - 1].upper(), (box[0] + 10, box[1] + 30),
                        cv2.FONT_HERSHEY_COMPLEX, 2, (0, 255, 0), 2)
    if len(indices) != 0 and classNames[classIds[int(i)] - 1] != "person":
        pass
    else:
        pass

    cv2.putText(img, "HEIGHT str(me.get_height())", (30, 35), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 125, 105), 1)
    cv2.putText(img, "YAW str(me.get_yaw()) ", (30, 65), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 125, 105), 1)

    cv2.imshow("Output", img)
    cv2.waitKey(1)