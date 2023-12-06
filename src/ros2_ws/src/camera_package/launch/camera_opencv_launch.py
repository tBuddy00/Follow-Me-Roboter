from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import LogInfo
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    return LaunchDescription([
        LogInfo(
            action=LogInfo.LogInfo.DEFAULT,
            msg="Launching CameraOpencv node..."
        ),
        Node(
            package='camera_package',
            executable='camera_opencv',
            name='camera_opencv',
            output='screen',
            parameters=[
                {'distance': 0.0},
            ],
        ),
        Node(
            package='camera_package',
            executable='movement_control',
            name='movement_control',
            output='screen',
            parameters=[
                {'pan_factor': 0.0},
                {'tilt_factor': 0.0},
            ],
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([Ros2_for_Waveshare_Alphabot2, 'Alphabot2_standard_launch.py']),
        ),
    ])
