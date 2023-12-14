import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import Int32MultiArray
from cv_bridge import CvBridge
import cv2
import time

from opencv import human_detector


class CameraOpencv(Node):
    def __init__(self):
        super().__init__('camera_subscriber')
        #create the subscriber 
        self.subscription = self.create_subscription(
            Image,                      #data type
            '/image_raw',               #topic published by v4l2_camera_node
            self.listener_callback,     #function to notify that a mesage was recived
            1)                          #queue size amount of the stored mesages  
        self.subscription               # prevent unused variable warning
        self.publisher_ = self.create_publisher(Int32MultiArray, '/position_data', 1)
        self.image_publisher = self.create_publisher(Image, '/opencv_image', 1)
        self.bridge = CvBridge()

        self.detector = human_detector.HumanDetector()


    def listener_callback(self, msg):
                
        self.get_logger().info('Image recived')      #consoll output to confirm that a mesage was recived 
        
        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")      #converts the ros image topic into the opencv image format
        except CvBridgeError as e:
            print(e)
        
        try:
            value = self.detector.locate_person(cv_image)       # run opencv skript
            Position, return_image = value

            return_image_msg = self.bridge.cv2_to_imgmsg(return_image, "bgr8")    # Image Streamer
            self.image_publisher.publish(return_image_msg)
        except:
            self.get_logger().info('no Position data recived')

        if Position != []:
            self.get_logger().info('Position data recived {}'.format(Position))
            position_data = Int32MultiArray()
            position_data.data = Position
            self.publisher_.publish(position_data)
            
        time.sleep(0.2)


def main(args=None):
    
    rclpy.init(args=args)
    camera_subscriber = CameraOpencv()  # create node object
    rclpy.spin(camera_subscriber)       # start node 

    camera_subscriber.destroy_node()    # destroy node
    rclpy.shutdown()


if __name__ == '__main__':
    main()
