'''USE THIS CODE TO CAPTURE IMAGES FOR INTRINSIC CALIBRATION OF ANY CAMERA. 
    WHILE THE VIDEO FEED IS ON, PLACE THE CHECKERBOARD PATTERN IN MULTIPLE 
    ORIENTATIONS AND PLACES AND USE THE S KEY TO SAVE THE IMAGE. 
    PRESS ESC TO CLOSE THE VIDEO FEED. AFTER YOU ARE DONE CAPTURING THE IMAGES, RUN calib.py'''
import numpy as np
import cv2
import os

def main():
    path='calibration_images'
    num=0  
    capture = cv2.VideoCapture(0)
#                                  (or 0)
    while(True):
        ret, frame = capture.read()
        gray= cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow('gray',gray)
        k=cv2.waitKey(1)#(to play at 30 fps for a video)
        if k == 27:
            break
        elif k==ord('s'):
            cv2.imwrite(os.path.join(path,f"left{num}.jpg"), gray)
            num+=1
    capture.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()