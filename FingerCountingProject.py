import cv2
import time
import HandTrackingModule as htm

wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

pTime = 0

detecror = htm.hanndDetector(detectionCon=0.75)

tipIds = [4, 8, 12, 16, 20]

while True:
    success, img = cap.read()
    img = detecror.findHands(img)
    lmList = detecror.findPosition(img)
    # print(lmList)

    if len(lmList) != 0:
        fingers = []
        # thumb
        if lmList[tipIds[0]][1] < lmList[tipIds[0]-1][1]:
            fingers.append(0)
        else:
            fingers.append(1)
        # 4 fingers
        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                fingers.append(1) # when finger open
            else:
                fingers.append(0) # when finger open
        # print(fingers)

        totalFingers = sum(fingers)
        print(totalFingers)

        dic = {0:"Zero", 1:"One", 2:"Two", 3:"Three", 4:"Four", 5:"Five"}
        # dic_farsi = {0: "صفر", 1: "یک", 2: "دو", 3: "سه", 4: "چهار", 5: "پنج"}
        cv2.rectangle(img, (20, 255), (170, 425), (0, 255, 255), cv2.FILLED)
        cv2.putText(img, str(totalFingers), (45, 400), cv2.FONT_HERSHEY_PLAIN, 10, (0, 0, 255), 25)

        cv2.putText(img, f'{str(dic[totalFingers])}', (25, 120), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {str(int(fps))}', (10, 70), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)



    cv2.imshow("Image", img)
    cv2.waitKey(1)
