import cv2 as cv
#import mediapipe as mp
import numpy as np
import time
import handtrackingmodule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


wcam, hcam = 640, 480
cap = cv.VideoCapture(0)
cap.set(3,wcam)
cap.set(4,hcam)
ptime = 0 


detector = htm.handDetector(detectioncon=0.7)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volumeRange = volume.GetVolumeRange()
minvol = volumeRange[0]
maxvol = volumeRange[1]


while True:
    isTrue, frame = cap.read()

    frame = detector.findhands(frame)
    lmlist = detector.findposition(frame, draw=False)
    if len(lmlist)!=0:
        #print(lmlist[4], lmlist[8])

        x1, y1 = lmlist[4][1], lmlist[4][2]
        x2, y2 = lmlist[8][1], lmlist[8][2]
        cx,cy = (x1+x2)//2,(y1+y2)//2

        cv.circle(frame, (x1,y1), 12, (255,0,0), cv.FILLED)
        cv.circle(frame, (x2,y2), 12, (255,0,0), cv.FILLED)

        cv.line(frame, (x1,y1), (x2,y2),(250,155,155),3)

        cv.circle(frame, (cx,cy), 12, (255,0,0), cv.FILLED)

        length = math.hypot(x2-x1,y2-y1)
        print(length)

        vol = np.interp(length, [50,230], [minvol,maxvol])
        print(int(length),vol)
        volume.SetMasterVolumeLevel(vol, None)

        if length<50:
            cv.circle(frame, (cx,cy),12,(0,0,255),cv.FILLED)






    ctime = time.time()
    fps = 1/(ctime - ptime)
    ptime = ctime
    
    cv.putText(frame, str(int(fps)), (10,70), cv.FONT_HERSHEY_COMPLEX_SMALL, 3, (50,150,250), 3)

    cv.imshow("frame",frame)

    if cv.waitKey(20)&0xFF==ord('0'):
        break

cap.release()
cv.destroyAllWindows()