"""
    Detect hands using cv2 & mediapipe library
    Draw lines to connect the landmarks of the detected hands
"""
import cv2
import mediapipe as mp
import math


class handDetector():
    def __init__(self, mode=False, maxHands=2, detectConfidence=0.75, trackConfidence=0.75):
        self.mode = mode
        self.maxHands = maxHands
        self.detectConfidence = detectConfidence
        self.trackConfidence = trackConfidence
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands()
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]
        # self.LmarkList = []

    def findHands(self, frame, draw=True):
        # convert img from BGR to RGB for hands object to process
        rgbImg = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.result = self.hands.process(rgbImg)
        if self.result.multi_hand_landmarks:
            for handLmarks in self.result.multi_hand_landmarks:
                if draw:
                    # draw landmarks & connections for them
                    self.mpDraw.draw_landmarks(
                        frame, handLmarks, self.mpHands.HAND_CONNECTIONS)
        return frame

    def findPosition(self, frame, handNo=0, draw=True):
        self.LmarkList = []
        # xList = []
        # yList = []
        # bBox = []
        # LmarkList = []
        # rgbImg = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # self.result = self.hands.process(rgbImg)

        if self.result.multi_hand_landmarks:
            # processed landmarks from Hands() method for 1 hand
            myHand = self.result.multi_hand_landmarks[handNo]
            # get land mark ids
            for LmarkId, lmk in enumerate(myHand.landmark):
                h, w, c = frame.shape  # get o/p window dimension
                # coordinates for landmarks of detected hands
                cx, cy = int(lmk.x * w), int(lmk.y * h)
                # xList.append(cx)
                # yList.append(cy)
                # print(LmarkId, cx, cy)  # print id & coord. of landmarks on console
                # LmarkList.append([LmarkId, cx, cy])
                self.LmarkList.append([LmarkId, cx, cy])

                if draw:
                    if LmarkId in [4, 8, 12, 16, 20]:  # id of thumb tip
                        # draw circle for thumb tip
                        cv2.circle(frame, (cx, cy), 9,
                                   (84, 245, 66), cv2.FILLED)
            # xMin, xMax = min(xList), max(xList)
            # yMin, yMax = min(yList), max(yList)
            # bBox = xMin, yMax, xMax, yMax

        return self.LmarkList


    def upFingers(self):
        fingers = []
        # thumb open or closed
        if self.LmarkList[self.tipIds[0]][1] < self.LmarkList[self.tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # other fingers
        for id in range(1, 5):
            if self.LmarkList[self.tipIds[id]][2] < self.LmarkList[self.tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers


    def findDistance(self, f1, f2, frame, draw=True):
        x1, y1 = self.LmarkList[f1][1:]
        x2, y2 = self.LmarkList[f1][1:]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        if draw:
            cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 255), 3)
            cv2.circle(frame, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            cv2.circle(frame, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
            cv2.circle(frame, (cx, cy), 15, (0, 0, 255), cv2.FILLED)
        length = math.hypot(x2 - x1, y2 - y1)
        
        return length, frame, [x1, y1, x2, y2, cx, cy]


def main():
    video = cv2.VideoCapture(0)  # open camera to capture image frame
    detect = handDetector()
    # make o/p window of free dimension
    cv2.namedWindow('=== Live Cam ===', cv2.WINDOW_NORMAL)

    while True:
        check, frame = video.read()  # check & capture the frame
        # flip the frame for a mirror image like o/p
        frame = cv2.flip(frame, 1)
        frame = detect.findHands(frame)
        # get hand landmarks and store in a list
        LmarkList = detect.findPosition(frame)

        cv2.putText(frame, "Press 'Q' to exit", (25, 450), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (255, 255, 0), 2)  # display quit key on o/p window
        # open window for showing the o/p
        cv2.imshow('=== Live Cam ===', frame)

        # escape key (q)
        if cv2.waitKey(1) == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
