import cv2
import numpy as np
import time
import handDetectionModule as htm
import pyautogui



video = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# setting the captured video's dimensions
wCam, hCam = 640, 480
frameR = 100  #Frame Reduction
smoothening = 5
pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0


video.set(3, wCam)
video.set(4, hCam)
detector = htm.handDetector(maxHands=1)
wScr, hScr = pyautogui.size()


while True:

    #Find Ladmarks
    success, img = video.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    lmList = detector.findPosition(img)

    #Get the tip of the index and middle finger
    if len(lmList)!=0:
        x1,y1 = lmList[8][1:]
        x2,y2 = lmList[12][1:]

        #Check which fingers are up
        fingers = detector.upFingers()
        cv2.rectangle(img, (frameR, frameR),(wCam-frameR, hCam -frameR), (255, 0, 255), 2)
           

        #Moving mode only if index finger is up
        if fingers[1]==1 and fingers[2]==0:

            #Convert Coordinates
            x3 = np.interp(x1, (frameR, wCam - frameR),(0, wScr))
            y3 = np.interp(y1, (frameR, hCam - frameR),(0, hScr))

            #Smoothen coordinate values
            clocX = plocX +(x3 -plocX) / smoothening
            clocY = plocY +(y3 -plocY) / smoothening

            #Move Mouse
            pyautogui.moveTo(clocX, clocY)
            cv2.circle(img, (x1,y1),15,(255,0,255),cv2.FILLED)
            plocX , plocY = clocX, clocY

        #Clicking mode, if both index and middle finger are up
        if fingers[1]==1 and fingers[2]==1:
            #Find distancee between fingers
            length, img, lineInfo = detector.findDistance(8, 12, img)
            # mouse click condition (threshold)
            if length < 35:
                # [x1, y1, x2, y2, cx, cy]
                # cv2.line(frame, (lineInfo[0], lineInfo[1]), (lineInfo[2], lineInfo[3]), (255, 0, 255), 3)
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                pyautogui.click()

    

    #Display
    cv2.imshow('Image', img)
    cv2.waitKey(1)