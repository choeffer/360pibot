Python 3 implementation for programming an ActivityBot 360° Robot Kit 360_kit_ with
a Raspberry Pi. The modules of the implementation are using the pigpio_ module 
to control the GPIOs of the Raspberry Pi. No other external module is needed.

The Documentation_ is hosted on `Read the Docs`_ .

The modules also enable remote controling the robots GPIOs. This enables 
executing the scripts on a laptop/computer and over e.g. WLAN remote controling the Raspberry Pi 
which provides a WLAN Hotspot, see remote_pin_ and pi_hotspot_ . So, the robot can freely
move with a powerbank attached and does not have to be connected to a monitor, keyboard 
and mouse while controling/programming it. The possibillity of remote controling
the Raspberry Pis GPIOs is a big advantage of the used pigpio_ module. It is also possible to execute
the scripts on the Raspberry Pi itself and connect to it over VNC, see VNC_ . For both ways, 
executing the code on the Raspberry Pi itself or remote on a laptop/computer to control
the GPIOs, no modifications have to be made in the source code, it works in both cases.

References
----------

.. target-notes::

.. _pi_hotspot: https://www.raspberrypi.org/documentation/configuration/wireless/access-point.md
.. _remote_pin : http://gpiozero.readthedocs.io/en/stable/remote_gpio.html
.. _360_kit: https://www.parallax.com/product/32600
.. _pigpio: https://pypi.org/project/pigpio/
.. _VNC: https://www.raspberrypi.org/documentation/remote-access/vnc/
.. _Documentation: https://360pibot.readthedocs.io/
.. _`Read the Docs`: https://readthedocs.org/
