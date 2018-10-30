.. _Introduction:

Introduction
============

Python 3 implementation for programming an ActivityBot 360° Robot Kit 360_kit_ with
a Raspberry Pi. The modules (see :ref:`360pibot_Python_API` ) of the implementation are using the pigpio_ module 
to control the GPIOs of the Raspberry Pi. No other external module is needed.

At the moment, the following functions are implemented:

* Turning on the spot.
* Moving straight forward and backward.
* Scanning the surrounding with a ultrasonic sensor mounted on a servo.

The modules also enable remote controling the robots GPIOs. This enables 
executing the scripts on a laptop/computer and over e.g. WLAN remote controling the Raspberry Pi 
which provides a WLAN Hotspot, see remote_pin_ and pi_hotspot_ . So, the robot can freely
move with a powerbank attached and does not have to be connected to a monitor, keyboard 
and mouse while controling/programming it. The possibillity of remote controling
the Raspberry Pis GPIOs is a big advantage of the used pigpio_ module. It is also possible to execute
the scripts on the Raspberry Pi itself and connect to it over VNC, see VNC_ . For both ways, 
executing the code on the Raspberry Pi itself or remote on a laptop/computer to control
the GPIOs, no modifications have to be made in the source code, it works in both cases.

All the default values in the modules are the once which have been used at a 
demo implementation. They provide a good starting point for the range of the values.

The documentation is done with Sphinx_ and can be extended or modified as needed for 
e.g. documenting own projects based on this or if extending functionality of the modules 
and document them.

Following some pictures of the demo implementation. Buying two Parallax Feedback 360° 
High-Speed servos `360_data_sheet`_ , two robot wheels `wheel_robot`_, one Parallax 
Standard Servo `stand_data_sheet`_ and a `HC-SR04`_ ultrasonic sensor will also be sufficient.
Then build an own chassi to mount all the stuff, instead of buying directly a ActivityBot 
360° Robot Kit 360_kit_ .

View from the right side.

.. image:: /_static/1.jpg

View from the front side.

.. image:: /_static/2.jpg

View from the backside.

.. image:: /_static/3.jpg

View from top, including the local coordinate system of the robot. 

.. image:: /_static/4.jpg

.. image:: /_static/5.jpg

Cabling
-------

Below see a Fritzing sheet which shows the cabling. The voltage divider is using two resistors,
blue one with 82 Ohm, gold one with 150 Ohm.

.. warning::

    The voltage divider is very important! The ``Echo`` Pin of the `HC-SR04`_ outputs a 
    PWM with the same voltage as ``VCC`` Pin (5 V in this case) which needs to be converted 
    to 3.3 V. 3.3 V is the max voltage the Raspberry Pi can handle on a GPIO, otherwise 
    it might get damaged! The chosen resistors for the voltage divider convert 5 V to 
    3.23 V. **Setup:** The output of the ``Echo`` Pin is connected to the blue 82 Ohm 
    resistor. At its end the GPIO is connected and then the golden 150 Ohm resistor at 
    which end ground is connected.

.. warning::

    The 5 V of the USB power supply should be connceted to the 5 V Pin of the Raspberry Pi 
    directly, as shown in the Fritzing sheet, because it does not only power the
    Raspberry Pi itself, also the three servos and maybe more devices, which get added 
    in the future, are powered over it. So powering all devices over the micro-USB port 
    should be avoided, because otherwise all needed current of all devices would be 
    conducted through the Raspberry Pi.
    
.. image:: /_static/6.jpg

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