'''
This file is used to convert an input sumo NET.XML scenario to a .JSON network consisting of a 
dictionary with keys as lanelet id and values as the list 
of points in its left bound and list of points in its right bound.
network.json= {"LaneletId": [left bound points][right bound points]}
'''
import argparse
import generate_json_network
import convert_s2c
import os

def main(file_name):
    SUMO_NETWORK_DIR=os.path.join(os.path.join(os.path.dirname(os.getcwd()),"custom_scenarios"),'sumo_network')
    FILE_PATH=os.path.join(SUMO_NETWORK_DIR,file_name)
    generate_json_network.main(convert_s2c.main(FILE_PATH,"True"))

def parse_arguments():
    
    my_parser= argparse.ArgumentParser(description="Give the name of the sumo file which you would like to convert.")
    my_parser.add_argument("-i", "--input", required=True,help="input sumo network file name")
    args=vars(my_parser.parse_args())
    return args

if __name__ == '__main__':
    args=parse_arguments()
    main(args['input'])