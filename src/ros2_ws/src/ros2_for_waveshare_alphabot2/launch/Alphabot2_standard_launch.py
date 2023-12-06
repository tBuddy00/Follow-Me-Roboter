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
            package='ros2_for_waveshare_alphabot2',
            executable='ir_control.py',
            name='ir_control',
            output='screen',
            emulate_tty=True,
            parameters=[{'rate': 10}],
            env=[('LIRCPATH', '/var/run/lirc/lircd')],
        ),

        Node(
            package='ros2_for_waveshare_alphabot2',  # replace with your actual package name
            executable='joystick',  # replace with your actual node script name
            name='joystick_driver',
            output='screen',
            emulate_tty=True,
            parameters=[{'rate': 10}],  # replace with your desired parameters
        ),

        Node(
            package='ros2_for_waveshare_alphabot2',  # replace with your actual package name
            executable='motion',  # replace with your actual executable name
            name='motion',
            output='screen',
            parameters=[
                {'in1': 13},
                {'in2': 12},
                {'in3': 21},
                {'in4': 20},
                {'ena': 6},
                {'enb': 26},
                {'pa': 50},
                {'pb': 50},
                {'timeout': 2},
                {'rate': 10},
                {'max_speed': 0.25},
                {'wheel_base': 0.093},
            ],
        ),

        Node(
            package='ros2_for_waveshare_alphabot2',  # replace with your actual package name
            executable='rgb_leds',  # replace with your actual executable name
            name='rgb_leds',
            output='screen',
            parameters=[
                {'server_address': 'http://localhost/'},
                {'server_port': '2812'},
                {'rate': 10},
            ],
        ),

        Node(
            package='ros2_for_waveshare_alphabot2',  # Replace with the actual package name
            executable='sensors',  # Replace with the actual executable name
            name='sensors',
            output='screen',
            parameters=[
                {'dr': 16},
                {'dl': 19},
                {'cs': 5},
                {'clock': 25},
                {'address': 24},
                {'dataout': 23},
                {'rate': 10}
            ],
        ),

        Node(
            package='ros2_for_waveshare_alphabot2',  # replace with your actual package name
            executable='sound',  # replace with your actual executable name
            name='sound',
            output='screen',
            parameters=[
                {'~rate': 10}
            ],
        ),
    ])
