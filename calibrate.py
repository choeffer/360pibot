import time

import pigpio

import lib_para_360_servo

#define GPIO for each servo to read from
gpio_l_r = 16
gpio_r_r = 20

#define GPIO for each servo to write to
gpio_l_w = 17
gpio_r_w = 27

pi = pigpio.pi()

#### Calibrate servos, speed  = 0.2 and -0.2
#chose gpio_l_w/gpio_l_r (left wheel), or accordingly gpio_r_w/gpio_r_r (right wheel)

servo = lib_para_360_servo.write_pwm(pi = pi, gpio = gpio_r_w, 
    min_pw = 1280, max_pw = 1720)
#buffer time for initializing everything
time.sleep(1)
servo.set_speed(0.2)
wheel = lib_para_360_servo.calibrate_pwm(pi = pi, gpio = gpio_r_r)
servo.set_speed(0)

#http://abyz.me.uk/rpi/pigpio/python.html#stop
pi.stop()