import time

import pigpio


#https://cdn.sparkfun.com/assets/b/3/0/b/a/DGCH-RED_datasheet.pdf
class hcsr04:
    """
    Makes measurements with an `HC-SR04`_ ultrasonic sensor.

    This class allows making measurements with a `HC-SR04`_ ultrasonic sensor. For this,
    a trigger signal will sent to a defined GPIO Pin ``trigger`` and a PWM will be recieved 
    on a defined GPIO Pin ``echo``. With the recieved PWM the distance to an object is calculated.

    :param pigpio.pi pi: 
        Instance of a pigpio.pi() object.
    :param int trigger:
        GPIO identified by their Broadcom number, see elinux.org_ .
        To this GPIO the trigger pin of the `HC-SR04`_ has to be connected.
    :param int echo:
        GPIO identified by their Broadcom number, see elinux.org_ .
        To this GPIO the echo pin of the `HC-SR04`_ has to be connected.
    :param int,float pulse_len:
        Defines the lenght of the send pulse on the trigger GPIO in microseconds.
        **Default:** 15, taken from the data sheet and added 50%.

    .. _elinux.org: https://elinux.org/RPi_Low-level_peripherals#Model_A.2B.2C_B.2B_and_B2
    .. _`HC-SR04`: https://cdn.sparkfun.com/assets/b/3/0/b/a/DGCH-RED_datasheet.pdf
    """

    def __init__(self, pi, trigger, echo, pulse_len = 15):

        self.pi = pi
        self.trigger = trigger
        self.echo = echo
        self.pulse_len = pulse_len
        self.tick_high = None
        self.tick_high_old = None
        self.tick_low = None
        self.tick_low_old = None
        self.pulse_width = None

        #http://abyz.me.uk/rpi/pigpio/python.html#set_mode
        self.pi.set_mode(gpio = self.trigger, mode = pigpio.OUTPUT)
        self.pi.set_mode(gpio = self.echo, mode = pigpio.INPUT)

        #http://abyz.me.uk/rpi/pigpio/python.html#callback
        self.cb = self.pi.callback(user_gpio=self.echo, edge=pigpio.EITHER_EDGE, func=self.cbf)

    #calculates the duty cycle
    def cbf(self, gpio, level, tick):

        #change to low (falling edge)
        if level == 0:
            
            self.tick_low = tick
            #try is needed because one of t1 or t2 might not be an int and then tickDiff would fail
            try:
                #http://abyz.me.uk/rpi/pigpio/python.html#callback
                # tick        32 bit    The number of microseconds since boot
                #                       WARNING: this wraps around from
                #                       4294967295 to 0 roughly every 72 minutes
                #Tested: This is handled by the tickDiff function internally, if t1 (earlier tick)
                #is smaller than t2 (later tick), which could happen every 72 min. The result will
                #not be a negative value, the real difference will be properly calculated.
                self.pulse_width = pigpio.tickDiff(t1=self.tick_high, t2=self.tick_low)
            except Exception:
                pass
            
        #change to high (rising edge)
        elif level == 1:

            self.tick_high = tick

    def trig(self):

        #default pulse_len is 50% more than needed (15 microseconds instead of 10)
        #to have a buffer to surely trigger the measurement
        self.pi.gpio_trigger(user_gpio = self.trigger, pulse_len = self.pulse_len, level = 1)

    def read(self, temp_air = 20, upper_limit = 4, number_of_sonic_bursts = 8, added_buffer = 2, debug = False):
        """
        Measures the distance to an object.

        This method triggers a measurement, does all the calculations and returns the distance in meters.

        :param int,float temp_air: 
            Temperature of the air in degree celsius.
            The temperature is used for calculating the distance to an object.
            **Default:** 20.
        :param int,float upper_limit: 
            The upper measurement limit in meters
            **Default:** 4, upper limit taken from the data sheet `HC-SR04`_ .
        :param int number_of_sonic_bursts:
            The number of sonic bursts the sensor
            will make. This parameter is later used internally in the method.
            **Default:** 8, taken from the data sheet `HC-SR04`_ .
        :param int,float added_buffer:
            The added safety buffer for waiting for the distance measurement.
            This parameter is later used internally in the method.
            **Default:** 2, so 100% safety buffer.
        :param bool debug:
            Controls if debugging printouts are made or not. For more details, have a look 
            at the source code. **Default:** False, so no printouts are made.
        
        :return: Measured distance in meters.
        :rtype: float

        .. _`HC-SR04`: https://cdn.sparkfun.com/assets/b/3/0/b/a/DGCH-RED_datasheet.pdf
        """
        
        #speed of sound at 20 degree celsius -> c_air = 343.42 m/s
        c_air = 331.3 + (0.606 * temp_air)

        #max distance is upper_limit (in m):
        #let the sensor make the measurements, it will do a 8 cycle sonic burst:
        #4×2÷343,42=23295,09 microsecond or ~23 ms or 0,023 s at temp_air = 20
        #so 8 cycle sonic burst should take in worst 8 * 0,023 s = 0,184 s
        #so adding 100% buffer would lead to ~0,368 s
        #but that also depends on the used sonar sensor, see datasheet.
        #in this time frame the callback function should be called two times for each sonic burst.
        wait_for_measurement = upper_limit * 2 / c_air * number_of_sonic_bursts * added_buffer
        
        #counter while loop
        a = 0

        #check if recognized rising and falling edges are valid, so correctly catched by the callback function
        while self.tick_high is None or self.tick_high is self.tick_high_old or self.tick_low is None or self.tick_low is self.tick_low_old or self.pulse_width is None:
            
            self.trig()
            time.sleep(wait_for_measurement)
            #debugging information
            if a >= 1 and debug:
                print('{} {} {} {}'.format('number of extra measurements:', a, 'at this time:', time.time()))
            a=+1

        #calculated distance in m
        distance = self.pulse_width / 1000000 * c_air / 2

        #and store the the last values of self.tick_high and self.tick_low
        self.tick_high_old = self.tick_high
        self.tick_low_old = self.tick_low
        #set self.tick_high and self.tick_low back to initial values
        self.tick_high = None
        self.tick_low = None
        #set self.pulse width back to initial value
        self.pulse_width = None

        #check if measured/calculated distance is out of measurement range of the sensor,
        #see datasheet
        if distance >= upper_limit:

            if debug:

                print('{} {}'.format('out of upper limit, calculated distance:', distance))

            distance = upper_limit

        return distance
    
    def cancel(self):
        """
        Cancel the started callback function.

        This method cancels the started callback function if initializing an object.
        As written in the pigpio callback_ documentation, the callback function may be cancelled
        by calling the cancel function after the created instance is not needed anymore, see examples 
        in the source code.

        .. _callback: http://abyz.me.uk/rpi/pigpio/python.html#callback
        """

        self.cb.cancel()

