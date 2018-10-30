import math
import statistics
import time

import pigpio

import lib_para_360_servo

class motion:
    """
    Controls the robot movement.

    This class controls the robot movement by controlling the two Parallax Feedback 360° 
    High-Speed Servo `360_data_sheet`_ . The robots local coordinate system is defined in
    the following way. X-axis positive is straight forward, y-axes positive perpendicular 
    to the x-axis in the direction to the left wheel. The center (0/0) is where the middle
    of the robot chassis is cutting across a imaginary line through both wheels/servos.
    Angle phi is the displacement of the local coordinate system to the real world coordinate
    system. See :ref:`Introduction` page for a picture.

    .. warning::
        Be carefull with setting the min and max pulsewidth! Test carefully ``min_pw`` and ``max_pw``
        before setting them. Wrong values can damage the servo, see set_servo_pulsewidth_ !!!

    :param pigpio.pi pi: 
        Instance of a pigpio.pi() object.
    :param int width_robot:
        Distance between middle right wheel and middle left wheel in mm. **Default:** 102 mm, 
        measured.
    :param diameter_wheels:
        Diameter of both wheels. **Default:** 66 mm, measured and taken from the product 
        website `wheel_robot`_ .
    :param int unitsFC:
        Units in a full circle. **Default:** 360, so each wheel is divided into 360 sections/ticks.
    :param float dcMin_l:
        Min duty cycle of the left wheel. **Default:** 27.3, measured with the 
        :meth:`lib_para_360_servo.calibrate_pwm` method, see :ref:`Examples` .
    :param float dcMax_l:
        Max duty cycle of the left wheel. **Default:** 969.15, measured with the 
        :meth:`lib_para_360_servo.calibrate_pwm` method, see :ref:`Examples` .
    :param float dcMin_r:
        Min duty cycle of the right wheel. **Default:** 27.3, measured with the 
        :meth:`lib_para_360_servo.calibrate_pwm` method, see :ref:`Examples` .
    :param float dcMax_r:
        Max duty cycle of the left wheel. **Default:** 978.25, measured with the 
        :meth:`lib_para_360_servo.calibrate_pwm` method, see :ref:`Examples` .
    :param int l_wheel_gpio:
        GPIO identified by their Broadcom number, see elinux.org_ .
        To this GPIO the feedback wire of the left servo has to be connected.
    :param int r_wheel_gpio:
        GPIO identified by their Broadcom number, see elinux.org_ .
        To this GPIO the feedback wire of the right servo has to be connected.
    :param int servo_l_gpio:
        GPIO identified by their Broadcom number, see elinux.org_ .
        To this GPIO the control wire of the left servo has to be connected.
    :param int min_pw_l:
        Min pulsewidth, see **Warning**, carefully test the value before!
        **Default:** 1280, taken from the data sheet `360_data_sheet`_ .
    :param int max_pw_l:
        Max pulsewidth, see **Warning**, carefully test the value before!
        **Default:** 1720, taken from the data sheet `360_data_sheet`_ .
    :param int servo_r_gpio:
        GPIO identified by their Broadcom number, see elinux.org_ .
        To this GPIO the control wire of the right servo has to be connected.
    :param int min_pw_r:
        Min pulsewidth, see **Warning**, carefully test the value before!
        **Default:** 1280, taken from the data sheet `360_data_sheet`_ .
    :param int max_pw_r:
        Max pulsewidth, see **Warning**, carefully test the value before!
        **Default:** 1720, taken from the data sheet `360_data_sheet`_ .

    .. todo::
        Implement passing min_speed and max_speed values down to 
        :meth:`lib_para_360_servo.write_pwm` when initialzing the object.

    .. _`360_data_sheet`: https://www.parallax.com/sites/default/files/downloads/900-00360-Feedback-360-HS-Servo-v1.1.pdf
    .. _`wheel_robot`: https://www.parallax.com/product/28114
    .. _elinux.org: https://elinux.org/RPi_Low-level_peripherals#Model_A.2B.2C_B.2B_and_B2
    """

    #default values are measured with the calibrate_pwm function from lib_servo.py
    def __init__(
        self, pi, width_robot = 102, diameter_wheels = 66, unitsFC = 360,
        dcMin_l = 27.3, dcMax_l = 969.15,
        dcMin_r = 27.3, dcMax_r = 978.25,
        l_wheel_gpio = 16, r_wheel_gpio = 20,
        servo_l_gpio = 17, min_pw_l = 1280, max_pw_l = 1720,
        servo_r_gpio = 27, min_pw_r = 1280, max_pw_r = 1720):
        
        self.pi = pi
        self.unitsFC = unitsFC
        self.dcMin_l = dcMin_l
        self.dcMax_l = dcMax_l
        self.dcMin_r = dcMin_r
        self.dcMax_r = dcMax_r
        self.width_robot = width_robot
        self.diameter_wheels = diameter_wheels

        self.l_wheel = lib_para_360_servo.read_pwm(pi = self.pi, gpio = l_wheel_gpio)
        self.r_wheel = lib_para_360_servo.read_pwm(pi = self.pi, gpio = r_wheel_gpio)
        self.servo_l = lib_para_360_servo.write_pwm(pi = self.pi, gpio = servo_l_gpio, min_pw = min_pw_l, max_pw = max_pw_l)
        self.servo_r = lib_para_360_servo.write_pwm(pi = self.pi, gpio = servo_r_gpio, min_pw = min_pw_r, max_pw = max_pw_r)

        #needed time for initializing the four instances
        time.sleep(1)

    #Angular position in units full circle
    def get_angle_l(self):

        #driving forward will increase the angle
        angle_l = (self.unitsFC - 1) - ((self.l_wheel.read() - self.dcMin_l) * self.unitsFC) / (self.dcMax_l - self.dcMin_l + 1)

        angle_l = max(min((self.unitsFC - 1), angle_l), 0)

        return angle_l

    #Angular position in units full circle
    def get_angle_r(self):

        #driving forward will increase the angle
        angle_r = (self.r_wheel.read() - self.dcMin_r) * self.unitsFC / (self.dcMax_r - self.dcMin_r + 1)

        angle_r = max(min((self.unitsFC - 1), angle_r), 0)

        return angle_r

    def set_speed_l(self, speed):

        self.servo_l.set_speed(-speed)

        return None

    def set_speed_r(self, speed):

        self.servo_r.set_speed(speed)

        return None

    def get_total_angle(self, angle, unitsFC, prev_angle, turns):
       
        #for counting number of rotations
        #If 4th to 1st quadrant
        if((angle < (0.25*unitsFC)) and (prev_angle > (0.75*unitsFC))):
            turns += 1
        #If in 1st to 4th quadrant
        elif((prev_angle < (0.25*unitsFC)) and (angle > (0.75*unitsFC))):
            turns -= 1

        #total angle measurement from zero
        if(turns >= 0):
            total_angle = (turns*unitsFC) + angle
        elif(turns < 0):
            total_angle = ((turns + 1)*unitsFC) - (unitsFC - angle)

        return turns, total_angle

    def get_target_angle(self, number_ticks, angle):
        
        #positiv number_ticks will be added, negativ number_ticks substracted
        target_angle = angle + number_ticks

        return target_angle

    def tick_length(self):

        tick_length_mm = math.pi * self.diameter_wheels / self.unitsFC

        return tick_length_mm

    def arc_circle(self, degree):

        arc_circle_mm = degree * math.pi * self.width_robot / 360.0

        return arc_circle_mm

    def turn(self, degree):
        """
        Turns the robot about x degree.

        This method turns the robot. Positive degree value turn the robot to the left,
        negative degree value to the right, see picture in :ref:`Introduction` where  local 
        coordinate system of the robot is shown. This method calls :meth:`lib_motion.move` which
        controlls the movement of the robot.

        :param int,float degree:
            Degree the robot has to turn.
        """

        number_ticks = self.arc_circle(degree)/self.tick_length()

        self.move(number_ticks = number_ticks, turn = True)

        return None

    def straight(self, distance_in_mm):
        """
        Moves the robot about x mm forward or backward.

        This method moves the robot about x mm forward or backward. Positive distance value move the 
        robot forward (regarding the local x-axis), negative distance value backward 
        (regarding the local x-axis), see picture in :ref:`Introduction` where  local 
        coordinate system of the robot is shown. This method calls :meth:`lib_motion.move` 
        which controlls the movement of the robot.

        :param int,float distance_in_mm:
            Distance the robot has to move.
        """

        number_ticks = distance_in_mm/self.tick_length()

        self.move(number_ticks = number_ticks, straight = True)

        return None

    def move(
        self,
        number_ticks = 0,
        #0.010 seconds:
        #1. PWM of motor feedback is 910Hz (0,001098901 s), so position changes cannot 
        #be recognized faster than 1.1 ms, therefore, it is not needed to run the outer control 
        #loop more often and update the speed values which have a 50 Hz (20ms) PWM.
        #2. Tests of the runtime of the code including the controller part showed, that
        #writing the pulse_width (pi.set_servo_pulsewidth()) in the lib_para_360_servo.py is 
        #the bottleneck which drastically slows down the code by the factor ~400 
        #(0,002 seconds ÷ 0,000005 seconds; runtime with / without writing pulsewidth).
        #3. For recognizing the RPMs of the wheel 10ms is needed to have enough changes in the
        #position, was found out by testing.
        sampling_time = 0.01,
        # Outer Controller, position
        Kp_p = 0.1, #not too big values, otherwise output of position control would slow down too abrupt
        Ki_p = 0,
        Kd_p = 0,
        # Inner Controller, speed
        Kp_s = 0.5,
        Ki_s = 0.1,
        Kd_s = 0,
        straight = False, turn = False):
        """
        Controlls movement of the robot.

        This method controlls the movement of the robot. It is called from :meth:`lib_motion.turn` 
        or :meth:`lib_motion.straight` and is not to ment to be called directly. The parameters
        of the four used digital PID controllers have to be hardcoded into the modules source code at the moment.
        The four PID controllers are used to make two cascade controll loops, one cascade control loop
        for each wheel. Each cascade controol loop has the same parameters (P/I/D values), so that 
        both wheels are controlled in the same way. Chosen default: Outer controll loop is a pure P 
        controller, the inner controll loop is a PI controller. The outer loop is a position controller,
        the inner loop a speed controller. The I part of each PID controller can be limited, so that 
        the sum of the errors is not integrated till infinity which means to very high or low values 
        which might cause problems. The output value of each inner PID controller is scaled between -1 
        and 1 and the output values of each outer PID controller is limited to -1 to 1.
        This ensures that no scaling factors are introduced in the P/I/D values and also that
        the output of the inner loop (speed) matches the range of the speed of the servos, defined in 
        :class:`lib_para_360_servo.write_pwm.set_speed` . A sliding median window is used to filter out
        the noise of the rotation speed measurement (ticks/s) which is done indirectly by measuring the 
        position of the servo. Also a deadband filter after the error calculation of the outer control
        loop is implemented. This adjustments help to make the controllers more stable, e.g. filter out
        outliers while calculating the rotation speed and therefore avoid high value changes/jumps or
        avoid oscillations after reaching the set-point (position). The sample time of the digital PID
        controllers can also be freely chosen and does not influence the P/I/D values nor the rotation
        speed measurement. All this can be tuned/adjusted in the source code. This makes the whole method
        very flexible and customizeable.

        :param int,float number_ticks:
            Number of ticks the wheels have to move.
        :param bool straight:
            True or False, if robot should move straight. **Default:** False.
        :param bool turn:
            True or False, if robot should turn. **Default:** False.

        .. todo::
        
            Modify the module/class so that the PID controller values can be set while initializing
            the class, so that they do not have to be hardcoded in the source code.

        .. todo::

            Modify the stopping condition, so that both wheels have to be at the set-point
            and not just the right wheel. At moment the control loop stops even if left
            wheel has not reached the set-point. This causes slight inaccuracies while moving!
            See stopping condition in the source code.       
        
        """

        turns_l = 0
        turns_r = 0

        angle_l = self.get_angle_l()
        angle_r = self.get_angle_r()

        target_angle_r = self.get_target_angle(number_ticks = number_ticks, angle = angle_r)

        if straight == True:

            #speed and number_ticks of servo_l must rotate in
            #SAME direction to servo_r while driving straight
            target_angle_l = self.get_target_angle(number_ticks = number_ticks, angle = angle_l)

        elif turn == True:
            
            #speed and number_ticks of servo_l must rotate in
            #OPPOSITE direction to servo_r while turning
            target_angle_l = self.get_target_angle(number_ticks = -number_ticks, angle = angle_l)

        #initial values sum_error_*
        sum_error_r_p = 0
        sum_error_r_s = 0
        sum_error_l_p = 0
        sum_error_l_s = 0
        
        #initial values error_*_old
        error_l_p_old = 0
        error_l_s_old = 0
        error_r_p_old = 0
        error_r_s_old = 0

        #empty list for ticks_*
        list_ticks_l = []
        list_ticks_r = []

        #start time of the outer control loop
        start_time = time.time()
        #outer control loop: total distance/right wheel
        position_reached = False

        #### start of outer control loop:
        while not position_reached:
            #DEBUGGING OPTION: printing runtime of loop , see end of while true loop
            #start_time_each_loop = time.time()

            angle_l = self.get_angle_l()
            angle_r = self.get_angle_r()

            try:
                turns_l, total_angle_l = self.get_total_angle(angle_l, self.unitsFC, prev_angle_l, turns_l)
                turns_r, total_angle_r = self.get_total_angle(angle_r, self.unitsFC, prev_angle_r, turns_r)

                #### Controller right wheel

                ## Position Controll
                #Er = SP - PV
                error_r_p = target_angle_r - total_angle_r
                #print(error_r_p)
                #Deadband-Filter to remove stuttering forward and backward after reaching the position
                if error_r_p <= 1 and error_r_p >= -1:
                    error_r_p = 0
                #I-Part
                sum_error_r_p += error_r_p
                #limit I-Part
                sum_error_r_p = max(min(20, sum_error_r_p), -20)

                #PID-Controller
                output_r_p = Kp_p * error_r_p + Ki_p * sampling_time * sum_error_r_p + Kd_p / sampling_time * (error_r_p - error_r_p_old)
                #limit output of position control to speed range
                output_r_p = max(min(1, output_r_p), -1)
                #print(output_r_p)

                error_r_p_old = error_r_p

                ## Speed Controll
                #convert range output_r_p from -1 to 1 to ticks/s
                output_r_p_con = 650 * output_r_p
                #ticks per second (ticks/s), as a moving median window with 5 values
                ticks_r = (total_angle_r - prev_total_angle_r) / sampling_time
                list_ticks_r.append(ticks_r)
                list_ticks_r = list_ticks_r[-5:]
                ticks_r = statistics.median(list_ticks_r)
                
                #Er = SP - PV
                error_r_s = output_r_p_con - ticks_r

                #I-Part
                sum_error_r_s += error_r_s
                #limit I-Part
                #sum_error_r_s = max(min(650/Ki_s, sum_error_r_s), -650/Ki_s)

                #PID-Controller
                output_r_s = Kp_s * error_r_s + Ki_s * sampling_time * sum_error_r_s + Kd_s / sampling_time * (error_r_s - error_r_s_old)

                error_r_s_old = error_r_s

                #convert range output_r_s fom ticks/s to -1 to 1
                output_r_s_con = output_r_s / 650

                self.set_speed_r(output_r_s_con)

                #### Controller left wheel
                
                ## Position Control
                #Er = SP - PV
                error_l_p = target_angle_l - total_angle_l
                #Deadband-Filter to remove stuttering forward and backward after reaching the position
                if error_l_p <= 1 and error_l_p >= -1:
                    error_l_p = 0
                #I-Part
                sum_error_l_p += error_l_p

                #limit I-Part
                sum_error_l_p = max(min(20, sum_error_l_p), -20)

                #PI-Controller
                output_l_p = Kp_p * error_l_p + Ki_p * sampling_time * sum_error_l_p + Kd_p / sampling_time * (error_l_p - error_l_p_old)
                #limit output of position control to speed range
                output_l_p = max(min(1, output_l_p), -1)

                error_l_p_old = error_l_p

                ## Speed Controll
                #convert range output_r_p from -1 to 1 to ticks/s
                output_l_p_con = 650 * output_l_p
                #ticks per second (ticks/s), as a moving median window with 5 values
                ticks_l = (total_angle_l - prev_total_angle_l) / sampling_time
                list_ticks_l.append(ticks_l)
                list_ticks_l = list_ticks_l[-5:]
                ticks_l = statistics.median(list_ticks_l)
                #Er = SP - PV
                error_l_s = output_l_p_con - ticks_l

                #I-Part
                sum_error_l_s += error_l_s
                #limit I-Part
                #sum_error_l_s = max(min(650/Ki_s, sum_error_l_s), -650/Ki_s)

                #PI-Controller
                output_l_s = Kp_s * error_l_s + Ki_s * sampling_time * sum_error_l_s + Kd_s / sampling_time * (error_l_s - error_l_s_old)

                error_l_s_old = error_l_s

                #convert range output_r_s fom ticks/s to -1 to 1
                output_l_s_con = output_l_s / 650

                self.set_speed_l(output_l_s_con)
                #self.set_speed_l(0.5)

            except Exception:
                pass

            prev_angle_l = angle_l
            prev_angle_r = angle_r

            #first run of while true loop, no total_angle_ is calcualted, because prev_angle_ is not available
            try:
                prev_total_angle_l = total_angle_l
                prev_total_angle_r = total_angle_r
            except Exception:
                pass

            #### todo ####
            # modify the stopping condition, so that both wheels have to be at the set-point
            # and not just the right wheel. At moment the control loop stops even if left
            # wheel has not reached the set-point, this causes inaccuracies while moving!!!
            try:
                if total_angle_r >= target_angle_r and number_ticks >= 0:

                    self.set_speed_r(0.0)
                    self.set_speed_l(0.0)
                    position_reached = True

                elif total_angle_r <= target_angle_r and number_ticks <= 0:
                    
                    self.set_speed_r(0.0)
                    self.set_speed_l(0.0)
                    position_reached = True

            except Exception:
                pass

            #Pause outer control loop to wait for changes in the system
            #https://stackoverflow.com/questions/474528/what-is-the-best-way-to-repeatedly-execute-a-function-every-x-seconds-in-python/25251804#25251804
            time.sleep(sampling_time - ((time.time() - start_time) % sampling_time))

            #DEBUGGING OPTION: printing runtime of loop, see beginning of while true loop
            #print('{:.20f}'.format((time.time() - start_time_each_loop)))
        
        return None

    def cancel(self):
        """
        Cancel the started callback function.

        This method cancels the started callback function if initializing an object.
        As written in the pigpio callback_ documentation, the callback function may be cancelled
        by calling the cancel function after the created instance is not needed anymore, see examples 
        in the source code.

        .. _callback: http://abyz.me.uk/rpi/pigpio/python.html#callback
        """

        self.l_wheel.cancel()
        self.r_wheel.cancel()

if __name__ == '__main__':

    pi = pigpio.pi()

    robot = motion(pi = pi)

    a = 0
    while a < 4:
        robot.turn(45)
        time.sleep(1)
        a+=1

    robot.straight(200)
    time.sleep(1)
    robot.straight(-200)
    time.sleep(1)
    
    a = 0
    while a < 2:
        robot.turn(-90)
        time.sleep(1)
        a+=1

    #http://abyz.me.uk/rpi/pigpio/python.html#callback
    robot.cancel()

    #http://abyz.me.uk/rpi/pigpio/python.html#stop
    pi.stop()
