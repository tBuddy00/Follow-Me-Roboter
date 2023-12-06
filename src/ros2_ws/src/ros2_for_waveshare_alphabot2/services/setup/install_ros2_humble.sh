#!/bin/bash

# Set locale
locale
while :
do
  echo 'Make sure you have a locale that supports UTF-8 - continue [y/n]'
  read INPUT_STRING
  case $INPUT_STRING in
    y|Y)
      break
      ;;
    n|N)
      echo 'Install UTF-8 and repeat the installation' 
      exit 1
      ;;
    *)
      echo "Wrong input"
      ;;
  esac
done

sudo apt update && sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8

locale

while :
do
  echo 'Verify your settings if they have been set to en_US.UTF-8 - continue [y/n]'
  read INPUT_STRING
  case $INPUT_STRING in
    y|Y)
      break
      ;;
    n|N)
      echo 'Look at the installation guide for help' 
      exit 1
      ;;
    *)
      echo "Wrong input"
      ;;
  esac
done

# Setup Sources
sudo apt install software-properties-common
sudo add-apt-repository universe
sudo apt update && sudo apt install curl -y
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

# Install ROS 2 packages
sudo apt update
sudo apt upgrade
while :
do
  echo 'Which version do you want to install - Desktop Install (Recommended)[D] / ROS-Base Install (Bare Bones) [B]'
  read INPUT_STRING
  case $INPUT_STRING in
    d|D)
      # Desktop Install (Recommended): ROS, RViz, demos, tutorials.
      sudo apt install ros-humble-desktop || { echo "Error installing ROS Desktop"; exit 1; }
      break
      ;;
    b|B)
      # ROS-Base Install (Bare Bones): Communication libraries, message packages, command line tools. No GUI tools.
      sudo apt install ros-humble-ros-base || { echo "Error installing ROS Base"; exit 1; }
      break
      ;;
    *)
      echo "Wrong input"
      ;;
  esac
done

# Development tools: Compilers and other tools to build ROS packages
sudo apt install ros-dev-tools || { echo "Error installing ROS development tools"; exit 1; }

# Environment setup: Sourcing the setup script
source /opt/ros/humble/setup.bash

echo "ros2 humble successfully installed" 