#!/bin/bash

# Navigate to the source directory of the ROS 2 workspace
cd ~/ros2_ws/src || exit 1

# Remove the existing package directory and clone the latest from the repository
rm -rf camera_package && git clone  https://github.com/cl-ire/camera_package.git || exit 1

# Navigate to the install directory
cd ~/ros2_ws/install || exit 1

# Remove the existing package installation
rm -rf camera_package || exit 1

# Navigate to the build directory
cd ~/ros2_ws/build || exit 1

# Remove the existing build
rm -rf camera_package || exit 1

# Navigate back to the ROS 2 workspace
cd ~/ros2_ws || exit 1

# Build the ROS 2 workspace using colcon with symlink installation
colcon build --symlink-install || exit 1

# Source the setup file to make the changes take effect
source install/setup.bash || exit 1

echo "camera_package cleaned and rebuilt successfully."
