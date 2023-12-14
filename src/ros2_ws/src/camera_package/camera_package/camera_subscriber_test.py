import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class CameraSubscriberTest(Node):
    def __init__(self):
        super().__init__('camera_subscriber')
        #create the subscriber 
        self.subscription = self.create_subscription(
            Image,                      #data type
            '/image_raw',               #topic published by v4l2_camera_node
            self.listener_callback,     #function to notify that a mesage was recived
            5)                          #queue size amount of the stored mesages  
        self.subscription  # prevent unused variable warning
        self.bridge = CvBridge()
        self.count = 0

    def listener_callback(self, Image):
        self.get_logger().info('Image recived')     #consoll output to confirm that a mesage was recived 
        
        try:
            cv_image = self.bridge.imgmsg_to_cv2(Image, "bgr8")      #converts the ros image topic into the opencv image format
        except CvBridgeError as e:
            print(e)

        path = ("/home/ubuntu/image/image" + str(self.count) + ".jpg")
        self.count = self.count + 1
        
        cv2.imwrite(path, cv_image)    #saves the image in the image folder
 
    
   


def main(args=None):
    
    #setup für die berechnung

    rclpy.init(args=args)

    camera_subscriber = CameraSubscriberTest()

    rclpy.spin(camera_subscriber)

    

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    camera_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
