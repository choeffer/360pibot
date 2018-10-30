Python 3 implementation for programming an ActivityBot 360° Robot Kit 360_kit_ with
a Raspberry Pi. The modules of the implementation are using the pigpio_ module 
to control the GPIOs of the Raspberry Pi. No other external module is needed.

At the moment, the following functions are implemented.

* Turning on the spot.
* Moving straight forward and backward.
* Scanning the surrounding with an ultrasonic sensor mounted on a servo.

The turning and moving straight movement is controlled by four digital PID 
controllers. Each wheel is controlled by a cascade control, which means 
a cascade of two PID controllers. The outer loops are controlling the position, 
the inner loops are controlling the speed of each wheel.

The documentation is hosted on `Read the Docs`_ and is 
available at https://360pibot.readthedocs.io/ .

The modules also enable remote controlling the Raspberry Pis GPIOs. This enables 
use of the modules on a laptop/computer and over e.g. WLAN remote controlling the Raspberry Pi 
which provides a WLAN Hotspot, see remote_pin_ and pi_hotspot_ . So, the robot can freely
move with a powerbank attached and does not have to be connected to a monitor, keyboard 
and mouse while controlling/programming it. The possibillity of remote controlling
the Raspberry Pis GPIOs is a big advantage of the used pigpio_ module. It is also possible to 
use the modules on the Raspberry Pi itself and connect to it over VNC, see VNC_ . For both ways, 
using the modules on the Raspberry Pi itself or remote on a laptop/computer to control
the Raspberry Pis GPIOs, no modifications have to be made in the source code, they 
work in both cases.

References
----------

.. target-notes::

.. _pi_hotspot: https://www.raspberrypi.org/documentation/configuration/wireless/access-point.md
.. _remote_pin : http://gpiozero.readthedocs.io/en/stable/remote_gpio.html
.. _360_kit: https://www.parallax.com/product/32600
.. _pigpio: https://pypi.org/project/pigpio/
.. _VNC: https://www.raspberrypi.org/documentation/remote-access/vnc/
.. _`Read the Docs`: https://readthedocs.org/
