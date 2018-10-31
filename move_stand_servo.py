import time

import pigpio

import lib_scanner

pi = pigpio.pi()

servo = lib_scanner.para_standard_servo(gpio = 22, pi = pi,
    min_pw = 600, max_pw = 2350)
    
servo.middle_position()
time.sleep(1)
servo.max_right()
time.sleep(1)
servo.max_left()
time.sleep(1)
servo.set_position(degree = 45)

#http://abyz.me.uk/rpi/pigpio/python.html#stop
pi.stop()