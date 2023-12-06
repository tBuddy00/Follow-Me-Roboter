#!/usr/bin/env python

import socket
import rclpy
from rclpy.node import Node
from ros2_for_waveshare_alphabot2.msg import IR

LIRCPATH = "/var/run/lirc/lircd"

class IRDriver(Node):

    def __init__(self):
        super().__init__('ir_control')
        
        self.get_logger().info("Node 'ir_control' configuring driver.")
        
        self.rate = self.create_rate(self.get_parameter_or('~rate', 10))

        try:
            self.lirc_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            self.lirc_socket.connect(LIRCPATH)

            self.get_logger().info("Node 'ir_control' lirc connection established.")
            
            # Setup publisher for ir_remote
            self.pub = self.create_publisher(IR, 'ir_remote', 4)

            self.get_logger().info("Node 'ir_driver' configured.")
            
        except AssertionError as error:
            
            self.get_logger().info("Node 'ir_control' ERROR: lirc connection failed. ")
            
            raise RuntimeError(error)

    def run(self):
        self.get_logger().info("Node 'ir_control' running.")
        
        while rclpy.ok():
            data = self.lirc_socket.recv(128)
            data = data.strip()
            if data:
                words = data.split()
                key_name = words[2]
                count_pressed = int(words[1], 16)
                ir_message = IR()
                ir_message.key_name = key_name
                ir_message.count_pressed = count_pressed

                self.pub.publish(ir_message)
                self.get_logger().info("Node 'ir_control' received key " + str(words[2]) + " (" + str(count_pressed) + ").")

            self.rate.sleep()

def main():
    rclpy.init()
    try:
        rclpy.spin(IRDriver())
    finally:
        rclpy.shutdown()

if __name__ == '__main__':
    main()
