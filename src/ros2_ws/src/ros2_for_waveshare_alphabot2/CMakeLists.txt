cmake_minimum_required(VERSION 3.5)
project(ros2_for_waveshare_alphabot2)

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)

# Add your messages
rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/IR.msg"
  "msg/LineFollow.msg"
  "msg/LineFollowStamped.msg"
  "msg/ObstacleStamped.msg"
  "msg/PanTilt.msg"
  "msg/PanTiltStamped.msg"
  "msg/RGBLED.msg"
)

# Install Python executables and libraries
ament_python_install_package(${PROJECT_NAME})

# Install launch files
install(DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}/
)

# Install services
install(DIRECTORY services
  DESTINATION share/${PROJECT_NAME}/
)

# Install resource directory
install(DIRECTORY resource
  DESTINATION share/${PROJECT_NAME}/
)

# Install urdf directory
install(DIRECTORY urdf
  DESTINATION share/${PROJECT_NAME}/
)

# Install scripts
install(PROGRAMS
  ros2_for_waveshare_alphabot2/ir_control.py
  ros2_for_waveshare_alphabot2/joystick.py
  ros2_for_waveshare_alphabot2/motion.py
  ros2_for_waveshare_alphabot2/pan_tilt.py
  ros2_for_waveshare_alphabot2/rgb_leds.py
  ros2_for_waveshare_alphabot2/sensors.py
  ros2_for_waveshare_alphabot2/sound.py
  ros2_for_waveshare_alphabot2/test.py
  ros2_for_waveshare_alphabot2/test2.py
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
