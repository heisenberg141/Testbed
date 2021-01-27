"""
THIS FILE SOLVES THE PURPOSE OF SCALING AND TRANSLATING THE COMMONROAD SCENARIOS
WITH A FACTOR SUCH THAT EVERY POINT (X,Y) ON THE HARDWARE TESTBED CAN BE 
MAPPED TO THE SCENARIO.
""" 

from dt_apriltags import Detector
import cv2
import numpy as np
import json

def main():
    detect_april_tags=False
    IMG_SCALE_FACTOR=3
    WORKSPACE_DIM={"Width": 750,
                   "Height": 750}
    CAR_WIDTH=30*IMG_SCALE_FACTOR
    ORIGIN=[50,50]
    file_name="reverse_six.json"
    network,boundary,intrinsics,homography,detector,scale_factor=load_data(file_name,CAR_WIDTH) 
    print(scale_factor)
    capture =cv2.VideoCapture(1)
    
    while(1):
        ret, img= capture.read()
        im_out= transform_img(img,intrinsics,homography,WORKSPACE_DIM)
        im_out=draw_network(im_out,network,boundary,scale_factor,ORIGIN)
        
        if detect_april_tags:
            results = detector.detect(im_out)
            for tag in results:            
                pts=np.array(tag.corners,np.int32)
                print(f"Tag {tag.tag_id}  Co-ordinates:\n {tag.corners}")
                print(f"W:{distance(tag.corners[0],tag.corners[1])} H: {distance(tag.corners[1],tag.corners[2])}")
                pts=pts.reshape((-1,1,2))
                im_out = cv2.polylines(im_out,[pts],True,(0,255,0),2)
        


        cv2.imshow('transformed', im_out)
        # cv2.imshow('normal', rectified_img)
        k=cv2.waitKey(1)#(to play at 30 fps for a video)
        if k == 27:
            break
        
    capture.release()
    cv2.destroyAllWindows()

def load_data(file_name,CAR_WIDTH):
    network=dict()
    print("loading network...")
    with open(file_name, 'r') as fp:
        network = json.load(fp)
    boundary=network['-1'][0]
    del network['-1']
    
    intrinsics=np.load('git3_calib_best.npz')
    homography=np.load('homography.npz')
    detector = create_detector()
    scale_factor=find_scale(network,CAR_WIDTH)

    return network,boundary,intrinsics,homography,detector,scale_factor

def transform_img(img,intrinsics,homography,WORKSPACE_DIM):
    # cv2.imshow('original', img)
    rectified_img=cv2.undistort(img, intrinsics['mtx'], intrinsics['dist'], None)
    # cv2.imshow('undistorted', rectified_img)
    gray= cv2.cvtColor(rectified_img, cv2.COLOR_BGR2GRAY)
    im_out = cv2.warpPerspective(gray, homography['homography'], 
                        (int(WORKSPACE_DIM["Height"]),int(WORKSPACE_DIM["Width"])))
    return im_out

def find_scale(network,car_width):
    min_width=find_min_width(network)
    scale=car_width/min_width
    return scale
    
def find_min_width(network):
    min_width=1000000000000
    for id in network:
        width=distance(network[id][0][0],network[id][1][0])
        if width <min_width:
            min_width=width
    return min_width
    
def create_detector():
    detector=Detector(families='tag36h11',
                           nthreads=1,
                           quad_decimate=1.0,
                           quad_sigma=0.0,
                           refine_edges=1,
                           decode_sharpening=0.5,
                           debug=0)
    return detector

def display_tag_id(tag,rectified_img):
    print(f"Tag ID: {tag.tag_id}.")
    cv2.putText(rectified_img, str(tag.tag_id),
                org=(tag.corners[0, 0].astype(int)+10,tag.corners[0, 1].astype(int)+10),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=0.6,
                color=(0, 0, 255))
    return tag.tag_id

def display_tag_center(tag,rectified_img):
    center=(int(tag.center[0]),int(tag.center[1]))
    print(f"Tag {tag.tag_id} center Co-ordinates: {center}")
    rectified_img= cv2.circle(rectified_img, center,2,(0,0,255),-1)
            
    return center

def display_tag_boundary(tag, rectified_img):
    pts=np.array(tag.corners,np.int32)
    pts=pts.reshape((-1,1,2))
    rectified_img = cv2.polylines(rectified_img,[pts],True,(0,255,0),2)

def distance(a,b):

    return ((a[0]-b[0])**2+ (a[1]-b[1])**2)**(1/2)

def draw_network(image, network,boundary,scale_factor,origin):
    
    for id in network:
        pointsl=np.array(scale(np.array(network[id][0]),boundary,scale_factor,origin),dtype=int)
        pointsl=pointsl.reshape(-1,1,2)
        pointsr=np.array(scale(np.array(network[id][1]),boundary,scale_factor,origin),dtype=int)
        pointsr=pointsr.reshape(-1,1,2)
        image=cv2.polylines(image,[pointsl],False, (0,0,255),2)
        image=cv2.polylines(image,[pointsr],False, (0,0,255),2)
    #     
    #     
    # lanelet_list=scenario.lanelet_network.lanelets
    # for lanelet in lanelet_list:
    #     pointsl=np.array(self.scale_to_image(lanelet.left_vertices,boundary),dtype=int)
    #     pointsr=np.array(self.scale_to_image(lanelet.right_vertices,boundary),dtype=int)
    #     pointsl=pointsl.reshape(-1,1,2)
    #     pointsr=pointsr.reshape(-1,1,2)
    #     img=cv2.polylines(image,[pointsl],False, (0,0,255))
    #     img=cv2.polylines(image,[pointsr],False, (0,0,255))
        
    return image
def scale(list_of_points, boundary, scale_factor,origin):
    ''' 
        THIS FUNCTION SCALES ALL THE POINTS FROM THE SCENARIO 
        TO THE IMAGE ACCORDING TO THE DESIRED PARAMETERS
    '''
    # print(list_of_points)
    # print(boundary)
    # scale_factor=20
    [[xmin,ymin],[xmax, ymax]] = boundary  
    list_of_points[: ,0] = list_of_points[: ,0]- xmin
    # print(list_of_points[: ,0])
    list_of_points[:,0] =list_of_points[:, 0] * scale_factor+origin[0] 
    
    list_of_points[:,1] = list_of_points[:,1] - ymin
    list_of_points[:,1] = ymax-ymin - list_of_points[:,1]
    list_of_points[:,1] =list_of_points[:, 1] * scale_factor +origin[1]
    
    return list_of_points
if __name__ == '__main__':
    main()