#https://www.parallax.com/sites/default/files/downloads/900-00005-Standard-Servo-Product-Documentation-v2.2.pdf

class para_standard_servo:
    """
    Stears a servo, in this case a Parallax Stadard Servo stand_data_sheet_ .

    This class stears a Parallax Stadard Servo and should also work with other servos which 
    have a 50Hz PWM for setting the position. The position of the Parallax Standard Servo 
    can be set between -90 (``min_degree``) and +90 (``max_degree``) degree.

    .. warning::
        Be carefull with setting the min and max pulsewidth! Test carefully ``min_pw`` and ``max_pw``
        before setting them. Wrong values can damage the servo, see set_servo_pulsewidth_ !!!

    :param pigpio.pi pi: 
        Instance of a pigpio.pi() object.
    :param int gpio:
        GPIO identified by their Broadcom number, see elinux.org_ .
        To this GPIO the signal wire of the servo has to be connected.
    :param int min_pw:
        Min pulsewidth, see **Warning**, carefully test the value before!
        **Default:** 1000, taken from set_servo_pulsewidth_ .
    :param int max_pw:
        Max pulsewidth, see **Warning**, carefully test the value before!
        **Default:** 2000, taken from set_servo_pulsewidth_ .
    :param int min_degree:
        Min degree which the servo is able to move.
        **Default:** -90, taken from stand_data_sheet_ .
    :param int max_degree:
        Max degree which the servo is able to move.
        **Default:** +90, taken from stand_data_sheet_ .       

    .. _elinux.org: https://elinux.org/RPi_Low-level_peripherals#Model_A.2B.2C_B.2B_and_B2
    .. _stand_data_sheet: https://www.parallax.com/sites/default/files/downloads/900-00005-Standard-Servo-Product-Documentation-v2.2.pdf
    .. _set_servo_pulsewidth: http://abyz.me.uk/rpi/pigpio/python.html#set_servo_pulsewidth
    """

    def __init__(self, pi, gpio, min_pw = 1000, max_pw = 2000, min_degree = -90, max_degree = 90):

        self.pi = pi
        self.gpio = gpio
        #min_pw and max_pw might needed to be interchanged, depending on
        #if min_pw is moving servo to max_right or max_left,
        #see test functions below
        self.min_pw = min_pw
        self.max_pw = max_pw
        #allowed range of servo movement, see max_left(), max_right() functions
        self.min_degree = min_degree
        self.max_degree = max_degree
        #calculate slope for calculating the pulse width
        self.slope = (self.min_pw - ((self.min_pw + self.max_pw)/2)) / self.max_degree
        #calculate y-offset for calculating the pulse width
        self.offset = (self.min_pw + self.max_pw)/2

    def set_pw(self, pulse_width):
        """
        Sets pulsewidth of the PWM.

        This method allows setting the pulsewidth of the PWM directly. This can be used to
        test which ``min_pw`` and ``max_pw`` are appropriate. For this the ``min_pw`` and ``max_pw``
        need to be set very small and big so that they do not limit the set pulsewidth. Because normally
        they are set to protect the servo, by limiting the pulsewidth to a certain range.

        :param int,float pulsewidth:
            Pulsewidth of the PWM signal. Will be limited to ``min_pw`` and ``max_pw``.
        """
        
        #be carefully with setting the pulsewidth!!!
        #test carefully min_pw and max_pw value before settting them!!!
        #this can DAMAGE the servo!!!
        #http://abyz.me.uk/rpi/pigpio/python.html#set_servo_pulsewidth
        pulse_width = max(min(self.max_pw, pulse_width), self.min_degree)

        self.pi.set_servo_pulsewidth(user_gpio = self.gpio, pulsewidth = pulse_width)
        
    def calc_pw(self, degree):

        pulse_width = self.slope * degree + self.offset
        
        return pulse_width

    def set_position(self, degree):
        """
        Sets position of the servo in degree.

        This method sets the servo position in degree. Minus is to the left, plus to the right.

        :param int,float degree:
            Should be between ``min_degree`` (max left) and ``max_degree`` 
            (max right), otherwise the value will be limited to those values.
        """
        
        degree = max(min(self.max_degree, degree), self.min_degree)

        calculated_pw = self.calc_pw(degree = degree)
        self.set_pw(pulse_width = calculated_pw)

    def middle_position(self):
        """
        Sets the position of the servo to 0 degree, so middle position.
        """

        pulse_width = (self.min_pw+self.max_pw)/2
        self.set_pw(pulse_width = pulse_width)

    def max_left(self):
        """
        Sets the position of the servo to -90 degree, so ``min_degree`` (max left).
        """
        
        self.set_pw(self.max_pw)

    def max_right(self):
        """
        Sets the position of the servo to 90 degree, so ``max_degree`` (max right).
        """

        self.set_pw(self.min_pw)

