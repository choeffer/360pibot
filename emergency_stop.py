import time

import pigpio

import lib_para_360_servo

#define GPIO for each servo to write to
gpio_l = 17
gpio_r = 27

pi = pigpio.pi()

servo_l = lib_para_360_servo.write_pwm(pi = pi, gpio = gpio_l)

servo_r = lib_para_360_servo.write_pwm(pi = pi, gpio = gpio_r)

#buffer time for initializing everything
time.sleep(1)

servo_l.set_speed(0)
servo_r.set_speed(0)

#http://abyz.me.uk/rpi/pigpio/python.html#stop
pi.stop()