import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

import RPi.GPIO as GPIO
import time

BUZ = 4

class SoundDriver(Node):
    def __init__(self):
        super().__init__('sound_driver')
        self.loginfo("Node 'sound' configuring driver.")

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(BUZ, GPIO.OUT)

        self.rate = self.create_rate(self.get_parameter_or('~rate', 10))

        # Setup subscriber for buzzer message
        self.create_subscription(Float32, 'buzzer', self.buzzer_callback, 10)

        self.loginfo("Node 'sound' configuration complete.")

    def __del__(self):
        GPIO.cleanup()

    def run(self):
        self.loginfo("Node 'sound' running.")
        while rclpy.ok():
            rclpy.spin_once(self)
            self.rate.sleep()

    # Beep for duration seconds
    def buzzer_callback(self, message):
        self.loginfo("Node 'sound' beeping for " + str(message.data) + " seconds.")
        GPIO.output(BUZ, GPIO.HIGH)
        time.sleep(message.data)
        GPIO.output(BUZ, GPIO.LOW)

def main():
    rclpy.init()
    node = SoundDriver()
    node.run()
    rclpy.shutdown()
    print("Node 'sound' Stopped")

if __name__ == '__main__':
    main()