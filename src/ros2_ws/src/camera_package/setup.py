from setuptools import find_packages, setup

package_name = 'camera_package'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Claire Schubert',
    maintainer_email='ubuntu@todo.todo',
    description='Camera Subscriber for the topic /image_raw form the v4l2_camera_node',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'camera_test = camera_package.camera_subscriber_test:main',
            'camera_opencv = camera_package.camera_opencv_node:main',
            'movement_control = camera_package.movement_control_node:main',
        ],
    },
)