class scanner:
    """
    Scans the surrounding with the help of the :class:`hcsr04` and :class:`para_standard_servo` classes.

    This class stears the servo position and triggers measurements with the ultrasonic sensor. With a passed
    :class:`list`, measurements will be made at the defined positions. A :class:`dict`
    will be returned with the measured distances at the defined positions.

    .. warning::
        Be carefull with setting the min and max pulsewidth! Test carefully ``min_pw`` and ``max_pw``
        before setting them. Wrong values can damage the servo, see set_servo_pulsewidth_ !!!

    :param pigpio.pi pi: 
        Instance of a pigpio.pi() object.
    :param int trigger:
        GPIO identified by their Broadcom number, see elinux.org_ .
        To this GPIO the trigger pin of the `HC-SR04`_ has to be connected.
    :param int echo:
        GPIO identified by their Broadcom number, see elinux.org_ .
        To this GPIO the echo pin of the `HC-SR04`_ has to be connected.
    :param int gpio:
        GPIO identified by their Broadcom number, see elinux.org_ .
        To this GPIO the signal wire of the servo has to be connected.
    :param int min_pw:
        Min pulsewidth, see **Warning**, carefully test the value before!
        **Default:** 1000, taken from set_servo_pulsewidth_ .
    :param int max_pw:
        Max pulsewidth, see **Warning**, carefully test the value before!
        **Default:** 2000, taken from set_servo_pulsewidth_ .
    :param int min_degree:
        Min degree which the servo is able to move.
        **Default:** -90, taken from stand_data_sheet_ .
    :param int max_degree:
        Max degree which the servo is able to move.
        **Default:** +90, taken from stand_data_sheet_ .
    :param list angles:
        List of positions where the servo moves to and the ultrasonic sensor will make measurements.
    :param int,float time_servo_reach_position:
        Time in seconds to wait until the servo moves from one to another position. This needs to be tested
        for each servo, how much time is needed.
        **Default:** 0.35, this was sufficient to safely reach each position before the measurement
        is made.
    :param bool debug:
        Controls if debugging printouts and measurements are made or not. For more details, have a look 
        at the source code. **Default:** False, so no printouts and measurements are made.
        
    .. todo::
        Implement passing all values to the sonar.read() function (see source code). At the moment just 
        debug is passed and for the rest the default values are used, see :meth:`hcsr04.read`.

    .. _elinux.org: https://elinux.org/RPi_Low-level_peripherals#Model_A.2B.2C_B.2B_and_B2
    .. _`HC-SR04`: https://cdn.sparkfun.com/assets/b/3/0/b/a/DGCH-RED_datasheet.pdf
    .. _set_servo_pulsewidth: http://abyz.me.uk/rpi/pigpio/python.html#set_servo_pulsewidth
    """
        
    #default values are for the Case-Study installation used
    def __init__(
        self, pi, trigger = 6, echo = 5, 
        gpio = 22, min_pw = 600, max_pw = 2350, min_degree = -90, max_degree = 90,
        angles = [-90, -45, 0, 45, 90],
        time_servo_reach_position = 0.35, debug = False):

        #create one pigpio.pi() instance for the sensor and servo in parallel     
        self.pi = pi
        self.trigger = trigger
        self.echo = echo
        self.gpio = gpio
        self.min_pw = min_pw
        self.max_pw = max_pw
        self.min_degree = min_degree
        self.max_degree = max_degree
        self.angles = angles
        self.time_servo_reach_position = time_servo_reach_position
        self.debug = debug

        #initialize sonar and servo instance
        #https://gpiozero.readthedocs.io/en/stable/recipes.html#pin-numbering
        self.sonar = hcsr04(pi = self.pi, trigger = self.trigger, echo = self.echo)
        self.servo = para_standard_servo(pi = self.pi, gpio = self.gpio, min_pw = self.min_pw, max_pw = self.max_pw, min_degree = self.min_degree, max_degree = self.max_degree)

        #buffer time for initializing everything
        time.sleep(1)

    def read_all_angles(self):
        """
        Moves servo and makes measurements at every defined position.

        This method moves the servo to every position defined in :class:`list` ``angles`` and 
        makes a measuremnt there and afterwards returns a :class:`dict` with the distance 
        in meter for every position.

        :return: Measured distances in meters for each position defined in ``angles``.
        :rtype: dict
        """

        #create an empty dict
        measurement_dict = dict()
        if self.debug:
            start_time = time.time()
        #return servo to middle position, to not have to move e.g. from
        #last 90 degree to new -90 degree in following for loop
        self.servo.middle_position()
        #wait for servo reaching the position
        time.sleep(self.time_servo_reach_position)

        for ang in self.angles:

            self.servo.set_position(degree = ang)
            #wait for servo reaching the position
            time.sleep(self.time_servo_reach_position)
            measurement_dict[ang] = self.sonar.read(debug = self.debug)
        
        if self.debug:
            stop_time = time.time() - start_time
            print('{} {}'.format('time needed for one measurement round:', stop_time))

        return measurement_dict

    def cancel(self):
        """
        Cancel the started callback function.

        This method cancels the started callback function if initializing an object.
        As written in the pigpio callback_ documentation, the callback function may be cancelled
        by calling the cancel function after the created instance is not needed anymore, see examples 
        in the source code.

        .. _callback: http://abyz.me.uk/rpi/pigpio/python.html#callback
        """

        self.sonar.cancel()

if __name__ == '__main__':

    #### Example 1
    pi = pigpio.pi()
    ranger = scanner(pi = pi)
    distances = ranger.read_all_angles()
    print(distances)
    #http://abyz.me.uk/rpi/pigpio/python.html#callback
    ranger.cancel()
    #http://abyz.me.uk/rpi/pigpio/python.html#stop
    pi.stop()

    #### Example 2
    # pi = pigpio.pi()
    # servo = para_standard_servo(gpio = 22, pi = pi, min_pw = 600, max_pw = 2350)
    # servo.middle_position()
    # time.sleep(1)
    # servo.max_right()
    # time.sleep(1)
    # servo.max_left()
    # time.sleep(1)
    # servo.set_position(degree = 45)
    # #http://abyz.me.uk/rpi/pigpio/python.html#stop
    # pi.stop()
