"""
This file is used to convert a commonroad scenario to a .json file with a dictionary of the following
format: network.json= {"LaneletId": [left bound points][right bound points]}
""" 
import numpy as np
import cv2
import matplotlib.pyplot as plt
from commonroad.common.file_reader import CommonRoadFileReader
from commonroad.visualization.draw_dispatch_cr import draw_object
import json
from drawer import *
import argparse
import os

def main(PATH_FILE,SCALE_FACTOR=1):    
    scenario, planning_problem_set = CommonRoadFileReader(PATH_FILE).open()
    print("Converting to json network...\n")
    cam_img=255*np.ones(shape=[720,1280], dtype = np.uint8)

    network= find_road_network(scenario)
    
    SAVE_PATH=os.path.join(f"{os.path.dirname(os.path.dirname(PATH_FILE))}","json_network")
    # print(SAVE_PATH)
    with open(f"{os.path.join(SAVE_PATH,os.path.splitext(os.path.basename(PATH_FILE))[0])}.json","w") as fp:
        
        json.dump(network, fp, sort_keys=True, indent=4)
    print("Conversion Successful.")
    print(f"\nFile {os.path.splitext(os.path.basename(PATH_FILE))[0]}.json saved at the following location:\n{SAVE_PATH}\n")
    # cv2.imshow("image ", artist.scenario_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
  

def parse_arguments():
    
    my_parser= argparse.ArgumentParser(description="Give the network file from the custom_scenarios/commonroad_network directory.")
    my_parser.add_argument("-i", "--input", required=True,help="input network file path")
    # my_parser.add_argument("-d","--display", default="True"  ,help="output network file name")
    args=vars(my_parser.parse_args())
    
    return args


def find_road_network(scenario):
        # This function returns the list of points that make up a road network
        # from the given commonroad scenario. 
        lanelets=dict()
        lanelet_list=scenario.lanelet_network.lanelets
        
        for lanelet in lanelet_list:
            # print(lanelet.lanelet_id)
            val= [lanelet.left_vertices.tolist(),lanelet.right_vertices.tolist()]
            lanelets[lanelet.lanelet_id]=val

        return lanelets   

if __name__ == '__main__':
    args= parse_arguments()
    main(args['input'])





