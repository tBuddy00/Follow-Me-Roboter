#!/usr/bin/env python

import rclpy
from rclpy.node import Node
from std_msgs.msg import Header
from geometry_msgs.msg import TransformStamped
from ros2_for_waveshare_alphabot2.msg import PanTilt

import time
import math
import smbus
import tf2_ros
import tf2_geometry_msgs
from tf2_ros import TransformBroadcaster

# Camera Pan
# Camera Tilt


class PCA9685:
		
	# Registers/etc.
	__SUBADR1		= 0x02
	__SUBADR2		= 0x03
	__SUBADR3		= 0x04
	__MODE1			= 0x00
	__PRESCALE		= 0xFE
	__LED0_ON_L		= 0x06
	__LED0_ON_H		= 0x07
	__LED0_OFF_L	= 0x08
	__LED0_OFF_H	= 0x09
	__ALLLED_ON_L	= 0xFA
	__ALLLED_ON_H	= 0xFB
	__ALLLED_OFF_L	= 0xFC
	__ALLLED_OFF_H	= 0xFD


	def __init__(self, address=0x40, debug=False):
		self.get_logger().info("Node 'camera_pan_tilt' configuring PCA9685")

		self.bus = smbus.SMBus(1)
		self.address = address
		self.debug = debug
		self.get_logger().info("Node 'camera_pan_tilt' Reseting PCA9685")
		self.write(self.__MODE1, 0x00)
		self.get_logger().info("Node 'camera_pan_tilt' PCA9685 configured")
		
	def write(self, reg, value):
		self.bus.write_byte_data(self.address, reg, value)
			
	def read(self, reg):
		# Read an unsigned byte from the I2C device
		result = self.bus.read_byte_data(self.address, reg)
		return result
		
	def setPWMFreq(self, freq):
		# Sets the PWM frequency
		prescaleval = 25000000.0		# 25MHz
		prescaleval /= 4096.0			 # 12-bit
		prescaleval /= float(freq)
		prescaleval -= 1.0
		prescale = math.floor(prescaleval + 0.5)

		oldmode = self.read(self.__MODE1)
		newmode = (oldmode & 0x7F) | 0x10				# sleep
		self.write(self.__MODE1, newmode)				# go to sleep
		self.write(self.__PRESCALE, int(math.floor(prescale)))
		self.write(self.__MODE1, oldmode)
		time.sleep(0.005)
		self.write(self.__MODE1, oldmode | 0x80)

	def setPWM(self, channel, on, off):
		# Sets a single PWM channel
		self.write(self.__LED0_ON_L+4*channel, on & 0xFF)
		self.write(self.__LED0_ON_H+4*channel, on >> 8)
		self.write(self.__LED0_OFF_L+4*channel, off & 0xFF)
		self.write(self.__LED0_OFF_H+4*channel, off >> 8)
			
	def setServoPulse(self, channel, pulse):
		# Sets the Servo Pulse,The PWM frequency must be 50HZ
		pulse = pulse*4096/20000				#PWM frequency is 50HZ,the period is 20000us
		self.setPWM(channel, 0, pulse)

	def __del__(self):
		self.write(self.__MODE1, 0x00)

class CameraPanTiltDriver(Node):

    def __init__(self):
        super().__init__('camera_pan_tilt_driver')
        self.get_logger().info("Node 'camera_pan_tilt' configuring driver")

        self.rate = self.create_rate(self.get_parameter('rate').get_parameter_value().integer_value, 'camera_pan_tilt_driver')

        self.pwm = PCA9685(0x40)
        self.pwm.setPWMFreq(50)

        self.pan_offset = self.get_parameter('pan_offset').get_parameter_value().double_value
        self.tilt_offset = self.get_parameter('tilt_offset').get_parameter_value().double_value
        self.pan_limit_left = self.get_parameter('pan_limit_left').get_parameter_value().double_value
        self.pan_limit_right = self.get_parameter('pan_limit_right').get_parameter_value().double_value
        self.tilt_limit_up = self.get_parameter('tilt_limit_up').get_parameter_value().double_value
        self.tilt_limit_down = self.get_parameter('tilt_limit_down').get_parameter_value().double_value

        self.get_logger().info(f"Node 'camera_pan_tilt' pan_offset = {self.pan_offset}.")
        self.get_logger().info(f"Node 'camera_pan_tilt' tilt_offset = {self.tilt_offset}.")
        self.get_logger().info(f"Node 'camera_pan_tilt' pan_limit_left = {self.pan_limit_left}.")
        self.get_logger().info(f"Node 'camera_pan_tilt' pan_limit_right = {self.pan_limit_right}.")
        self.get_logger().info(f"Node 'camera_pan_tilt' tilt_limit_up = {self.tilt_limit_up}.")
        self.get_logger().info(f"Node 'camera_pan_tilt' tilt_limit_down = {self.tilt_limit_down}.")

        # Center servos
        self.pan_center_pulse = int(-self.pan_offset * (1000 / (math.pi / 2)) + 1500)
        self.tilt_center_pulse = int(-self.tilt_offset * (1000 / (math.pi / 2)) + 1500)

        self.HPulse = self.pan_center_pulse
        self.VPulse = self.tilt_center_pulse

        self.pwm.setServoPulse(0, self.HPulse)
        self.pwm.setServoPulse(1, self.VPulse)

        self.subscription = self.create_subscription(PanTilt, 'pan_tilt', self.pan_tilt_callback, 10)

        self.tf_broadcaster = TransformBroadcaster(self)

	
    def run(self):
        self.get_logger().info("Node 'pan_tilt' running.")

        while rclpy.ok():
            # Send Pan tf
            self.tf_broadcaster.sendTransform(
                (0.0, 0.0, 0.0),
                tf2_geometry_msgs.transformations.quaternion_from_euler(0.0, 0.0, self.pan),
                self.get_clock().now().to_msg(),
                "servoPan",
                "servoPanNeck"
            )

            # Send Tilt tf
            self.tf_broadcaster.sendTransform(
                (0.0, 0.0, 0.0),
                tf2_geometry_msgs.transformations.quaternion_from_euler(0.0, self.tilt, 0.0),
                self.get_clock().now().to_msg(),
                "servoTilt",
                "servoPan"
            )

            self.rate.sleep()

    def pan_tilt_callback(self, message):
        self.get_logger().info("Node 'camera_pan_tilt' message received.")

        # limit the servo pan
        self.pan = min(message.pan, self.pan_limit_left) if message.pan >= 0 else max(message.pan, -self.pan_limit_right)

        # Limit the servo tilt
        self.tilt = min(message.tilt, self.tilt_limit_up) if message.tilt >= 0 else max(message.tilt, -self.tilt_limit_down)

        self.get_logger().info(f"Node 'camera_pan_tilt' Pan = {self.pan}.")
        self.get_logger().info(f"Node 'camera_pan_tilt' Tilt = {self.tilt}.")

        # Convert from radians to pulses (500 - 2500)
        self.HPulse = int(self.pan * (1000 / (math.pi / 2)) + self.pan_center_pulse)
        self.VPulse = int(self.tilt * (1000 / (math.pi / 2)) + self.tilt_center_pulse)

        self.pwm.setServoPulse(1, self.VPulse)
        self.pwm.setServoPulse(0, self.HPulse)


def main(args=None):
    rclpy.init(args=args)
    driver = CameraPanTiltDriver()
    driver.run()
    rclpy.shutdown()


if __name__ == '__main__':
	main()
