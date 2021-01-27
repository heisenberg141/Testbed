
'''
THIS FILE IS USED TO CONVERT THE INPUT SUMO ROAD NETWORK IN net.xml FORMAT
TO A COMMONROAD ROAD NETWORK IN.xml FORMAT
'''
import sys
import os
import warnings
warnings.filterwarnings("ignore")
import matplotlib.pyplot as plt
from typing import List
# add path to the commonroad sumo interface
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.getcwd())),'commonroad-sumo-interface'))
from sumo2cr.maps.sumo_scenario import ScenarioWrapper
from commonroad.common.util import Interval
from commonroad.scenario.trajectory import State

from commonroad.scenario.scenario import Scenario
from commonroad.visualization.draw_dispatch_cr import draw_object
from commonroad.common.file_writer import CommonRoadFileWriter
from commonroad.scenario.scenario import Tag
import argparse

DEFAULT_DIR='../custom_scenarios/sumo_network'

def main(input_file,display):
    
    print("\nLoading Sumo Network...\n")
    net_file=input_file
    sumo_cfg_file=os.path.join(DEFAULT_DIR,"HW.sumocfg")
    print("Sumo Network Loaded.\n")
    
    print("Converting to commonroad network...\n")
    CR_SCEN_FILE=os.path.join(os.path.dirname(DEFAULT_DIR),
                                f'commonroad_network/{os.path.splitext(os.path.splitext(os.path.basename(input_file))[0])[0]}.xml')
    cr_scenario= generate_scenario(net_file,sumo_cfg_file,CR_SCEN_FILE)
    
    if display=="True":
        print("\nDisplaying CommonRoad Network.\n")
        display_cr_network(cr_scenario)
    
    return CR_SCEN_FILE


def generate_scenario(net_file,sumo_cfg_file,cr_scen_file):
    dt = 0.1
    n_vehicles_max:int = 30
    veh_per_second = 50
    n_ego_vehicles:int = 1
    ego_ids:List[int] = []
    initial_states:List[State] = []
    ego_start_time:int=10
    departure_time_ego = 3
    departure_interval_vehicles = Interval(0,20)
    
    scenario = ScenarioWrapper.full_conversion_from_net(net_file, dt, n_vehicles_max, n_ego_vehicles, 
                                                        ego_ids, ego_start_time, departure_time_ego, 
                                                        departure_interval_vehicles,veh_per_second)
    Scenario=create_scenario(cr_scen_file,scenario.lanelet_network)
    return scenario
    
def create_scenario(file,network):
    scen=Scenario(dt=0.1,author="Hitesh",scenario_id=1,tags={Tag.SINGLE_LANE},affiliation="NA")
    scen.add_objects(network)
    writer=CommonRoadFileWriter(scenario=scen,planning_problem_set=None, author="Hitesh",source=" ")
    writer.write_scenario_to_file(filename=file)
    return scen

def display_cr_network(scenario):
    
    plt.figure(figsize=(25, 25))
    draw_object(scenario.lanelet_network)
    plt.autoscale()
    plt.axis('equal')
    plt.xlim([290,380])
    plt.ylim([195,250])
    plt.show()
    return

def parse_arguments():
    
    my_parser= argparse.ArgumentParser(description="Give the network file from the custom_scenarios/sumo_network directory.")
    my_parser.add_argument("-i", "--input", required=True,help="input network file name")
    my_parser.add_argument("-d","--display", default="True"  ,help="Display the Network?")
    args=vars(my_parser.parse_args())
    
    return args

if __name__ == '__main__':
    args=parse_arguments()
    input_file= os.path.join(DEFAULT_DIR,args['input'])
    
    if not os.path.exists(input_file):
        print("input file is invalid")
        sys.exit()
    
    CFNAME=main(input_file,args['display'])
    print(f"\nfile saved at:\n {FNAME}.\n")
    
