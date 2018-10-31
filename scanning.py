import pigpio

import lib_scanner

pi = pigpio.pi()

"""
.. warning::

    Make sure that the ``min_pw`` and ``max_pw`` values are carefully tested
    **before** using this example, see **warning** in 
    :class:`lib_scanner.para_standard_servo`! The default values for the 
    created ranger object are just valid for the demo implementation!
"""

ranger = lib_scanner.scanner(pi = pi)

distances = ranger.read_all_angles()
print(distances)

#http://abyz.me.uk/rpi/pigpio/python.html#callback
ranger.cancel()

#http://abyz.me.uk/rpi/pigpio/python.html#stop
pi.stop()