# from deepface import DeepFace
# import cv2
#
# cap = cv2.VideoCapture(0)
#
# while True:
#
#     _,img = cap.read()
#     result = DeepFace.verify(img1_path=img, img2_path="pics//bb.jpg")
#     print(result['verified'])
#     cv2.imshow("output",img)
#     cv2.waitKey(1)
#
# # result = DeepFace.verify(img1_path = "pics//bb.jpg", img2_path = "pics//bb.jpg")
# #
# # print(result['verified'])

1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
from mtcnn import MTCNN
import cv2

detector = MTCNN()
# Load a videopip TensorFlow
video_capture = cv2.VideoCapture(0)

while (True):
    ret, frame = video_capture.read()
    frame = cv2.resize(frame, (600, 400))
    boxes = detector.detect_faces(frame)
    if boxes:

        box = boxes[0]['box']
        conf = boxes[0]['confidence']
        x, y, w, h = box[0], box[1], box[2], box[3]

        if conf > 0.5:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 1)

    cv2.imshow("Frame", frame)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()