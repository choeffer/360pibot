.. _Introduction:

Introduction
============

Python 3 implementation for programming an ActivityBot 360° Robot Kit 360_kit_ with
a Raspberry Pi. The modules (see :ref:`360pibot_Python_API` ) of the implementation are using the pigpio_ module 
to control the GPIOs of the Raspberry Pi. No other external module is needed.

At the moment, the following functions are implemented.

* Turning on the spot.
* Moving straight forward and backward.
* Scanning the surrounding with an ultrasonic sensor mounted on a servo.

The turning and moving straight movements are controlled by four digital PID 
controllers. Each wheel is controlled by a cascade control, which means 
a cascade of two PID controllers. The outer loops are controlling the position, 
the inner loops are controlling the speed of each wheel.

The modules provide simple API interfaces for the turning and moving straight 
movements and also for scanning the surrounding or stearing a servo. Have a look 
at the :ref:`Examples` section for some code examples.

All the default values in the modules are the once which are used while 
experimenting/developing with the demo implementation. They provide a good starting 
point for the range of the values. Pictures of the demo implementation can be
found further down in this section.

The modules also enable remote controlling the Raspberry Pis GPIOs. This enables 
use of the modules on a laptop/computer and over e.g. WLAN remote controlling the Raspberry Pi 
which provides a WLAN Hotspot, see remote_pin_ and pi_hotspot_ . So, the robot can freely
move with a powerbank attached and does not have to be connected to a monitor, keyboard 
and mouse while controlling/programming it. The possibillity of remote controlling
the Raspberry Pis GPIOs is a big advantage of the used pigpio_ module. It is also possible to 
use the modules on the Raspberry Pi itself and connect to it over VNC, see VNC_ . For both ways, 
using the modules on the Raspberry Pi itself or remote on a laptop/computer to control
the Raspberry Pis GPIOs, no modifications have to be done in the source code of the modules.

The documentation is made with Sphinx_ and can be extended or modified as needed for 
e.g. documenting own projects based on this or if extending functionality of the modules 
and documenting this.

Buying two Parallax Feedback 360° High-Speed Servos `360_data_sheet`_ , two robot wheels 
`wheel_robot`_, one Parallax Standard Servo `stand_data_sheet`_ and a `HC-SR04`_ 
ultrasonic sensor will also be sufficient. This enables building an own chassi 
and attaching there the above listed parts, instead of buying an ActivityBot 
360° Robot Kit 360_kit_ .

Pictures of the demo implementation
-----------------------------------

View from the right side.

.. image:: /_static/1.jpg

View from the front side.

.. image:: /_static/2.jpg

View from the back side.

.. image:: /_static/3.jpg

.. image:: /_static/5.jpg

Defined local coordinate system in module lib_motion
----------------------------------------------------

The following picture shows the local coordinat system which is used in 
:ref:`lib_motion` .

.. image:: /_static/4.jpg

Cabling of the demo implementation
----------------------------------

Below see a Fritzing sheet which illustrates the cabling of the demo implementation. 
The voltage divider is build out of two resistors, blue one with 82 Ohm and gold 
one with 150 Ohm.

.. warning::

    The voltage divider is very important! The ``Echo`` Pin of the `HC-SR04`_ outputs a 
    PWM with the same voltage as ``VCC`` Pin (5 V in this case) which needs to be converted 
    to 3.3 V. 3.3 V is the max voltage the Raspberry Pi can handle on a GPIO, otherwise 
    it might get damaged! The chosen resistors for the voltage divider convert 5 V to 
    3.23 V. **Setup:** The output of the ``Echo`` Pin is connected to the blue 82 Ohm 
    resistor. At its end, the GPIO is connected and then the golden 150 Ohm resistor at 
    whose end ground is connected.

.. warning::

    The 5 V of the USB power supply should be connceted to the 5 V Pin of the Raspberry Pi 
    directly, as shown in the Fritzing sheet, because it does not only power the
    Raspberry Pi itself, also the three servos and maybe more devices, which get added 
    in the future, are powered over it. Therefore, powering all devices over the micro-USB 
    port should be avoided, because otherwise all needed current of all devices would be 
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