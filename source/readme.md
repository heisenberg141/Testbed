# Source Directory
__This directory contains python scripts with use cases of the test bed.__

As of now the testbed can be used for the following applications:  
__1. Overlaying a road network  
2. mapping the trajectory of a moving vehicle__

## Overlaying a road Network:
1. For overlaying a road network, you need to make a suitable road network using sumo's netedit tool. Refer to the following tutorials: https://sumo.dlr.de/docs/Tutorials.html. The road network created using sumo is be of the format `.net.xml` and should be saved at the path `../custom_scenarios/sumo_network`. This will ensure smooth working of code.  
2. After creating the road network in netedit and saving it in the `../custom_scenarios/sumo_network` directory, run the following command in a terminal at the source directory: `python3 generate_network.py -i <name_of_your_file>.net.xml`. This will convert the given sumo road network to both, a commonroad scenario `.xml` file and `.json` file, both with the same name as `name_of_your_file`. They are saved at paths   `../custom_scenarios/commonroad_network` and `../custom_scenarios/json_network` respectively.  
3. After the creation of the `.json` file,connect the ceiling camera to your computer,and  in the source directory run the command `python3 overlay.py -i <name_of_your_file>.json`.
You should see a video feed similar to the image as shown below.  
![illustration](overlay_illustration.png | width = 250)


