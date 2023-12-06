import rclpy
from rclpy.node import Node
import time
from sensor_msgs.msg import Image
from std_msgs.msg import String, Int32MultiArray, Float32
from geometry_msgs.msg import Twist

from ros2_for_waveshare_alphabot2.msg import PanTilt, IR, RGBLED


class MovementControl(Node):
    def __init__(self):
        super().__init__('movement_control')
        #create the subscriber 
        self.subscription = self.create_subscription(
            Int32MultiArray,            #data type
            '/position_data',           #topic published by camera_opencv_node
            self.listener_callback,     #function to notify that a mesage was recived
            5)                          #queue size amount of the stored mesages  
        self.subscription

        # Message publishers
        self.pantilt_pub = self.create_publisher(PanTilt, 'pan_tilt', 4)
        self.rgb_pub = self.create_publisher(RGBLED, 'rgb_leds', 4)
        self.buzz_pub = self.create_publisher(Float32, 'buzzer', 4)
        self.move_pub = self.create_publisher(Twist, 'cmd_vel', 4)

        # variables
        self.Position = []

        # parameter
        self.pan_factor = self.get_parameter_or('pan_factor', 1)
        self.tilt_factor = self.get_parameter_or('tilt_factor', 1)


    def listener_callback(self, msg):
        # Messages
        pantilt_msg = PanTilt()
        rgb_led_msg = RGBLED()        
        
        self.get_logger().info('Position recived')      #consoll output to confirm that a mesage was recived 
        self.Position.append(msg.data)         #save recived msg in a array

        self.coordinate_x = self.Position[1]
        self.coordinate_y = self.Position[2]
        self.lenght_x     = self.Position[3]
        self.lenght_y     = self.Position[4]
        self.max_x        = self.Position[5]
        self.max_y        = self.Position[6]
        
        self.calculate()

        pantilt_msg.pan = self.percetage_x
        pantilt_msg.tilt = self.percetage_y
        self.pantilt_pub.publish(pantilt_msg)
        time.sleep(0.2)



    def calculate(self):
        self.center_x = (self.coordinate_x - (self.lenght_x/2))
        self.center_y = (self.coordinate_y - (self.lenght_y/2))

        if (self.max_x > self.max_y):
            max = self.max_x
        else:
            max = self.max_y

        self.percetage_x = ((self.center_x/max)*self.pan_factor)
        self.percetage_y = ((self.center_y/max)*self.tilt_factor)



    


def main(args=None):
    

    rclpy.init(args=args)
    movement_control = MovementControl()
    rclpy.spin(movement_control)    

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    movement_control.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
