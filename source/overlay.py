"""
THIS FILE SOLVES THE PURPOSE OF SCALING AND TRANSLATING THE COMMONROAD SCENARIOS
WITH A FACTOR SUCH THAT EVERY POINT (X,Y) ON THE HARDWARE TESTBED CAN BE 
MAPPED TO THE SCENARIO.
""" 
import cv2
import numpy as np
import json
import argparse
import os

def main(file_name):
    DEFAULT_DIR=os.path.join(os.path.join(os.path.dirname(os.getcwd()),"custom_scenarios"),'json_network')
    FILE_PATH=os.path.join(DEFAULT_DIR,file_name)

    # this scale factor was calculated used in finding the homography matrix. DO NOT CHANGE IMG_SCALE_FACTOR.
    IMG_SCALE_FACTOR=3
    # DO NOT CHANGE
    WORKSPACE_DIM={"Width": 750,
                   "Height": 750}
    CAR_WIDTH=30*IMG_SCALE_FACTOR
    ORIGIN=[7,7]
    
    overlayer=Overlay(FILE_PATH,CAR_WIDTH,WORKSPACE_DIM,ORIGIN)
    
    capture =cv2.VideoCapture(1)
    while(1):
        ret, frame= capture.read()
        # We need to overlay a colored path over the image.Opencv doesnt allow us to overlay 
        # coloured images over Gray images
        im_out= cv2.cvtColor(overlayer.cam_calibrate(frame,WORKSPACE_DIM),cv2.COLOR_GRAY2BGR)
        
        
        cv2.imshow('final', overlayer.overlay_network(im_out))
        
        k=cv2.waitKey(1)#(to play at 30 fps for a video)
        if k == 27:
            break
        
    capture.release()
    cv2.destroyAllWindows()


class Overlay():
    def __init__(self,json_network,car_width,WORKSPACE_DIM,ORIGIN=[0,0]):
        self.car_width=car_width
        self.json_network=json_network
        self.WORKSPACE_DIM=WORKSPACE_DIM
        self.ORIGIN=ORIGIN
        self.network,self.intrinsics,self.homography,self.scale_factor=self.load_data(self.json_network,
                                                                                         self.car_width) 
        self.net_img=self.generate_network_image(self.WORKSPACE_DIM,self.ORIGIN)
    
    def load_data(self,FILE_PATH,CAR_WIDTH):
        network=dict()
        print("loading network...")
        with open(FILE_PATH, 'r') as fp:
            network = json.load(fp)
        
        intrinsics=np.load('git3_calib_best.npz')
        homography=np.load('homography.npz')
        scale_factor=self.find_scale(network,CAR_WIDTH)

        return network,intrinsics,homography,scale_factor

    def cam_calibrate(self,frame,WORKSPACE_DIM):
        rectified_img=cv2.undistort(frame, self.intrinsics['mtx'], self.intrinsics['dist'], None)
        gray= cv2.cvtColor(rectified_img, cv2.COLOR_BGR2GRAY)
        im_out = cv2.warpPerspective(gray, self.homography['homography'], 
                        (int(WORKSPACE_DIM["Width"]),int(WORKSPACE_DIM["Height"])))
        
        return im_out
    

    def find_scale(self,network,car_width):
        min_width=self.find_min_width(network)
        scale=car_width/min_width
        return scale


    def find_min_width(self,network):
        min_width=1000000000000
        for id in network:
            width=self.distance(network[id][0][0],network[id][1][0])
            if width <min_width:
                min_width=width
        return min_width

    def generate_network_image(self, dimensions, origin=[0,0]):
        blank_canvas=255*np.ones(shape=[dimensions["Width"],dimensions["Height"],3], dtype = np.uint8)
        boundary=self.find_boundary(self.network)
        [[xmin,ymin],[xmax,ymax]]=boundary
        for id in self.network:
            pointsl=np.array(self.scale(np.array(self.network[id][0]),boundary,self.scale_factor,origin),dtype=int)
            pointsl=pointsl.reshape(-1,1,2)
            pointsr=np.array(self.scale(np.array(self.network[id][1]),boundary,self.scale_factor,origin),dtype=int)
            pointsr=pointsr.reshape(-1,1,2)
            blank_canvas=cv2.polylines(blank_canvas,[pointsl],False, (255,0,100),2)
            blank_canvas=cv2.polylines(blank_canvas,[pointsr],False, (255,0,100),2)
        
        return blank_canvas
        
    def find_boundary(self, network):
        
        list_of_points=list()
        x_list=list()
        y_list=list()
        for id in network:
            for point in network[id][0]:
                list_of_points.append(point)
            for point in network[id][1]:
                list_of_points.append(point)
            for point in list_of_points:
                x_list.append(point[0])
                y_list.append(point[1])
        bound=[[min(x_list), min(y_list)], [max(x_list), max(y_list)]]
        
        return bound    
    
    def distance(self,a,b):
        return ((a[0]-b[0])**2+ (a[1]-b[1])**2)**(1/2)

    def scale(self,list_of_points, boundary, scale_factor,origin):
        ''' 
            THIS FUNCTION SCALES ALL THE POINTS FROM THE SCENARIO 
            TO THE IMAGE ACCORDING TO THE DESIRED PARAMETERS
        '''
        [[xmin,ymin],[xmax, ymax]] = boundary  
        list_of_points[: ,0] = list_of_points[: ,0]- xmin
        
        list_of_points[:,0] =list_of_points[:, 0] * scale_factor+origin[0] 
        
        list_of_points[:,1] = list_of_points[:,1] - ymin
        list_of_points[:,1] =  list_of_points[:,1]
        list_of_points[:,1] =list_of_points[:, 1] * scale_factor +origin[1]
        
        return list_of_points

    def overlay_network(self,image):
        purple=np.array([255,0,100])
        mask=cv2.inRange(self.net_img,purple,purple)
        
        image_bg=cv2.bitwise_and(image,image,mask=cv2.bitwise_not(mask))
        image_fg=cv2.bitwise_and(self.net_img,self.net_img,mask=mask)
        return cv2.add(image_bg,image_fg)
        cv2.imshow('frame',image)
        return cv2.addWeighted(image,0.8,self.net_img,0.2,0)
        
def parse_arguments():
    
    my_parser= argparse.ArgumentParser(description="give the name of the input network file")

    my_parser.add_argument("-i", "--input", required=True,help="input json network file name")
    args=vars(my_parser.parse_args())
    
    return args

if __name__ == '__main__':
    args=parse_arguments()
    main(args["input"])
