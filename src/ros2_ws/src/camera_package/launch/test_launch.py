from launch import LaunchDescription
from launch_ros.actions import Node
# from launch.actions import IncludeLaunchDescription
# from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    return LaunchDescription([
        
        Node(
            package='camera_package',
            executable='camera_test',
            name='camera_test',
            output='screen',
        ),

        Node(
            package='v4l2_camera',
            executable='v4l2_camera_node',
            name='v4l2_camera_node',
            output='screen',
            parameters=[
                {'image_size': [1280,960]},
            ],
        ),

    ])
