import serial
import serial.tools.list_ports
import time
from calculate_movement import calculate_movement_variable_time 
from arduino import setup, run, Serial_Arduino

def setup():
    try:
        ser = Serial_Arduino("COM5")

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

def test_movement_calculation():
    accuracy_outputs = []
    speed_right_outputs = []
    speed_left_outputs = []
    time_out_outputs = []
    base_rpm_measured_outputs = []
    angle_measured_outputs = []
    angle_outputs = []
    base_rpm_outputs = []
    i = 0
    
    num_tests = int(input("Enter the number of test runs: "))
    print(f"\n== Einzeltests")

    try:
        ser = Serial_Arduino("COM5")
        while i < num_tests:
            i += 1
            base_rpm = int(input("\nEnter base RPM: "))
            angle = int(input("\nEnter angle: "))
            move = input("\nMove? (y/n): ")
            if move == "y":
                move = True
            else:
                move = False

            speed_right, speed_left, time_out = run(ser, base_rpm, angle, move)
            # speed_right, speed_left, time_out = calculate_movement_variable_time(base_rpm, angle, move)
            angle_measured = int(input("\nEnter measured angle: "))

            accuracy = (angle_measured - angle) / angle * 100

            accuracy_outputs.append(accuracy)
            speed_right_outputs.append(speed_right)
            speed_left_outputs.append(speed_left)
            time_out_outputs.append(time_out)
            angle_measured_outputs.append(angle_measured)
            angle_outputs.append(angle)
            base_rpm_outputs.append(base_rpm)

            # Ausgabe für jeden Test
            print(f"\n=== Test {i + 1}")
            print("\n==== Eingegebene Werte:")
            print(f"  Base RPM: {base_rpm}")
            print(f"  Angle: {angle}")

            print("\n==== Gemessene Werte:")
            print(f"  Measured Angle: {angle_measured}")

            print("\n==== Berechnete Werte:")
            print(f"  Time Out: {time_out}")
            print(f"  Speed Right: {speed_right}")
            print(f"  Speed Left: {speed_left}")

            print("\n==== Deviation from entered to measured angle:")
            print(f"  {accuracy:.2f}%")

    except:
        print("Serial port not available. Exiting...")

    

    # Gesamtauswertung
    total_accuracy_output = sum(accuracy_outputs)
    average_accuracy_output = total_accuracy_output / num_tests
    print("\n== Gesamtauswertung:")
    print(f"\n=== Tests performed: {num_tests}")
    print(f"\n=== Average Deviation: {average_accuracy_output:.2f}%")

test_movement_calculation()
