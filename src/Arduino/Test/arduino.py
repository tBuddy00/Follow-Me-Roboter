import serial
import serial.tools.list_ports
import time
from calculate_movement import calculate_movement_variable_time 

class Serial_Arduino():
    def __init__(self, serial_port= "COM3"):
        # Define the serial port and baud rate
        # self.serial_port = self.find_arduino_port()  # Change this to the appropriate port on your system
        self.find_arduino_port()
        self.serial_port = serial_port
        baud_rate = 9600
        self.ser = serial.Serial(self.serial_port, baud_rate, timeout=1)
        time.sleep(2)
        self.ser.flush()

    def find_arduino_port(self):
        # Check the operating system
        ports = list(serial.tools.list_ports.comports())

        for p in ports:
            print(p)
            if "Arduino" in p.description:
                print('Arduino found on port: {}'.format(p.device))
                return p.device

        # Return None if no Arduino is found
        print('Arduino not found')
        return None

    def write(self, data):
        self.ser.write(data.encode())
        self.ser.flush()
        # self.ser.write(str(data))

    def read(self):
        return self.ser.readline()


def run(ser, base_rpm, angle, move = False):
    speed_right, speed_left, time_out = calculate_movement_variable_time(base_rpm, angle, move)
    
    if move and angle == 0:
        time_override = int(input("Enter time override: "))
        speed_time = time_override
    else:
        speed_time = int(time_out * 1000)
    
    speed_right_after = 0
    speed_left_after = 0

    serial_data = "{},{},{},{},{}\n".format(speed_right, speed_left, speed_time, speed_right_after, speed_left_after)

    print(serial_data)
    ser.write(serial_data)

    time.sleep(0.5)
    response = ser.read()
    print(response)
    return speed_right, speed_left, time_out


def setup():

    try:
        ser = Serial_Arduino("COM4")

        while True:
            base_rpm = int(input("Enter base RPM: "))
            angle = int(input("Enter angle: "))
            move = input("Move? (y/n): ")
            if move == "y":
                move = True
            else:
                move = False

            run(ser, base_rpm, angle, move)

            if input("Continue? (y/n): ") != "y":
                break
    except:
        print("Serial port not available. Exiting...")


setup()


