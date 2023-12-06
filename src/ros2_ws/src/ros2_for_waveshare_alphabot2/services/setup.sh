
# move the directories
mv ~/ros2_ws/src/ros2_for_waveshare_alphabot2/services/lirc ~/lirc
mv ~/ros2_ws/src/ros2_for_waveshare_alphabot2/services/wsRGB ~/wsRGB
mv ~/ros2_ws/src/ros2_for_waveshare_alphabot2/services/setup ~/setup

# make the needed files executable
chmod +x ~/setup/reinstall_alphabot.sh
chmod +x ~/setup/full_reinstall_alphabot.sh 
chmod +x ~/setup/reinstall_camera.sh
chmod +x ~/setup/full_reinstall_camera.sh 
chmod +x ~/setup/create_workspace.sh 
chmod +x ~/setup/install_ros2_humble.sh 

# file to set up RGB LED service 
chmod +x ~/wsRGB/setup.sh

while true; do
  echo 'Do you want to run wsRGB/setup.sh to set up the RGB LED service? [y/n]'
  read INPUT_STRING
  case $INPUT_STRING in
    [yY])
        cd ~/wsRGB
        sudo ./setup.sh
        break
        ;;
    [nN])
        break
        ;;
    *)
        echo "Wrong input. Please enter 'y' or 'n'."
        ;;
  esac
done

echo "setup sucsessfull"