import pigpio

import lib_motion
import lib_scanner

#initialize one pigpio.pi() instance to be used by all lib_*
pi = pigpio.pi()

robot = lib_motion.control(pi = pi)

"""
.. warning::

    Make sure that the ``min_pw`` and ``max_pw`` values are carefully tested
    **before** using this example, see **Warning** in 
    :class:`lib_scanner.para_standard_servo` . The passed values ``min_pw`` 
    and ``max_pw`` for the created ranger object are just valid for the 
    demo implementation!
"""

ranger = lib_scanner.scanner(pi = pi, min_pw=600, max_pw=2350)

while True:

    distances = ranger.read_all_angles()
    list_dist = list(distances.values())
    if any(t<0.4 for t in list_dist):
        robot.turn(45)
    else:
        robot.straight(200)

#http://abyz.me.uk/rpi/pigpio/python.html#callback
robot.cancel()
ranger.cancel()

#http://abyz.me.uk/rpi/pigpio/python.html#stop
pi.stop()
