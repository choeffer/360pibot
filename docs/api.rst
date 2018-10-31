.. _`360pibot_API`:

360pibot API
============

In this section it is documented how to use each module. In the source
code it is commented, if necessary, how each part of the code is working 
and what it is intended to do.

For the Parallax Feedback 360° High-Speed Servo `360_data_sheet`_ also C 
example code is available sample_360_ .

.. _`lib_scanner`:

lib_scanner
-----------

Module for making measurements with a `HC-SR04`_ ultrasonic sensor and rotating 
it with a Parallax Standard Servo `stand_data_sheet`_ .

This module includes three classes. One for making the measurements with an `HC-SR04`_ 
ultrasonic sensor :class:`lib_scanner.hcsr04`, one for stearing a Parallax Standard Servo 
`stand_data_sheet`_ :class:`lib_scanner.para_standard_servo` and one which combines 
the first two to scan the surrounding :class:`lib_scanner.scanner` .

.. automodule:: lib_scanner
   :members:

.. _`lib_para_360_servo`:

lib_para_360_servo
------------------

Module for setting the speed and reading the position of a Parallax Feedback 360° 
High-Speed Servo `360_data_sheet`_ .

This module includes three classes. One for setting the speed :class:`lib_para_360_servo.write_pwm` ,
one for reading the position :class:`lib_para_360_servo.read_pwm` and one for calibrating 
a servo to determine the appropriate ``dcMin`` / ``dcMax`` values needed in :ref:`lib_motion` 
:class:`lib_para_360_servo.calibrate_pwm` .

.. automodule:: lib_para_360_servo
   :members:

.. _`lib_motion`:

lib_motion
----------

Module for moving the robot.

This module includes the class :class:`lib_motion.move` which is the 
the core of the movement controlling. The module imports :ref:`lib_para_360_servo` .

.. automodule:: lib_motion
   :members:

References
----------

.. target-notes::

.. _`360_data_sheet`: https://www.parallax.com/sites/default/files/downloads/900-00360-Feedback-360-HS-Servo-v1.1.pdf
.. _sample_360: https://www.parallax.com/downloads/feedback-360%C2%B0-high-speed-servo-propeller-c-example-code
.. _`HC-SR04`: https://cdn.sparkfun.com/assets/b/3/0/b/a/DGCH-RED_datasheet.pdf
.. _`stand_data_sheet`: https://www.parallax.com/sites/default/files/downloads/900-00005-Standard-Servo-Product-Documentation-v2.2.pdf
