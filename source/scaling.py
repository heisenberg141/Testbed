"""
THIS FILE SOLVES THE PURPOSE OF SCALING AND TRANSLATING THE COMMONROAD SCENARIOS
WITH A FACTOR SUCH THAT EVERY POINT (X,Y) ON THE HARDWARE TESTBED CAN BE 
MAPPED TO THE SCENARIO.
""" 
import os
import numpy as np
import cv2
import matplotlib.pyplot as plt
# import classes and functions for reading xml file and visualizing commonroad objects
from commonroad.common.file_reader import CommonRoadFileReader
from commonroad.visualization.draw_dispatch_cr import draw_object
from commonroad.scenario.scenario import GeoTransformation
path_file = "../CommonRoad/commonroad-search/scenarios/exercise/ARG_Carcarana-13_1_T-1.xml"



def main():    
    
    scenario, planning_problem_set = CommonRoadFileReader(path_file).open()
    
    plt.figure(figsize=(25, 10))
    draw_object(scenario, draw_params={'time_begin': 0})
    draw_object(planning_problem_set)
    plt.gca().set_aspect('equal')
    
    cam_img=255*np.ones(shape=[720,1280], dtype = np.uint8)

    SCALE_FACTOR=1

    artist= Drawer(scenario, cam_img, SCALE_FACTOR,[20,20])

    cv2.imshow("image ", artist.scenario_image)
    plt.show()
    cv2.waitKey(0)
    cv2.destroyAllWindows()
 
# 

class Drawer():

    def __init__(self, scenario, image, scale_factor, origin=[0,0]):
        self.scenario=scenario
        self.image=image
        self.scale_factor=scale_factor
        self.origin=origin
        self.boundary=self.find_boundary(self.scenario)
        [[xmin,ymin],[xmax,ymax]]=self.boundary
        
        self.scen_img_width=int((xmax-xmin)*self.scale_factor)
        self.scen_img_height=int((ymax-ymin)*self.scale_factor)
        
        self.scenario_image= self.draw_on_image(self.image,self.scenario,self.boundary)
    
    def find_boundary(self, scenario):
        ''' THIS IS THE HELPER FUNCTION WHICH GIVES THE BOUNDARIES OF THE 
            SCENARIO, IE (XMIN, YMIN), (XMAX, YMAX)
        '''

        lanelet_list=scenario.lanelet_network.lanelets
        list_of_points=list()
        x_list=list()
        y_list=list()
        for l in lanelet_list:
            for point in l.left_vertices:
                list_of_points.append(point)
            for point in l.right_vertices:
                list_of_points.append(point)    
            for point in list_of_points:
                x_list.append(point[0])
                y_list.append(point[1])
        bound=[[min(x_list), min(y_list)], [max(x_list), max(y_list)]]
        
        return bound

    def draw_on_image(self,image,scenario,boundary):
        ''' 
            THIS FUNCTION HANDLES HOW, WHAT AND WHERE TO DRAW THE SCENARIO ON THE IMAGE
        '''
        points=list()
        lanelet_list=scenario.lanelet_network.lanelets
        for lanelet in lanelet_list:
            pointsl=np.array(self.scale_to_image(lanelet.left_vertices,boundary),dtype=int)
            pointsr=np.array(self.scale_to_image(lanelet.right_vertices,boundary),dtype=int)
            pointsl=pointsl.reshape(-1,1,2)
            pointsr=pointsr.reshape(-1,1,2)
            img=cv2.polylines(image,[pointsl],False, (255,0,0))
            img=cv2.polylines(image,[pointsr],False, (0,0,255))
        
        return img

    def scale_to_image(self,list_of_points, boundary):
        ''' 
            THIS FUNCTION SCALES ALL THE POINTS FROM THE SCENARIO 
            TO THE IMAGE ACCORDING TO THE DESIRED PARAMETERS
        '''
        
        [[xmin,ymin],[xmax, ymax]] = boundary  
        list_of_points[: ,0] = list_of_points[: ,0]- xmin
        list_of_points[:,0] =list_of_points[:, 0] * self.scale_factor+self.origin[0] 
        
        list_of_points[:,1] = list_of_points[:,1] - ymin
        list_of_points[:,1] = ymax-ymin - list_of_points[:,1]
        list_of_points[:,1] =list_of_points[:, 1] * self.scale_factor +self.origin[1]
        
        return list_of_points
        
    

if __name__ == '__main__':
    main();





# def find_boundary(scenario):
#     lanelet_list=scenario.lanelet_network.lanelets
#     list_of_points=list()
#     x_list=list()
#     y_list=list()
#     for l in lanelet_list:
#         for point in l.left_vertices:
#             list_of_points.append(point)
#         for point in l.right_vertices:
#             list_of_points.append(point)    
#         for point in list_of_points:
#             x_list.append(point[0])
#             y_list.append(point[1])
#     bound=[[min(x_list), min(y_list)], [max(x_list), max(y_list)]]
#     return bound 