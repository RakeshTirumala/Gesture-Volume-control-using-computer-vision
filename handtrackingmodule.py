import cv2 as cv
import mediapipe as mp
import time

class handDetector:
    def __init__(self, mode= False, maxhands = 2, detectioncon = 0.5, trackcon = 0.5):
        self.mode = mode
        self.maxhands = maxhands
        self.detectioncon = detectioncon
        self.trackcon = trackcon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode,self.maxhands,self.detectioncon, self.trackcon)
        self.mpdraw = mp.solutions.drawing_utils


    def findhands(self, frame, draw = True):
        imgRGB = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpdraw.draw_landmarks(frame, handLms, self.mpHands.HAND_CONNECTIONS) 
        

        return frame

    
    def findposition(self, frame, handno =0, draw = True):
            lmlist = []
            if self.results.multi_hand_landmarks:
                myhand =  self.results.multi_hand_landmarks[handno]
                for id, lm in enumerate(myhand.landmark):
                    height, width, c = frame.shape
                    cx, cy = int(lm.x * width), int(lm.y * height)
                    #print(id, cx,cy)
                    lmlist.append([id,cx,cy])
                    if draw:
                        cv.circle(frame, (cx,cy), 10, (255,0,0), cv.FILLED)

            #self.mpdraw.draw_landmarks(frame, handLms, self.mpHands.HAND_CONNECTIONS)

            return lmlist

    

    

def main():

    cap = cv.VideoCapture(0)
    ptime = 0 
    ctime= 0

    detector = handDetector()
    
    while True:
        isTrue, frame = cap.read()

        frame = detector.findhands(frame)
        lmlist = detector.findposition(frame)
        if len(lmlist)!=0:
            print(lmlist[4])

        ctime = time.time()
        fps = 1/(ctime-ptime)
        ptime = ctime
        cv.putText(frame, str(int(fps)),(10,70), cv.FONT_HERSHEY_COMPLEX,3, (255,0,255),3)


        cv.imshow('yo!', frame)
        if cv.waitKey(20)& 0xFF == ord('0'):
            break



    cap.release()
    cv.destroyAllWindows()



if __name__ == "__main__":
    main()