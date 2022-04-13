import cv2
import mediapipe as mp
import time
import helperFunctions as hf


pTime = 0

cap = cv2.VideoCapture(0)


mpFace = mp.solutions.face_detection
faceDet = mpFace.FaceDetection()

while True:

    success, img = cap.read()
    img = cv2.resize(img,(hf.width, hf.height))
    info = hf.findFace(img, faceDet)

    area = info[1]
    x = info[0][0]
    y = info[0][1]

    # print("area", area, "x", x, "y", y)
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    if x < hf.x1 and x != 0:
        print("left") # positive number will go to right

    if x > hf.x2 and x != 0:
        rl = 20
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 255), 5)
    hf.display(img)
    cv2.imshow("Output", img)
    cv2.waitKey(1)

cap.release()
cv2.destroyAllWindows()