import time

import pigpio

import lib_scanner

pi = pigpio.pi()

servo = lib_scanner.para_standard_servo(pi = pi, gpio = 22)

servo.middle_position()
time.sleep(2)
servo.max_right()
time.sleep(2)
servo.max_left()
time.sleep(2)
servo.set_position(degree = 45)

#http://abyz.me.uk/rpi/pigpio/python.html#stop
pi.stop()