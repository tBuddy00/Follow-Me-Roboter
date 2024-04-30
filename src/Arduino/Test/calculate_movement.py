import math
import time
import datetime


def calculate_speed_variable_time(base_rpm, radius, angle, wheel_distance, wheel_radius, correction_factor):    
    
    #base_rpm rpm
    #radius cm
    #angle °
    #wheel_distance cm
    #wheel_radius cm
    #base_speed cm/s

    base_speed = ((2 * math.pi * wheel_radius) / 60) * base_rpm

    if angle < 0:
        angle = -angle
        switch = True
    else:
        switch = False
    
    distance_in = (2 * math.pi * (radius) * (angle / 360))
    distance_out = (2 * math.pi * (radius + wheel_distance) * (angle / 360))

    time_out = distance_in / base_speed
    
    if distance_out == 0:
        rpm_out = base_rpm
        time_out = 1
    else:
        rpm_out = distance_out / time_out / (0.1047 * wheel_radius)
    rpm_in = base_rpm
    # print("rpm_out:", int(rpm_out), "rpm_in:", int(rpm_in), "time_out:", time_out)

    time_out = time_out * correction_factor
    
    if switch:
        return rpm_in, rpm_out, time_out
    else:    
        return rpm_out, rpm_in, time_out


def calculate_movement_variable_time(base_rpm, angle, move = False):
    
    radius = 25
    wheel_distance = 10
    wheel_radius = 1.5
    correction_factor = 1

    if base_rpm > 0 and move == True:
        speed_out, speed_in, time_out = calculate_speed_variable_time(base_rpm, radius, angle, wheel_distance, wheel_radius, correction_factor)
        speed_right = speed_in
        speed_left = speed_out

    elif base_rpm < 0 and move == True:
        speed_out, speed_in, time_out = calculate_speed_variable_time(base_rpm, radius, angle, wheel_distance, wheel_radius, correction_factor)
        speed_right = speed_out
        speed_left = speed_in

    elif base_rpm != 0 and move == False:
        radius_2 = (wheel_distance / 2)
        wheel_distance_2 = -wheel_distance
        speed_out, speed_in, time_out = calculate_speed_variable_time(base_rpm, radius_2, angle, wheel_distance_2, wheel_radius, correction_factor)
        speed_right = -speed_in
        speed_left = -speed_out

    elif move == True:
        speed_right = base_rpm
        speed_left = base_rpm
        time_out = 1
    
    else:
        speed_right = 0
        speed_left = 0
        time_out = 0
    
    return int(speed_right), int(speed_left), time_out
