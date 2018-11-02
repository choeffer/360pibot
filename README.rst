360pibot
========

Python 3 implementation for programming an ActivityBot 360° Robot Kit 360_kit_ with
a Raspberry Pi. The modules of the implementation are using the pigpio_ module 
to control the GPIOs of the Raspberry Pi. No other external module is needed.

About
-----

At the moment, the following functions are implemented:

* Turning on the spot
* Moving straight - forward and backward
* Scanning the surrounding with an ultrasonic sensor mounted on a servo

The turning and straight movements are controlled by four digital PID 
controllers. Each wheel is controlled by a cascade control, using 
a cascade of two PID controllers. The outer loops control the position 
while the inner loops control the speed of each wheel.

The modules provide simple APIs for turning and straight 
movements and also for scanning the surrounding or stearing a servo. Have a look 
at the Examples section of the documentation for some code examples.

Most of the default values in the modules are those which are used while 
experimenting/developing with the demo implementation. They provide a good starting 
point for the range of the values. Pictures of the demo implementation can be
found in the Introduction section of the documentation.

The modules also enable remote controlling the Raspberry Pis GPIOs. This enables 
use of the modules on a laptop/computer and over e.g. WLAN remote controlling the Raspberry Pi 
which provides a WLAN Hotspot, see remote_pin_ and pi_hotspot_ . So, the robot can freely
move with a powerbank attached without any peripheral devices while controlling/programming it. 
The possibillity of remote controlling the Raspberry Pis GPIOs is a big advantage of the 
used pigpio_ module. It is also possible to use the modules on the Raspberry Pi itself 
and connect to it over VNC, see VNC_ . For both ways, using the modules on the Raspberry 
Pi itself or remote on a laptop/computer to control the Raspberry Pis GPIOs, no 
modifications have to be done in the source code of the modules.

The documentation is made with Sphinx_ and can be extended or modified as needed for 
e.g. documenting own projects based on this or if extending functionality of the modules 
and documenting this. The whole documentation is stored in the ``docs/`` folder 
of the git repository.

Instead of buying an ActivityBot 360° Robot Kit 360_kit_ it is sufficient to buy 
two Parallax Feedback 360° High-Speed Servos `360_data_sheet`_ , two robot wheels 
`wheel_robot`_, one Parallax Standard Servo `stand_data_sheet`_ and a `HC-SR04`_ 
ultrasonic sensor to build your own chassi/robot.

Documentation
-------------

The documentation is hosted on `Read the Docs`_ and is 
available at https://360pibot.readthedocs.io/ .

References
----------

.. target-notes::

.. _pi_hotspot: https://www.raspberrypi.org/documentation/configuration/wireless/access-point.md
.. _remote_pin : http://gpiozero.readthedocs.io/en/stable/remote_gpio.html
.. _360_kit: https://www.parallax.com/product/32600
.. _`360_data_sheet`: https://www.parallax.com/sites/default/files/downloads/900-00360-Feedback-360-HS-Servo-v1.1.pdf
.. _`stand_data_sheet`: https://www.parallax.com/sites/default/files/downloads/900-00005-Standard-Servo-Product-Documentation-v2.2.pdf
.. _`HC-SR04`: https://cdn.sparkfun.com/assets/b/3/0/b/a/DGCH-RED_datasheet.pdf
.. _`wheel_robot`: https://www.parallax.com/product/28114
.. _pigpio: https://pypi.org/project/pigpio/
.. _VNC: https://www.raspberrypi.org/documentation/remote-access/vnc/
.. _Sphinx: https://www.sphinx-doc.org/
.. _`Read the Docs`: https://readthedocs.org/
