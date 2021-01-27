'''
THIS FILE CONTAINS A DRAWER CLASS WHICH CONTAINS FUNCTIONS TO DRAW 
A ROAD NETWORK ON AN ARBITRARY WHITE IMAGE, GIVEN A SET OF POINTS IN THE LEFT BOUND AND RIGHT BOUND.
'''
import numpy as np
import cv2

class Drawer():

    def __init__(self, scenario, image, scale_factor, origin=[0,0]):
        self.scenario=scenario
        self.image=image
        self.scale_factor=scale_factor
        self.origin=origin
        self.lanelets=self.find_road_network()
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
            print(type(lanelet.left_vertices))
            pointsl=np.array(self.scale_to_image(lanelet.left_vertices,boundary),dtype=int)
            pointsr=np.array(self.scale_to_image(lanelet.right_vertices,boundary),dtype=int)
            pointsl=pointsl.reshape(-1,1,2)
            pointsr=pointsr.reshape(-1,1,2)
            img=cv2.polylines(image,[pointsl],False, (0,0,255))
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
        
    def find_road_network(self):
        lanelets=dict()
        
        lanelet_list=self.scenario.lanelet_network.lanelets
        
        for lanelet in lanelet_list:
            # print(lanelet.left_vertices)
            val= [lanelet.left_vertices.tolist(),lanelet.right_vertices.tolist()]
            lanelets[lanelet.lanelet_id]=val

        return lanelets   
