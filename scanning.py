import pigpio

import lib_scanner

pi = pigpio.pi()

"""
.. warning::

    Make sure that the ``min_pw`` and ``max_pw`` values are carefully tested
    **before** using this example, see **Warning** in 
    :class:`lib_scanner.para_standard_servo` . The passed values ``min_pw`` 
    and ``max_pw`` for the created ranger object are just valid for the 
    demo implementation!
"""

ranger = lib_scanner.scanner(pi = pi, min_pw=600, max_pw=2350)

distances = ranger.read_all_angles()
print(distances)

#http://abyz.me.uk/rpi/pigpio/python.html#callback
ranger.cancel()

#http://abyz.me.uk/rpi/pigpio/python.html#stop
pi.stop()