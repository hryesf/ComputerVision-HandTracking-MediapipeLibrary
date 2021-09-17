import math

import cv2
import time
import numpy as np
import HandTrackingModule as htm

#############################################
wCam, hCam = 640, 480  #width of camera and height of camera
#############################################

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

detector = htm.hanndDetector(detectionCon=0.7)


while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img)

    if len(lmList) != 0:
        # print(lmList[4], lmList[8])
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        # cx, cy = x1+x2//2, y1+y2//2 #circle in between

        cv2.circle(img, (x1, y1), 7, (255, 0, 0), cv2.FILLED)
        cv2.circle(img, (x2, y2), 7, (255, 0, 0), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 3)
        # cv2.circle(img, (cx, cy), 7, (255, 0, 0), cv2.FILLED) #circle in between

        #for valume
        length = math.hypot(x2-x1, y2-y1)
        print(length)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, f'FPS:{int(fps)}', (40, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)


    cv2.imshow("Image", img)
    cv2.waitKey(1)