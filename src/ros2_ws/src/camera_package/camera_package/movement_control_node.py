import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Int32MultiArray
import time
import math

class MovementControl(Node):
    def __init__(self):
        super().__init__('movement_control')
        
        # parameters
        # camera angle
        self.max_winkel_x = (66 + 4)/2
        self.max_winkel_y = (48 + 2)/2
        # distance aproximation setings
        self.distance_to_person = 200
        self.hight_of_person = 170
        self.optimal_hight_percentage = self.determine_percentage_of_height()
        # default setings 
        self.enable_movement = False
        self.send_delay = 2
        self.send = 2

        #Folow me 
        self.subscription = self.create_subscription(
            Int32MultiArray,            #data type
            '/position_data',           #topic published by camera_opencv_node
            self.listener_callback,     #function to notify that a mesage was recived
            1)                          #queue size amount of the stored mesages  
        self.subscription
        self.Position = []

        #Joistick
        self.subscription = self.create_subscription(
            String,                     #data type
            '/joystick',                 #topic published by camera_opencv_node
            self.control,               #function to notify that a mesage was recived
            5)                          #queue size amount of the stored mesages  
        self.subscription

        # Servo
        self.servo_msg_hold = [0, 0]
        self.servo_pub = self.create_publisher(Int32MultiArray, '/servo', 1)
                

    def listener_callback(self, Position):
        
        self.coordinate_x = Position.data[0]
        self.coordinate_y = Position.data[1]
        self.lenght_x     = Position.data[2]
        self.lenght_y     = Position.data[3]
        self.max_x        = Position.data[4]
        self.max_y        = Position.data[5]
                
        # Winkelberechnung
        self.winkel_x = int((self.coordinate_x/self.max_x)*self.max_winkel_x)
        self.winkel_y = int((self.coordinate_y/self.max_y)*self.max_winkel_y)

        self.get_logger().info("Angle: [{}, {}]".format(self.winkel_x, self.winkel_y))

        if self.enable_movement:
            if self.winkel_x == 0 and self.winkel_y == 0:
                self.send = 0
            elif self.send < self.send_delay:                
                self.send += 1
            else:
                self.send = 0
            
            if self.send == self.send_delay:
                # channel 0 = pan 
		        # channel 1 = tilt

                self.servo_msg_hold[0] = self.servo_msg_hold[0] + self.winkel_x
                self.servo_msg_hold[1] = self.servo_msg_hold[1] + self.winkel_y

                self.get_logger().info("Data sent to Servo: {}".format(self.servo_msg_hold))

                servo_msg_sent = Int32MultiArray()
                servo_msg_sent.data = self.servo_msg_hold
                self.servo_pub.publish(servo_msg_sent)

        try:
            distance = self.aproximate_distance(self.lenght_y)
            self.get_logger().info("Distance to person : {}".format(distance))
        except:
            self.get_logger().info("unable to calculate Distance")

        time.sleep(0.2)

    def control(self, msg):
        #Joistick
        imput = msg.data
        self.get_logger().info("Joistick Imput recived: {}".format(imput))        
                
        if imput == "Center":
            # togle movement
            self.enable_movement = not self.enable_movement
            if self.enable_movement:
                self.get_logger().info("Movement enabled")
            else:
                self.get_logger().info("Movement diabled")

        elif imput == "Up":
            #center servo
            servo_msg_sent = Int32MultiArray()
            self.get_logger().info("Data sent to Servo: {}".format(self.servo_msg_hold))
            servo_msg_sent.data = [0, 0]
            self.servo_pub.publish(servo_msg_sent)
            time.sleep(1)
        # elif imput == "Right":
        #     #
        # elif imput == "Left":
        #     #
        # elif imput == "Down":
        #     #
    
    def determine_percentage_of_height(self):
        max_hight = round(self.distance_to_person * math.tan(math.radians(self.max_winkel_y)))
        return round((self.hight_of_person/max_hight) * 100)

    def aproximate_distance(self, lenght_y):
        hight_percentage = (lenght_y / self.max_y)
        return int((hight_percentage / self.optimal_hight_percentage) * self.distance_to_person)


def main(args=None):
    
    rclpy.init(args=args)
    movement_control = MovementControl()  # create node object
    rclpy.spin(movement_control)       # start node
    
    movement_control.destroy_node()    # destroy node
    rclpy.shutdown()


if __name__ == '__main__':
    main()
