import time
import rclpy
from geometry_msgs.msg import Twist
from ros2_for_waveshare_alphabot2.msg import PanTilt, IR, RGBLED
from std_msgs.msg import Float32

def main():
    rclpy.init()
    node = rclpy.create_node("test")

    # Message publishers
    pantilt_pub = node.create_publisher(PanTilt, 'pan_tilt', 4)
    rgb_pub = node.create_publisher(RGBLED, 'rgb_leds', 4)
    buzz_pub = node.create_publisher(Float32, 'buzzer', 4)
    move_pub = node.create_publisher(Twist, 'cmd_vel', 4)

    time.sleep(1)

    # Messages
    pantilt_msg = PanTilt()
    rgb_led_msg = RGBLED()

    # beep
    print('buzz......')
    buzz_pub.publish(Float32(data=0.5))

    # Flash LEDs
    print('Flashing LED\s')
    rgb_led_msg.function = 'theaterChaseRainbow'
    rgb_led_msg.delay = 50
    rgb_pub.publish(rgb_led_msg)

    # Centre
    print('Head Pan/Tilt - Centre')
    pantilt_msg.pan = 0.0
    pantilt_msg.tilt = 0.0
    pantilt_pub.publish(pantilt_msg)
    time.sleep(1.0)

    #  Head Up/Right
    print('Head Pan/Tilt - Look Up and Right')
    pantilt_msg.pan = 1.0
    pantilt_msg.tilt = 1.0
    pantilt_pub.publish(pantilt_msg)
    time.sleep(1.0)

    #  Head Down/Left
    print('Head Pan/Tilt - Look Down and Left')
    pantilt_msg.pan = -1.0
    pantilt_msg.tilt = -1.0
    pantilt_pub.publish(pantilt_msg)
    time.sleep(1.0)

    # Centre
    print('Head Pan/Tilt - Centre')
    pantilt_msg.pan = 0.0
    pantilt_msg.tilt = 0.0
    pantilt_pub.publish(pantilt_msg)
    time.sleep(1.0)

    # beep
    print('buzz......')
    buzz_pub.publish(Float32(data=0.5))

    # Now we're going to move the robot
    print('Moving forward for 0.5 seconds')
    move_msg = Twist()
    move_msg.linear.x = 0.5
    move_pub.publish(move_msg)
    time.sleep(1.0)

    print('Moving backward for 0.5 seconds')
    move_msg = Twist()
    move_msg.linear.x = -0.5
    move_pub.publish(move_msg)
    time.sleep(1.0)

    print('Turning robot right for 0.5 seconds')
    move_msg = Twist()
    move_msg.linear.x = 0.0
    move_msg.angular.z = 0.5
    move_pub.publish(move_msg)
    time.sleep(1.0)

    print('Turning robot left for 0.5 seconds')
    move_msg = Twist()
    move_msg.angular.z = -0.5
    move_pub.publish(move_msg)
    time.sleep(1.0)

    # beep
    print('buzz......')
    buzz_pub.publish(Float32(data=0.5))

    print('Turning robot left for 0.5 seconds')
    move_msg = Twist()
    move_msg.angular.z = 0.0
    move_pub.publish(move_msg)
    time.sleep(0.5)

    # beep
    print('buzz......')
    buzz_pub.publish(Float32(data=0.5))

    # Turn LED's Off
    print('LED\'s Off')
    rgb_led_msg.function = 'setLED'
    rgb_led_msg.led1_color = '000000'
    rgb_led_msg.led2_color = '000000'
    rgb_led_msg.led3_color = '000000'
    rgb_led_msg.led4_color = '000000'
    rgb_led_msg.delay = 50
    rgb_pub.publish(rgb_led_msg)

    rclpy.shutdown()

if __name__ == '__main__':
    main()
