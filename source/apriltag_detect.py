# import the necessary packages
from dt_apriltags import Detector
import cv2
import numpy as np

detector = Detector(families='tag36h11',
                       nthreads=1,
                       quad_decimate=1.0,
                       quad_sigma=0.0,
                       refine_edges=1,
                       decode_sharpening=0.25,
                       debug=0)

# path="AprilTags36h11/AT1.png"
capture =cv2.VideoCapture(0)
# img= cv2.imread(path)
while(1):
    ret, img= capture.read()
    gray= cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    results = detector.detect(gray)
    for tag in results:
        print(f"Tag {tag.tag_id} corner Co-ordinates: {tag.corners}")
        pts=np.array(tag.corners,np.int32)
        pts=pts.reshape((-1,1,2))
        img = cv2.polylines(img,[pts],True,(0,255,0),2)
    
    cv2.imshow('Detected tags', img)
    k=cv2.waitKey(27)#(to play at 30 fps for a video)
    if k == 27:
        break
capture.release()
cv2.destroyAllWindows()