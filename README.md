# Testbed

### This repository contains the configuration and the implementation of the hardware test bed for the ICPS co-operative perception project.

## Dependencies

1. This code is built on python 3.6.

2. Clone this repository on your system, open a terminal in the repository and run the command: `pip3 install -r requirements.txt` .

3. Build and install Opencv 4 from source with contrib packages. Refer to the following link: https://www.pyimagesearch.com/2018/08/15/how-to-install-opencv-4-on-ubuntu/.

4. To install Sumo, run the following commands:   
`sudo add-apt-repository ppa:sumo/stable`   
`sudo apt-get update`   
`sudo apt-get install sumo sumo-tools sumo-doc`   
`sudo apt-get install ffmpeg`  
Add the following line at the end of your `~/.bashrc` file: `export SUMO_HOME=/usr/share/sumo`  
`source ~/.bashrc`
  
5. To install commonroad to sumo interface, clone the following repository outside this repository using the command: `git clone https://gitlab.lrz.de/tum-cps/commonroad-sumo-interface.git`.
6.change the directory to the commonroad-sumo-interface repository and rename the file `pathConfig_DEFAULT.py` to `pathConfig.py`.

7. Run the command `pip3 show opendrive2lanelet` and copy the `location` where it is installed.  

8. Change the directory to the `opendrive2lanelet` package directory and locate `network.py` file inside it. 

9. Open the network.py in your favourite editor and change line 125 of the code from  
`scenario = Scenario(dt=dt, benchmark_id=benchmark_id if benchmark_id is not None else "none")`  
to  
`scenario = Scenario(scenario_id=1,dt=dt, benchmark_id=benchmark_id if benchmark_id is not None else "none")`





## Using this repository
This repository consists of two parts:  
__1. Configuring the test bed -__ `homography_and_calibration` directory   
__2. Using the testbed -__ `source` directory

### Configuring the Testbed
The configuration needs to be done prior to running the implementation on the testbed. For complete configuration details, refer to the readme.md file in the `homography_and_calibration` directory.

### Using the testbed
After completing the configuration of the testbed and copying the `homography.npz` and `git3_calib_best.npz` into the source directory, you are in the position to run the python scripts present inside the `source` directory. More description about the implementation details of the scripts and usage is given in the readme file in the `source` directory
