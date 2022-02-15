import cv2

def getFileNames():
    classFile = 'additional Files//coco.names'
    with open(classFile, 'rt') as f:
        classNames = f.read().rstrip('\n').split('\n')
    return classNames

def nnSetup():
    configPath = 'additional Files//ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
    weightsPath = 'additional Files//frozen_inference_graph.pb'

    net = cv2.dnn_DetectionModel(weightsPath, configPath)

    return net

Known_distance = 76.2
knownWidth = 14.3
def focalLengthFinder(measured_distance, real_width, width_in_rf_image):
    focal_length = (width_in_rf_image * measured_distance) / real_width
    return focal_length


def distanceFinder(Focal_Length, real_face_width, face_width_in_frame):
    distance = (real_face_width * Focal_Length) / face_width_in_frame
    return distance

face_detector = cv2.CascadeClassifier("additional Files//haarcascade_frontalface_default.xml")

def faceData(image):
    face_width = 0

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faces = face_detector.detectMultiScale(gray_image, 1.3, 5)

    for (x, y, h, w) in faces:
        face_width = w

    return face_width

ref_image = cv2.imread("pics//bb.jpg")

ref_image_face_width = faceData(ref_image)

focallengthFound = focalLengthFinder(Known_distance, knownWidth, ref_image_face_width)
