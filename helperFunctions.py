import cv2
import getKeyPress as kp

####################################
####### CONSTANT VARIABLES #########
####################################

width, height = 720, 480#360, 240#800, 600
deadZone = 100

x1 = int(width / 2) - deadZone
x2 = int(width / 2) + deadZone
y1 = int(height / 2) - deadZone
y2 = int(height / 2) + deadZone

fbRange = [15000, 53500]#[60000, 85000]
pId = [0.4, 0.4, 0]
pError = 0

####################################
########### FUNCTIONS ##############
####################################

def putDataOnFrame(img, drone):
    cv2.putText(img, "BATTERY " + str(drone.get_battery()), (30, 125), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 125, 105), 2)
    return img

def display(img):
    cv2.line(img, (x1, 0), (x1, height), (255, 255, 125), 3)
    cv2.line(img, (x2, 0), (x2, height), (255, 55, 0), 3)

    cv2.line(img, (0, y1), (width, y1), (255, 25, 0), 3)
    cv2.line(img, (0, y2), (width, y2), (255, 200, 0), 3)

    return img

def getFileNames():
    classFile = 'additional Files//coco.names'
    with open(classFile, 'rt') as f:
        classNames = f.read().rstrip('\n').split('\n')
    return classNames

def nnSetup():
    configPath = 'additional Files//ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
    weightsPath = 'additional Files//frozen_inference_graph.pb'

    net = cv2.dnn_DetectionModel(weightsPath, configPath)
    net.setInputSize(320, 320)
    net.setInputScale(0.5 / 127.5)
    net.setInputMean((127.5, 127.5, 127.5))
    net.setInputSwapRB(True)

    return net

def findFace(img, faceDetector):

    ih, iw, ic = img.shape
    RGBimg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = faceDetector.process(RGBimg)

    if results.detections:
        # for detection in results.detections:
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

def getKeyboardInput(drone):
    flag = False

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