import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)
pTime = 0

mpFace = mp.solutions.face_detection
faceDet = mpFace.FaceDetection()


def findFace(img, faceDetector):
    ih, iw, ic = img.shape
    RGBimg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = faceDetector.process(RGBimg)

    if results.detections:

        x = int(results.detections[0].location_data.relative_bounding_box.xmin * iw)
        y = int(results.detections[0].location_data.relative_bounding_box.ymin * ih)
        w = int(results.detections[0].location_data.relative_bounding_box.width * iw)
        h = int(results.detections[0].location_data.relative_bounding_box.height * ih)

        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)

        cx = x + w // 2
        cy = y + h // 2
        area = w * h
        cv2.circle(img, (cx, cy), 5, (0, 0, 255), cv2.FILLED)

        return [[x, y], area]
    else:
        return [[0, 0], 0]


while True:
    _, img = cap.read()
    findFace(img, faceDet)

    cTime = time.time()
    fps = 1 / (cTime - pTime)

    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 255), 5)
    cv2.imshow("img", img)
    cv2.waitKey(1)
