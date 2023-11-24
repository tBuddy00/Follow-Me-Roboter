#!/bin/bash

#Create a new directory
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/

#Resolve dependencies
sudo rosdep init
rosdep update
rosdep install -i --from-path src --rosdistro humble -y

#Build the workspace with colcon
colcon build