from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='ros2_for_waveshare_alphabot2',
            executable='pan_tilt',
            name='camera_pan_tilt_node',
            output='screen',
            parameters=[
                {'pan_offset': 0.0},  # Adjust values as needed
                {'tilt_offset': 0.0},
                {'pan_limit_left': 1.5},
                {'pan_limit_right': 1.5},
                {'tilt_limit_up': 1.4},
                {'tilt_limit_down': 1.0},
                {'rate': 10}  # Adjust as needed
            ],
        ),

        Node(
            package='ros2_for_waveshare_alphabot2',  # replace with your actual package name
            executable='joystick',  # replace with your actual node script name
            name='joystick',
            output='screen',
            emulate_tty=True,
            parameters=[{'rate': 10}],  # replace with your desired parameters
        ),

        Node(
            package='ros2_for_waveshare_alphabot2',  # replace with your actual package name
            executable='alphabot2_test2',  # replace with your actual node script name
            name='alphabot2_test2',
            output='screen',
            emulate_tty=True,
        ),     

    ])
