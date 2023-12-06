#!/bin/bash

# Create a new directory
mkdir -p ~/ros2_ws/src || { echo "Error creating src directory"; exit 1; }
cd ~/ros2_ws/ || { echo "Error changing directory to ros2_ws"; exit 1; }

# Resolve dependencies
sudo rosdep init || { echo "Error initializing rosdep"; exit 1; }
rosdep update || { echo "Error updating rosdep"; exit 1; }
rosdep install -i --from-path src --rosdistro humble -y || { echo "Error installing dependencies with rosdep"; exit 1; }

# Build the workspace with colcon
colcon build || { echo "Error building the workspace with colcon"; exit 1; }

echo "workspace sucsesfully created"