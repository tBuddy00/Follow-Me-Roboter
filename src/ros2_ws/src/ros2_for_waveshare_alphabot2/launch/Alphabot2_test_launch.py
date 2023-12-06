from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='ros2_for_waveshare_alphabot2',
            executable='alphabot2_test',
            name='alphabot2_test',
            output='screen',
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(['Alphabot2_standard_launch.py']),
        ),
    ])