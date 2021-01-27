from dt_apriltags import Detector
from overlay import Overlay
import cv2
import numpy as np
from overlay import Overlay
import argparse
import os
import socket



def main(file_name):

    DEFAULT_DIR=os.path.join(os.path.join(os.path.dirname(os.getcwd()),"custom_scenarios"),'json_network')
    FILE_PATH=os.path.join(DEFAULT_DIR,file_name)
    # this scale factor was calculated used in finding the homography matrix. DO NOT CHANGE IMG_SCALE_FACTOR.
    IMG_SCALE_FACTOR=3
    # DO NOT CHANGE
    WORKSPACE_DIM={"Width": 750,
                   "Height": 750}
    
    CAR_WIDTH=45*IMG_SCALE_FACTOR
    ORIGIN=[60,60]

    prev=list()
    current=list()
    overlayer=Overlay(FILE_PATH,CAR_WIDTH,WORKSPACE_DIM,ORIGIN)
    
    capture=cv2.VideoCapture(1)
    trajectory= 255*np.ones(shape=[WORKSPACE_DIM["Width"],WORKSPACE_DIM["Height"],3], dtype = np.uint8)
    
    HOST = get_ip()   # Standard loopback interface address (localhost)
    PORT = 12345        # Port to listen on (non-privileged ports are > 1023)
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT))
        server.listen()
        conn, addr = server.accept()
        with conn:
            print('Connected by', addr)
            # while True:
            #     data = conn.recv(1024)
            #     if not data:
            #         break
            #     conn.sendall(data)

            while(1):
                ret, frame= capture.read()
                im_out= overlayer.cam_calibrate(frame,WORKSPACE_DIM)
                
                detector=create_detector()
                
                if detector.detect(im_out):
                    results=detector.detect(im_out)
                
                    for tag in results:
                        if tag.tag_id==1:
                
                            current=np.array(tag.center,np.int32)
                            data= str(current//IMG_SCALE_FACTOR).encode()   
                            conn.send(data)
                            trajectory=draw_trajectory(prev,current,trajectory)
                            prev=current


                im_out=cv2.cvtColor(im_out,cv2.COLOR_GRAY2BGR)
                
                cv2.imshow('final', cv2.addWeighted(overlayer.overlay_network(im_out),0.8,trajectory,0.2,0))
                
                k=cv2.waitKey(1)#(to play at 30 fps for a video)
                if k == 27:
                    break

        
    capture.release()
    cv2.destroyAllWindows()

def draw_trajectory(prev, current,trajectory):
    if len(prev)==0:
        trajectory= cv2.circle(trajectory, (current[0],current[1]),2,(0,0,255),-1)
    else:
        list_of_points=np.array([prev,current])
        list_of_points=list_of_points.reshape((-1,1,2))
        trajectory=cv2.polylines(trajectory,[list_of_points],True,(0,0,255),2)

    return trajectory
    
        
def get_ip():
    gw = os.popen("ip -4 route show default").read().split()    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((gw[2], 0))
    ipaddr = s.getsockname()[0]
    print(f"Host IP is {ipaddr}")
    return ipaddr

def create_detector():
    detector=Detector(families='tag36h11',
                           nthreads=1,
                           quad_decimate=1.0,
                           quad_sigma=0.8,
                           refine_edges=1,
                           decode_sharpening=0.5,
                           debug=0)
    return detector

def parse_arguments():
    
    my_parser= argparse.ArgumentParser(description="give the name of the input network file")

    my_parser.add_argument("-i", "--input", required=True,help="input json network file name")
    args=vars(my_parser.parse_args())
    
    return args


if __name__ == '__main__':
    args=parse_arguments()
    main(args['input'])