import pigpio

import lib_scanner

pi = pigpio.pi()
ranger = lib_scanner.scanner(pi = pi)
distances = ranger.read_all_angles()
print(distances)

#http://abyz.me.uk/rpi/pigpio/python.html#callback
ranger.cancel()

#http://abyz.me.uk/rpi/pigpio/python.html#stop
pi.stop()