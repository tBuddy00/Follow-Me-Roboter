#!/bin/bash

#Set locale

#Make sure you have a locale which supports UTF-8
locale  # check for UTF-8

sudo apt update && sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8

locale  # verify settings


#Setup Sources

#You will need to add the ROS 2 apt repository to your system.
#First ensure that the Ubuntu Universe repository is enabled.
sudo apt install software-properties-common
sudo add-apt-repository universe

#Now add the ROS 2 GPG key with apt.
sudo apt update && sudo apt install curl -y
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg

#Then add the repository to your sources list.
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null


#Install ROS 2 packages

#Update your apt repository caches after setting up the repositories.
sudo apt update
sudo apt upgrade




while :
do
  echo 'Wich version do you want to install - Desktop Install (Recommended)[D] / ROS-Base Install (Bare Bones) [B]'
  read INPUT_STRING
  case $INPUT_STRING in
	d||D)
		#Desktop Install (Recommended): ROS, RViz, demos, tutorials.
        sudo apt install ros-humble-desktop
        break
		;;
	b||B)
		#ROS-Base Install (Bare Bones): Communication libraries, message packages, command line tools. No GUI tools.
        sudo apt install ros-humble-ros-base
		break
		;;
	*)
		echo "Wrong imput"
		;;
  esac
done

if [$input]




#Development tools: Compilers and other tools to build ROS packages
sudo apt install ros-dev-tools


#Environment setup
#Sourcing the setup script

source /opt/ros/humble/setup.bash