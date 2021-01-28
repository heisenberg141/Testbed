# Testbed

### This repository contains the configuration and the implementation of the hardware test bed for the ICPS co-operative perception project.

## Dependencies

1. This code is built on python 3.6.

2. Clone this repository on your system, open a terminal in the repository and run the command: pip3 install -r requirements.txt .

3. Build and install Opencv 4 from source with contrib packages. Refer to the following link: https://www.pyimagesearch.com/2018/08/15/how-to-install-opencv-4-on-ubuntu/.

4. To install Sumo, run the following commands:
`sudo add-apt-repository ppa:sumo/stable`
`sudo apt-get update`
`sudo apt-get install sumo sumo-tools sumo-doc`
`sudo apt-get install ffmpeg`
  
5. To install commonroad to sumo interface, git clone the following repository outside this repository: https://gitlab.lrz.de/tum-cps/commonroad-sumo-interface.git. You may need to change some of the files in order to make the repository compatible with the latest commonroad xml structure.


## Using this repository

This repository consists of two parts. 
#### Configuring the test bed - homography_and_calibration folder

#### Using the testbed - source folder

### Configuring the Testbed
