import cv2
import time
import os
import numpy as np
import HandTrackingModule as htm

brushThickness = 15
eraserThickness = 50

folderPath = 'Header'
myList = os.listdir(folderPath)
myList.sort()
print(myList)
overlayList =[]
for imPath in myList:
    image  = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)
# print(len(overlayList))
header = overlayList[0]
drawColor = (255, 0, 0)

cap = cv2.VideoCapture(0)
cap.set(3, 1280) #width
cap.set(4, 720)  #height

detector = htm.hanndDetector(detectionCon=0.85)

xp, yp = 0,0    # x previous and y previous
imgCanvas = np.zeros((720, 1280, 3), np.uint8)

while True:
    # 1. Import image
    success, img = cap.read()
    img  = cv2.flip(img, 1)
    # 2. Find hand Landmarks
    img = detector.findHands(img)
    lmList = detector.findPosition(img)
    if len(lmList) != 0:
        # print(lmList)

        # tip of index middle fingers
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        # 3. check which fingers are up
        fingers = detector.fingersUp()
        # print(fingers)
        # 4. If selection mode - Two fingers are up
        if fingers[1] and fingers[2]:
            print("Selection mode")
            xp, yp = x1, y1 # I fix this Bug : continue drawing after selection mode with previous state in drawing mode
            # checking for the click
            if y1 < 125 :
                if 220< x1 <350:
                    header = overlayList[0]
                    drawColor = (0, 255, 0)  # green
                elif 390< x1 <525:
                    header = overlayList[1]
                    drawColor = (0, 0, 255)  # red
                elif 558< x1 <698:
                    header = overlayList[2]
                    drawColor = (255, 0, 0)  # blue
                elif 730< x1 <865:
                    header = overlayList[3]
                    drawColor = (255, 255, 255) # white
                elif 940< x1 <1050:
                    header = overlayList[3]
                    drawColor = (0, 0, 0) # black= eraser

            cv2.rectangle(img, (x1, y1 - 20), (x2, y2 + 20), drawColor, cv2.FILLED)

        # 5. I f Drawing mode  - Index finger os up
        if fingers[1] and fingers[2] == False:
            cv2.circle(img, (x1, y1), 10, drawColor, cv2.FILLED)
            print("Drawing mode")
            if xp == 0 and yp == 0:
                xp, yp = x1, y1
            if drawColor == (0, 0, 0):
                cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)  # draw lines in screen
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)  # draw lines in screen
            else:
                cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness) # draw lines in screen
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness) # draw lines in screen
            xp, yp = x1, y1

        # imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
        # _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
        # imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
        # img = cv2.bitwise_and(img, imgInv)
        # img = cv2.bitwise_or(img, imgCanvas)


    # setting the header image
    img[0:125, 0:1280] = header
    # img = cv2.addWeighted(img, 0.5, imgCanvas, 0.5, 0)
    cv2.imshow("Image", img)
    # cv2.imshow("Canvas", imgCanvas)
    cv2.waitKey(1)