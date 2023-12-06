#!/usr/bin/env python

import rclpy
from std_msgs.msg import String
from ros2_for_waveshare_alphabot2.msg import RGBLED

import requests

class LedDriver:
    def __init__(self):
        self.server_address = "http://localhost/"
        self.server_port = "2812"

        self.node = rclpy.create_node("rgb_leds_driver")
        self.node.loginfo("Node 'rgb_leds' configuring driver.")

        self.rate = self.node.create_rate(self.node.get_parameter('~rate'), 'rgb_leds')
        self.server_address = self.node.get_parameter('~server_address')
        self.server_port = self.node.get_parameter('~server_port')

        # Setup subscriber for rgb_led message
        self.subscriber = self.node.create_subscription(
            RGBLED,
            'rgb_leds',
            self.rgbled_callback,
            10
        )

        self.node.loginfo("Node 'rgb_leds' configuration complete.")

    def run(self):
        self.node.loginfo("Node 'rgb_leds' running.")
        while rclpy.ok():
            rclpy.spin_once(self.node)
            self.rate.sleep()

    def rgbled_callback(self, message):
        self.node.loginfo("Node 'rgb_leds' RGB_DATA Received")
        self.node.loginfo("    RGB_LED_DATA: function: " + str(message.function) + ", color: " + str(message.color) \
                        + ", LED 1 color: " + str(message.led1_color) \
                        + ", LED 2 color: " + str(message.led2_color) \
                        + ", LED 3 color: " + str(message.led3_color) \
                        + ", LED 4 color: " + str(message.led4_color) \
                        + ", delay: " + str(message.delay))

        # Create command for service here and call RGB LED Service
        if message.function.lower().strip() == "setled":
            url = f"{self.server_address}:{self.server_port}/setLED/{message.led1_color}/{message.led2_color}/{message.led3_color}/{message.led4_color}/"
        elif message.function.lower().strip() == "setallred":
            url = f"{self.server_address}:{self.server_port}/setAllRed/"
        elif message.function.lower().strip() == "setallgreen":
            url = f"{self.server_address}:{self.server_port}/setAllGreen/"
        elif message.function.lower().strip() == "setallblue":
            url = f"{self.server_address}:{self.server_port}/setAllBlue/"
        elif message.function.lower().strip() == "rainbow":
            url = f"{self.server_address}:{self.server_port}/setMode/rainbow/{message.delay}/"
        elif message.function.lower().strip() == "theaterchaserainbow":
            url = f"{self.server_address}:{self.server_port}/setMode/theaterChaseRainbow/{message.delay}/"
        elif message.function.lower().strip() == "colorwipe" and message.delay > 0:
            url = f"{self.server_address}:{self.server_port}/setMode/colorWipe/{message.color}/{message.delay}/"
        elif message.function.lower().strip() == "colorwipe" and message.delay <= 0:
            url = f"{self.server_address}:{self.server_port}/setMode/colorWipe/{message.color}/0/"
        elif message.function.lower().strip() == "theaterchase" and message.delay > 0:
            url = f"{self.server_address}:{self.server_port}/setMode/theaterChase/{message.color}/{message.delay}/"
        elif message.function.lower().strip() == "theaterchase" and message.delay <= 0:
            url = f"{self.server_address}:{self.server_port}/setMode/theaterChase/{message.color}/0/"
        elif message.function.lower().strip() == "delay" and message.delay > 0:
            url = f"{self.server_address}:{self.server_port}/setDelay/{message.delay}/"
        else:
            url = f"{self.server_address}:{self.server_port}/"

        self.node.loginfo("Node 'rgb_leds' Request: " + url)

        response = requests.put(url)

        self.node.loginfo("Node 'rgb_leds' Response: " + str(response.status_code))


def main():
    rclpy.init()
    node = LedDriver()
    node.run()
    rclpy.shutdown()
    print("Node 'rgb_leds' Stopped")


if __name__ == '__main__':
    main()
