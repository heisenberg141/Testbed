'''
    AFTER CLICKING THE IMAGES FOR CALIBRATION BY RUNNNING calib_images.py,
    RUN THIS FILE TO ESTIMATE THE CAMERA MATRIX AND DISTORTION COEFFICIENTS 
    IT WILL BE SAVED IN THE CURRENT DIRECTORY AS git3_calib_best.npz
'''

import cv2
import numpy as np
import os 
import glob

CHECKERBOARD=(6,9)

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

objpoints = []

imgpoints = []

objp = np.zeros((1, CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)

objp[0,:,:2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)

prev_img_shape = None

images = glob.glob('calibration_images/*.jpg')
for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)
    if ret == True:
        objpoints.append(objp)

        corners2 = cv2.cornerSubPix(gray, corners, (11,11),(-1,-1), criteria)
        imgpoints.append(corners2)
        img = cv2.drawChessboardCorners(img, CHECKERBOARD, corners2, ret)
    cv2.imshow('img',img)
    cv2.waitKey(0)
cv2.destroyAllWindows()

h,w = img.shape[:2]

ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

np.savez('git3_calib_best.npz',ret=ret,mtx=mtx,dist=dist,rvecs=rvecs,tvecs=tvecs)


print("Camera matrix : \n")
print(mtx)

total_error = 0

for i in range(len(objpoints)):
    imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
    error = cv2.norm(imgpoints[i],imgpoints2, cv2.NORM_L2)/len(imgpoints2)
    total_error+= error

print("Reprojection Error: ", total_error/len(objpoints))
