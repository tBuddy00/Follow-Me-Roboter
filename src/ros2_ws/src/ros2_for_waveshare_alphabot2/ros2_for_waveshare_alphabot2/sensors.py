import rclpy
from rclpy.node import Node
from std_msgs.msg import Header, Int16
from ros2_for_waveshare_alphabot2.msg import ObstacleStamped, LineFollowStamped, LineFollow

import RPi.GPIO as GPIO
import time

class SensorDriver(Node):
    def __init__(self, dr=16, dl=19, cs=5, clock=25, address=24, dataout=23):
        super().__init__('sensor_driver')
        self.loginfo("Node 'sensors' configuring driver.")

        self.numSensors = 5
        self.DR = dr
        self.DL = dl
        self.CS = cs
        self.Clock = clock
        self.Address = address
        self.DataOut = dataout

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        GPIO.setup(self.DR, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(self.DL, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(self.Clock, GPIO.OUT)
        GPIO.setup(self.Address, GPIO.OUT)
        GPIO.setup(self.CS, GPIO.OUT)
        GPIO.setup(self.DataOut, GPIO.IN, GPIO.PUD_UP)

        self.rate = self.create_rate(self.get_parameter_or('~rate', 10))

        # Setup publisher for obstacle detection
        self.pub_right = self.create_publisher(ObstacleStamped, 'obstacle_right', 4)
        self.pub_left = self.create_publisher(ObstacleStamped, 'obstacle_left', 4)

        # Setup publisher for the line following sensor
        self.pub_line_follow = self.create_publisher(LineFollowStamped, 'line_follow', 4)

        self.loginfo("Node 'sensors' configuration complete.")

    def __del__(self):
        GPIO.cleanup()

    def run(self):
        DR_status = False
        DL_status = False

        self.loginfo("Node 'sensors' running.")

        while rclpy.ok():
            DR_status = not bool(GPIO.input(self.DR))
            DL_status = not bool(GPIO.input(self.DL))

            DR_message = ObstacleStamped()
            DR_message.header.stamp = self.get_clock().now().to_msg()
            DR_message.obstacle = DR_status

            DL_message = ObstacleStamped()
            DL_message.header.stamp = self.get_clock().now().to_msg()
            DL_message.obstacle = DL_status

            self.pub_right.publish(DR_message)
            self.pub_left.publish(DL_message)

            line_follow_value = self.analog_read()

            line_follow_msg = LineFollow()
            line_follow_msg.left_outer = line_follow_value[0]
            line_follow_msg.left_inner = line_follow_value[1]
            line_follow_msg.centre = line_follow_value[2]
            line_follow_msg.right_inner = line_follow_value[3]
            line_follow_msg.right_outer = line_follow_value[4]

            line_follow_stamped_msg = LineFollowStamped()
            header = Header()
            header.stamp = self.get_clock().now().to_msg()
            line_follow_stamped_msg.header = header
            line_follow_stamped_msg.sensors = line_follow_msg

            self.pub_line_follow.publish(line_follow_stamped_msg)

            self.rate.sleep()

    def analog_read(self):
        value = [0] * (self.numSensors + 1)
        for j in range(0, self.numSensors + 1):
            GPIO.output(self.CS, GPIO.LOW)
            for i in range(0, 4):
                if (((j) >> (3 - i)) & 0x01):
                    GPIO.output(self.Address, GPIO.HIGH)
                else:
                    GPIO.output(self.Address, GPIO.LOW)
                value[j] <<= 1
                if GPIO.input(self.DataOut):
                    value[j] |= 0x01
                GPIO.output(self.Clock, GPIO.HIGH)
                GPIO.output(self.Clock, GPIO.LOW)
            for i in range(0, 6):
                value[j] <<= 1
                if GPIO.input(self.DataOut):
                    value[j] |= 0x01
                GPIO.output(self.Clock, GPIO.HIGH)
                GPIO.output(self.Clock, GPIO.LOW)
            time.sleep(0.0001)
            GPIO.output(self.CS, GPIO.HIGH)
        return value[1:]


def main():
    rclpy.init()
    node = SensorDriver()
    node.run()
    rclpy.shutdown()
    print("Node 'sensors' Stopped")


if __name__ == '__main__':
    main()
