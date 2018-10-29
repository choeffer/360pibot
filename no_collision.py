import lib_scanner
import lib_motion
import pigpio
import time

#initialize one pigpio.pi() instance to be used by all lib_*
pi = pigpio.pi()

robot = lib_motion.motion(pi = pi)
ranger =lib_scanner.scanner(pi = pi)

while True:

    distances = ranger.read_all_angles()
    print(distances)
    list_dist = list(distances.values())
    if any(t<0.4 for t in list_dist):
        robot.turn(45)

    elif any(t>=0.4 for t in list_dist):
        robot.straight(200)

#http://abyz.me.uk/rpi/pigpio/python.html#callback
robot.cancel()
ranger.cancel()

#http://abyz.me.uk/rpi/pigpio/python.html#stop
pi.stop()
