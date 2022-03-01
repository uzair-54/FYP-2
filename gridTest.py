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
    info = hf.findFace(img, faceDet)

    area = info[1]
    x = info[0][0]
    y = info[0][1]

    print("area", area, "x", x, "y", y)
    cTime = time.time()
    fps = 1 / (cTime - pTime)

    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 255), 5)

    cv2.imshow("Output", img)
    cv2.waitKey(1)

cap.release()
cv2.destroyAllWindows()