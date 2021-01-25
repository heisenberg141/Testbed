''' 
    THIS FILE IS USED TO FIND HOMOGRAPHY MATRIX BETWEEN THE CAMERA PLANE 
    AND THE GROUND PLANE(SINGLE CAMERA). THE MATRIX IS SAVED AS homograpy.npz
'''
from dt_apriltags import Detector
import cv2
import numpy as np

def main():

    '''
        TO FIND HOMOGRAPHY, WE ARE USING THE IMAGE COORDINATES OF MULTIPLE 
        APRILTAGS AS THE DESTINATION POINTS, AND THEIR REAL WORLD COORDINATES
        (AS (X cm, Y cm)) WRT AN ARBITRARY ORIGIN AS THE SOURCE POINTS. 

        TO UNDERSTAND THE CONCEPT OF HOMOGRAPHY, REFER TO THE FOLLOWING LINK:
        https://learnopencv.com/homography-examples-using-opencv-python-c/
    '''
    # This is the dimension of the 
    WORKSPACE_DIM={"Width": 250,
                   "Height": 250}

    # This scale factor is to increase the size of the final image in the final image. 
    # Dont change this scale factor. If for some reason you need to change it, you will 
    # also need to change the parameter IMG_SCALE_FACTOR in the rest of the repository. 
    SCALE_FACTOR=3  
    
    # These are the the real world coordinates of the points we will use to calculate the homography
    ground_truth=[[0,0],       [109,0],          [218,0],
                    [54.5,55.2],     [163.5,55.2],
                  [0,110.4],    [109,110.4],      [218,110.4],
                    [54.5, 165.6], [163.5, 165.6],
                  [0.0, 220.8], [109.0, 220.8],   [218.0, 220.8]]
    
    origin_offset=16
    ground_truth,WORKSPACE_DIM=scale(ground_truth,WORKSPACE_DIM,origin_offset,SCALE_FACTOR)
    ground_truth
    centers=dict()

    # creates a detector object for finding april tags
    detector = create_detector()
    # USE THE INTRINSICS FROM THE CALIBRATION TO UNDISTORT THE IMAGE.
    intrinsics=np.load('git3_calib_best.npz')
    
    capture =cv2.VideoCapture(1)
    
    while(1):
        
        ret, img= capture.read()
        rectified_img=cv2.undistort(img, intrinsics['mtx'], intrinsics['dist'], None)
        gray= cv2.cvtColor(rectified_img, cv2.COLOR_BGR2GRAY)
        # DETECT THE APRILTAGS
        results = detector.detect(gray)
        
        for tag in results:
            center=display_tag_center(tag,rectified_img)
            # UNCOMMENT TO SEE THE BOUNDING BOX AROUND THE APRIL TAGS
            # display_tag_boundary(tag,rectified_img)
            
            display_tag_id(tag,rectified_img)
            # The coordinates of the centers of the april 
            # tags correspond to the points in the ground truth points 
            centers[tag.tag_id]=center
        
        cv2.imshow('Detected tags rectified', rectified_img)
        
        k=cv2.waitKey(1)
        if k == 27:
            break

    image_points=list()  
    
    # I arranged the april tags on the ground such that the tag of
    # id0 corresponds to the point[0,0] in the ground_truth
    # id1 corresponds to the point[109,0] in the ground_truth
    # id2 corresponds to the point[218,0] in the ground_truth, and so on...

    for iD in range(0,13):
        image_points.append(centers[iD])
    
    h, status = cv2.findHomography(np.float32(image_points),np.float32(ground_truth))
    np.savez('homography.npz',homography=h)
    # THIS PART OF THE CODE CAN BE USED TO CHECK THE ACCURACY OF THE RESULTS. 
    # COMPARE THE W/SCALE_FACTOR AND H/SCALE_FACTOR WITH THE REAL DIMENSIONS OF THE APRILTAGS.
    while(1):
        ret, img= capture.read()
        rectified_img=cv2.undistort(img, intrinsics['mtx'], intrinsics['dist'], None)
        gray= cv2.cvtColor(rectified_img, cv2.COLOR_BGR2GRAY)
        im_out = cv2.warpPerspective(gray, h, 
                (int(WORKSPACE_DIM["Height"]),int(WORKSPACE_DIM["Width"])))
        
        results = detector.detect(im_out)
        for tag in results:
            if tag.tag_id==12:
                pts=np.array(tag.corners,np.int32)
                print(f"Tag {tag.tag_id}  Co-ordinates: {tag.corners}")
                print(f"W:{tag.corners[0][0]-tag.corners[2][0]}\n H: {tag.corners[0][1]-tag.corners[1][1]}")
                pts=pts.reshape((-1,1,2))
                im_out = cv2.polylines(im_out,[pts],True,(0,255,0),2)
            

        cv2.imshow('transformed', im_out)
        cv2.imshow('normal', rectified_img)
        k=cv2.waitKey(1)#(to play at 30 fps for a video)
        if k == 27:
            break
        
    
    capture.release()
    cv2.destroyAllWindows()

def display_tag_id(tag,rectified_img):
    print(f"Tag ID: {tag.tag_id}.")
    cv2.putText(rectified_img, str(tag.tag_id),
                org=(tag.corners[0, 0].astype(int)+10,tag.corners[0, 1].astype(int)+10),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=0.6,
                color=(0, 0, 255))
    return tag.tag_id

def scale(ground_truth,WORKSPACE_DIM,origin_offset=0,SCALE_FACTOR=1):
    
    for i,row in enumerate(ground_truth):
        for j,elem in enumerate(row):
            ground_truth[i][j]+=origin_offset
            ground_truth[i][j]*=SCALE_FACTOR
    for dim in WORKSPACE_DIM:
        WORKSPACE_DIM[dim]*=SCALE_FACTOR

    return ground_truth,WORKSPACE_DIM

def display_tag_center(tag,rectified_img):
    center=(int(tag.center[0]),int(tag.center[1]))
    print(f"Tag {tag.tag_id} center Co-ordinates: {center}")
    rectified_img= cv2.circle(rectified_img, center,2,(0,0,255),-1)
            
    return center
def display_tag_boundary(tag, rectified_img):
    pts=np.array(tag.corners,np.int32)
    pts=pts.reshape((-1,1,2))
    rectified_img = cv2.polylines(rectified_img,[pts],True,(0,255,0),2)

def create_detector():
    detector=Detector(families='tag36h11',
                           nthreads=1,
                           quad_decimate=1.0,
                           quad_sigma=0.0,
                           refine_edges=1,
                           decode_sharpening=0.5,
                           debug=0)
    return detector

if __name__ == '__main__':
    main()