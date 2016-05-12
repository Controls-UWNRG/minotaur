import math as math
import array as array
import log as log
import serial as serial
import serial.tools.list_ports as list_ports
import struct as struct
import time as time
import thread as thread

DEFAULT_SPEED = 100
overshoot = 300

def getOvershootTime(self, max_speed):
    return overshoot / self.__actuator_speed_to_actual_speed(max_speed)

def get_default_speed():
    return DEFAULT_SPEED #do better

def _convert_bytes_to_int(byte_array):
    """ Returns a signed integer from a bytearray type (little endian)

    Keyword Arguments:
    byte_array -- array of 4 bytes

    """
    return struct.unpack('<i', array.array('B', byte_array))[0]

    def act_move(self, device, bytes):
        log.log_info("Moving actuators in ??? direction (needs testing)")
        self.__issue_command(
            device,
            22, bytes[0], bytes[1], bytes[2], bytes[3]
        )
        print "move"

    def stop(self, device):
        log.log_info("Stopping actuators")
        self.__issue_command(
            device,
            23, 0, 0, 0, 0
        )

    def save_start_position(self):
        """
        Store current position in register 0,
        to be used to return to in return_to_start_position
        """
        self.__issue_command(
            self.__x_device,
            16, 0, 0, 0, 0
        )
        self.__issue_command(
            self.__y_device,
            16, 0, 0, 0, 0
        )

    def return_to_start_position(self):
        """
        Returns to stored position in register 0 (previously saved start position),
        set in save_start_position
        """
        self.__issue_command(
            self.__x_device,
            18, 0, 0, 0, 0
        )

        self.__issue_command(
            self.__y_device,
            18, 0, 0, 0, 0
        )

def _convert_int_to_bytes(i):
    """ Returns a bytearray (little endian) from a signed integer

    Keyword Arguments:
    i -- integer to be converted

    """
    return array.array('B', struct.pack('<i', i))

def get_available_com_ports():
    """ Returns a list of all available com-ports """
    return list(list_ports.comports())

class Actuators():
    """ Actuator Controller

    Attributes:
    _SETTINGS -- Settings that can be changed on the actuators. Available
                 settings to add can be found at:
                 http://www.zaber.com/wiki/Manuals/T-LSR#Detailed_Command_Reference
    __properties -- A dictionary utilizing lazy load to speed up accessing of
                    actuator settings
    """
    _SETTINGS = {"MAX_POSITION":44,
                 "ACCELERATION":43,
                 "HOME_OFFSET":47,
                 "SPEED":42,
                 "RETURN_CURRENT_POSITION":45}
    __properties = {}
    __in_x_movement = False
    __x_direction = 0
    __in_y_movement = False
    __y_direction = 0
    __step_size = 1.984375
    __variable_step_size = DEFAULT_SPEED

    def get_step(self):
        return self.__variable_step_size

    def step_change(self, new_value, increment):
        if new_value != None and new_value >= 0:
            log.log_info("Changing step size to " + str(new_value))
            self.__variable_step_size = new_value

        if increment != None:
            temp = self.__variable_step_size + increment

            if temp < 0:
                temp = 0

            log.log_info("Changing step size from " + str(self.__variable_step_size) + " to " + str(temp))
            self.__variable_step_size = temp

    def __align_to_y(self, loc, ir, inv=0):
        """ Align to either TOP=0, MID=1, or BOT=2 """
        # How strict we are about being lined up with gates
        align_threshold = 5

        y_delay = 0.03
        y_max_speed = 300.0
        y_up = _convert_int_to_bytes(y_max_speed)
        y_down = _convert_int_to_bytes(-y_max_speed)

        # Get initial distance from alignment
        dist = ir.get_distance_to_alignment_y(loc)

        while (math.fabs(dist) > align_threshold):
            #time.sleep(0.5) # TODO: Tweak/remove
            print(dist)

            if (inv == 0):
                if dist < 0: # TODO: What about inversion?
                    print("Moving up!")
                    #starts moving the robot down to compensate
                    self.__issue_command(self.__y_device,
                                         22,
                                         y_up[0],
                                         y_up[1],
                                         y_up[2],
                                         y_up[3])
                    time.sleep(y_delay)
                    self.__issue_command(self.__y_device,
                                         23,
                                         0,
                                         0,
                                         0,
                                         0)

                else:
                    print("Moving down!") # Not entirely accurate (inversion)
                    self.__issue_command(self.__y_device,
                                         22,
                                         y_down[0],
                                         y_down[1],
                                         y_down[2],
                                         y_down[3])
                    # TODO: Ideally should be able to remove the stops after each step
                    time.sleep(y_delay)
                    self.__issue_command(self.__y_device,
                                         23,
                                         0,
                                         0,
                                         0,
                                         0)
            else:
                if dist < 0: # TODO: What about inversion?
                    print("Moving up!")
                    #starts moving the robot down to compensate
                    self.__issue_command(self.__y_device,
                                         22,
                                         y_down[0],
                                         y_down[1],
                                         y_down[2],
                                         y_down[3])
                    time.sleep(y_delay)
                    self.__issue_command(self.__y_device,
                                         23,
                                         0,
                                         0,
                                         0,
                                         0)

                else:
                    print("Moving down!") # Not entirely accurate (inversion)
                    self.__issue_command(self.__y_device,
                                         22,
                                         y_up[0],
                                         y_up[1],
                                         y_up[2],
                                         y_up[3])
                    # TODO: Ideally should be able to remove the stops after each step
                    time.sleep(y_delay)
                    self.__issue_command(self.__y_device,
                                         23,
                                         0,
                                         0,
                                         0,
                                         0)


            dist = ir.get_distance_to_alignment_y(loc)

        # Ensure we've stopped
        self.__issue_command(self.__y_device,
                             23,
                             0,
                             0,
                             0,
                             0)
        print ("Aligned on Y-axis!")

    def __align_to_x(self, loc, ir, inv=0):
        """ Align to either LEFT=0, L_MID=1, R_MID=2, or RIGHT=2 """
        # How strict we are about being lined up with gates
        align_threshold = 5

        x_delay = 0.03
        x_max_speed = 300.0

        #stores the movements for the specified directions
        x_right = _convert_int_to_bytes(x_max_speed)
        x_left = _convert_int_to_bytes(-x_max_speed)

        # Get initial distance from alignment
        dist = ir.get_distance_to_alignment_x(loc)

        while (math.fabs(dist) > align_threshold):
            #time.sleep(0.5) # TODO: Tweak/remove
            print(dist)

            if (inv == 0):
                if dist < 0: # TODO: What about inversion?
                    print("Moving right!")
                    #starts moving the robot down to compensate
                    self.__issue_command(self.__x_device,
                                         22,
                                         x_right[0],
                                         x_right[1],
                                         x_right[2],
                                         x_right[3])
                    time.sleep(x_delay)
                    # TODO: Ideally should be able to remove the stops after each step
                    self.__issue_command(self.__x_device,
                                         23,
                                         0,
                                         0,
                                         0,
                                         0)

                else:
                    print("Moving left!") # Not entirely accurate (inversion)
                    self.__issue_command(self.__x_device,
                                         22,
                                         x_left[0],
                                         x_left[1],
                                         x_left[2],
                                         x_left[3])
                    time.sleep(x_delay)
                    self.__issue_command(self.__x_device,
                                         23,
                                         0,
                                         0,
                                         0,
                                         0)
            else:
                if dist < 0: # TODO: What about inversion?
                    print("Moving right!")
                    #starts moving the robot down to compensate
                    self.__issue_command(self.__x_device,
                                         22,
                                         x_left[0],
                                         x_left[1],
                                         x_left[2],
                                         x_left[3])
                    time.sleep(x_delay)
                    # TODO: Ideally should be able to remove the stops after each step
                    self.__issue_command(self.__x_device,
                                         23,
                                         0,
                                         0,
                                         0,
                                         0)

                else:
                    print("Moving left!") # Not entirely accurate (inversion)
                    self.__issue_command(self.__x_device,
                                         22,
                                         x_right[0],
                                         x_right[1],
                                         x_right[2],
                                         x_right[3])
                    time.sleep(x_delay)
                    self.__issue_command(self.__x_device,
                                         23,
                                         0,
                                         0,
                                         0,
                                         0)

            dist = ir.get_distance_to_alignment_x(loc)

        self.__issue_command(self.__x_device,
                             23,
                             0,
                             0,
                             0,
                             0)
        print ("Aligned on x-axis!")

    def maze_navigate(self, ir, sequence, inverted_x_axis, inverted_y_axis):
        log.log_info("Engaging actuators...")
        log.log_info("Sequence: " + (str)(sequence))

        ir.get_field_from_frame(ir.get_frame())

        # TODO: Plumb into parameter
        inv_x = 0
        inv_y = 0

        # TODO: Larger moves when further away
        # TODO: Ideally, we'd use the time while we're moving to run image recognition.
        # TODO: Handle inversion correctly.
        # TODO: Log results in-program.

        self.__align_to_y(sequence[0], ir, inv_y) # Align on left
        self.__align_to_x(1, ir, inv_x) # Align in middle-left x region

        log.log_info("Passed gate 1!")

        self.__align_to_y(sequence[1], ir, inv_y) # Alig on middle-left
        self.__align_to_x(2, ir, inv_x) # Align in middle-right x regio

        log.log_info("Passed gate 2!")

        self.__align_to_y(sequence[2], ir, inv_y) # Align on middle-right
        self.__align_to_x(3, ir, inv_x) # Hop to the right

        log.log_info("Passed gate 3!")

        self.__align_to_y(sequence[3], ir, inv_y) # Align on the right
        self.__align_to_x(2, ir, inv_x) # Hop to the left

        log.log_info("Passed gate 4!")

        self.__align_to_y(sequence[4], ir, inv_y) # Align on middle-right
        self.__align_to_x(1, ir, inv_x) # Hop to the left

        log.log_info("Passed gate 5!")

        self.__align_to_y(sequence[5], ir, inv_y) # Align on middle-left
        self.__align_to_x(0, ir, inv_x) # Hop to the left

        log.log_info("Passed gate 6!")

        self.__issue_command(self.__x_device,
                             23,
                             0,
                             0,
                             0,
                             0)
        self.__issue_command(self.__y_device,
                             23,
                             0,
                             0,
                             0,
                             0)
        log.log_info("Maze navigated!")

    def getOvershootTime(self, max_speed):
        return overshoot / self.__actuator_speed_to_actual_speed(max_speed)

    def move_to_circle_start(self, inverted_x_axis, inverted_y_axis):
        """ Move from top-right corner to the start of the circle path """
        #limits the speeds so that the robot can use a constant speed in each direction
        x_max_speed = 250.0

        #stores the movements for the specified directions
        x_right = _convert_int_to_bytes(x_max_speed)
        x_left = _convert_int_to_bytes(-x_max_speed)

        #the width of the field (from the center of the left section to the center of the right)
        width_distance = 1900 + overshoot + 25
        true_delay = 0.4

        #the time to travel across the field
        x_time = width_distance / self.__actuator_speed_to_actual_speed(x_max_speed)

        ################################################
        # MOVEMENT BEGINS HERE
        ################################################

        # Start moving left
        self.__issue_command(self.__x_device,
                             22,
                             x_left[0],
                             x_left[1],
                             x_left[2],
                             x_left[3])
        time.sleep(x_time)
        # Stop x movement
        self.__issue_command(self.__x_device,
                             23,
                             0,
                             0,
                             0,
                             0)

        # Correct overshoot
        self.__issue_command(self.__x_device,
                             22,
                             x_right[0],
                             x_right[1],
                             x_right[2],
                             x_right[3])
        time.sleep(self.getOvershootTime(x_max_speed))

        # Stop the overshoot
        self.__issue_command(self.__x_device,
                             23,
                             0,
                             0,
                             0,
                             0)

        time.sleep(true_delay)

    def move_to_top_right(self, inverted_x_axis, inverted_y_axis):
        """ Move from start of the circle path to the top-right corner """
        #limits the speeds so that the robot can use a constant speed in each direction
        x_max_speed = 250.0

        #stores the movements for the specified directions
        x_right = _convert_int_to_bytes(x_max_speed)
        x_left = _convert_int_to_bytes(-x_max_speed)

        #the width of the field (from the center of the left section to the center of the right)
        width_distance = 1900 + overshoot + 25
        true_delay = 0.4

        #the time to travel across the field
        x_time = width_distance / self.__actuator_speed_to_actual_speed(x_max_speed)

        ################################################
        # MOVEMENT BEGINS HERE
        ################################################
        # Start moving right
        time.sleep(true_delay)
        self.__issue_command(self.__x_device,
                             22,
                             x_right[0],
                             x_right[1],
                             x_right[2],
                             x_right[3])
        time.sleep(x_time)
        # Stop x movement
        self.__issue_command(self.__x_device,
                             23,
                             0,
                             0,
                             0,
                             0)

        # Correct overshoot
        self.__issue_command(self.__x_device,
                             22,
                             x_left[0],
                             x_left[1],
                             x_left[2],
                             x_left[3])
        time.sleep(self.getOvershootTime(x_max_speed))

        # Stop the overshoot
        self.__issue_command(self.__x_device,
                             23,
                             0,
                             0,
                             0,
                             0)


        time.sleep(true_delay)

    def circle_path(self, inverted_x_axis, inverted_y_axis, radius, start, end):
        '''This function should cause the robot to travel in a circle. It uses derivatives to determine speed.
        I have no idea if it will work (Not sure what I am doing with the actuators is sound). If that works
        you will have to play around with the constants.
        If the actuator command code fails, we will need to add more sleeps between each call and decrease the delay and
        decrease the angle increment.'''

        radius = radius * 2000.0
        x_multiplier = 0.13
        y_multiplier = 0.41
        angle = start
        delay = 0.0001
        current_time = 0
        total_time = (end - start) * 0.0075 / 360
        angle_increment = 5

        #handle CW paths
        if total_time < 0:
            total_time = -1 * total_time
            angle_increment = -5

        def get_new_x_speed(theta):
            return (-1)*radius*math.sin(math.radians(theta))

        def get_new_y_speed(theta):
            return radius*math.cos(math.radians(theta))

        while current_time < total_time:
            x_speed = _convert_int_to_bytes(get_new_x_speed(angle)*x_multiplier)
            y_speed = _convert_int_to_bytes(get_new_y_speed(angle)*y_multiplier)
            self.__issue_command(
                self.__x_device,
                22,
                x_speed[0],
                x_speed[1],
                x_speed[2],
                x_speed[3],
            )
            self.__issue_command(
                self.__y_device,
                22,
                y_speed[0],
                y_speed[1],
                y_speed[2],
                y_speed[3],
            )
            time.sleep(delay)
            self.__issue_command(
                self.__y_device,
                23,
                0,
                0,
                0,
                0
            )
            self.__issue_command(
                self.__x_device,
                23,
                0,
                0,
                0,
                0
            )
            #bootleg shifting right is needed
            #self.__issue_command(
            #    self.__x_device,
            #    22,
            #    100,
            #    100,
            #    100,
            #    100,
            #)
            self.__issue_command(
                self.__x_device,
                23,
                0,
                0,
                0,
                0
            )

            angle = angle + angle_increment
            current_time = current_time + delay

        # Return to stored position in register 0 (starting position)
        self.__issue_command(
            self.__x_device,
            18,
            0,
            0,
            0,
            0,
        )
        self.__issue_command(
            self.__y_device,
            18,
            0,
            0,
            0,
            0,
        )

    def triangle_path(self, inverted_x_axis, inverted_y_axis):
        """ TODO: Need to overshoot target corners, then pull back before making the next move """
        #height: 2mm or 2000+-20um
        #length: 1.25mm or 1250+-20um
        #path(not included in above): 10+-5um
        #landmark diameter: 20+-5um

        #limits the speeds so that the robot can use a constant speed in each direction
        max_speed = 700.0*0.6

        triangle_y_max_speed = 650.0*0.95*0.65
        triangle_x_max_speed = 450.0*0.95*0.65

        #stores the movements for the specified directions
        x_left = _convert_int_to_bytes(-max_speed)
        x_right = _convert_int_to_bytes(max_speed)
        y_down = _convert_int_to_bytes(-max_speed)
        y_up = _convert_int_to_bytes(max_speed)

        x_hypo = _convert_int_to_bytes(triangle_x_max_speed)
        y_hypo = _convert_int_to_bytes(triangle_y_max_speed)

        #the delay for the first command to be processed
        #start_delay = 0.013
        true_delay = 0.50

        #height of the field (from the center of one gate to the center of the one below)
        height_distance = 2100.0 + overshoot# 2000 is actual distance

        #the width of the field (from the center of the left section to the center of the right)
        width_distance = 1200.0 + overshoot - 80# 1250 is actual distance

        #the time to travel across the field
        x_time = width_distance / self.__actuator_speed_to_actual_speed(max_speed)

        #the time to travel the height of the field
        y_time = height_distance / self.__actuator_speed_to_actual_speed(max_speed)

        # Note this is not /quite/ accurate as we aren't actually tavelling at max_speed
        diag_time = math.sqrt(math.pow(width_distance,2) + math.pow(height_distance,2)) / self.__actuator_speed_to_actual_speed(max_speed+100);

        # Store current position in register 0
        self.__issue_command(
            self.__x_device,
            16,
            0,
            0,
            0,
            0,
        )
        self.__issue_command(
            self.__y_device,
            16,
            0,
            0,
            0,
            0,
        )

        ################################################
        # MOVEMENT BEGINS HERE
        ################################################

        # Start moving down
        self.__issue_command(self.__y_device,
                             22,
                             y_down[0],
                             y_down[1],
                             y_down[2],
                             y_down[3])
        time.sleep(y_time)
        # Stop y movement
        self.__issue_command(self.__y_device,
                             23,
                             0,
                             0,
                             0,
                             0)

        # Correct overshoot
        self.__issue_command(self.__y_device,
                             22,
                             y_up[0],
                             y_up[1],
                             y_up[2],
                             y_up[3])
        time.sleep(self.getOvershootTime(max_speed))
        # Stop the overshoot
        self.__issue_command(self.__y_device,
                             23,
                             0,
                             0,
                             0,
                             0)

        time.sleep(true_delay)

        # Start moving left
        self.__issue_command(self.__x_device,
                             22,
                             x_left[0],
                             x_left[1],
                             x_left[2],
                             x_left[3])
        time.sleep(x_time)

        # Stop the robots x movement
        self.__issue_command(self.__x_device,
                             23,
                             0,
                             0,
                             0,
                             0)


        # Correct overshoot
        self.__issue_command(self.__x_device,
                             22,
                             x_right[0],
                             x_right[1],
                             x_right[2],
                             x_right[3])
        time.sleep(self.getOvershootTime(max_speed))

        # Stop overshoot
        self.__issue_command(self.__x_device,
                             23,
                             0,
                             0,
                             0,
                             0)

        time.sleep(true_delay)

        # TODO: Synchronize start and synchronize stop
        # Start moving diagonally
        thread.start_new_thread(self.__issue_command, (self.__y_device, 22, y_hypo[0], y_hypo[1], y_hypo[2], y_hypo[3],));
        thread.start_new_thread(self.__issue_command, (self.__x_device, 22, x_hypo[0], x_hypo[1], x_hypo[2], x_hypo[3],));

        time.sleep(diag_time)

        #stops y and x movement as the robot is done
        self.__issue_command(self.__y_device,
                             23,
                             0,
                             0,
                             0,
                             0)
        self.__issue_command(self.__x_device,
                             23,
                             0,
                             0,
                             0,
                             0)

        #thread.start_new_thread(self)

        # Correct overshoot for the y axis
        self.__issue_command(self.__y_device,
                             22,
                             y_down[0],
                             y_down[1],
                             y_down[2],
                             y_down[3])
        time.sleep(self.getOvershootTime(triangle_y_max_speed))
        # Stop the overshoot
        self.__issue_command(self.__y_device,
                             23,
                             0,
                             0,
                             0,
                             0)

        #start the overshoot for the x axis
        self.__issue_command(self.__x_device,
                             22,
                             x_left[0],
                             x_left[1],
                             x_left[2],
                             x_left[3])
        time.sleep(self.getOvershootTime(triangle_x_max_speed))

        # Stop overshoot
        self.__issue_command(self.__x_device,
                             23,
                             0,
                             0,
                             0,
                             0)

        time.sleep(true_delay)

        # Return to stored position in register 0 (starting position)
        self.__issue_command(
            self.__x_device,
            18,
            0,
            0,
            0,
            0,
        )
        self.__issue_command(
            self.__y_device,
            18,
            0,
            0,
            0,
            0,
        )
        time.sleep(true_delay)

    def movement(self, num, direction, byte, delay):
        """
        num = actuator movement control value (documentation from Zaber online)
        direction = left, right, up, down (currently only in 2D)
        byte = movement for specific direction
        delay = delay for the actuator before changing directions/commands
        """

        #Movement in a given direction
        if direction == "left" or direction == "right":
            self.__issue_command(
                self.__x_device,
                num,
                byte[0],
                byte[1],
                byte[2],
                byte[3],
            )
            time.sleep(delay)
            self.__issue_command(   #stop actuators
                self.__x_device,
                23,
                0,
                0,
                0,
                0,
            )
            time.sleep(delay)

            #Actuators overshoot error
        else:
            self.__issue_command(   #left or right movement
                self.__y_device,
                num,
                byte[0],
                byte[1],
                byte[2],
                byte[3],
            )
            time.sleep(delay)
            self.__issue_command(   #stop actuators
                self.__y_device,
                23,
                0,
                0,
                0,
                0,
            )
            time.sleep(delay)

    def box_path(self, inverted_x_axis, inverted_y_axis):
        #length: 3mm or 3000+-20um
        #height: 2mm or 2000+-20um
        #path(not included in above): 10+-5um
        #landmark diameter: 20+-5um

        #limits the speeds so that the robot can use a constant speed in each direction
        max_speed = 400.0*0.6 #250.0 #accurate to 20um

        #stores the movements for the specified directions
        x_right = _convert_int_to_bytes(max_speed)
        x_left = _convert_int_to_bytes(-max_speed)
        y_up = _convert_int_to_bytes(max_speed)
        y_down = _convert_int_to_bytes(-max_speed)

        true_delay = 1.000
        errorTime = 0.1

        #height of the field (from the center of one gate to the center of the one below)
        height_distance = 1950.0 + overshoot

        #the width of the field (from the center of the left section to the center of the right)
        width_distance = 3050.0 - 100 + overshoot

        #the time to travel across the field
        x_time = width_distance / self.__actuator_speed_to_actual_speed(max_speed)
        #the time to travel the height of the field
        y_time = height_distance / self.__actuator_speed_to_actual_speed(max_speed)

        overshoot_time = self.getOvershootTime(max_speed)#overshoot / self.__actuator_speed_to_actual_speed(max_speed)

        # Store current position in register 0
        self.__issue_command(
            self.__x_device,
            16,
            0,
            0,
            0,
            0,
        )
        self.__issue_command(
            self.__y_device,
            16,
            0,
            0,
            0,
            0,
        )

        ################################################
        # MOVEMENT BEGINS HERE
        ################################################

        # Start moving left
        self.__issue_command(self.__x_device,
                             22,
                             x_left[0],
                             x_left[1],
                             x_left[2],
                             x_left[3])
        time.sleep(x_time)
        # Stop x movement
        self.__issue_command(self.__x_device,
                             23,
                             0,
                             0,
                             0,
                             0)

        # Correct the overshoot
        self.__issue_command(self.__x_device,
                             22,
                             x_right[0],
                             x_right[1],
                             x_right[2],
                             x_right[3])
        time.sleep(overshoot_time)
        # Stop x movement
        self.__issue_command(self.__x_device,
                             23,
                             0,
                             0,
                             0,
                             0)

        time.sleep(true_delay)
        # Start moving downward
        self.__issue_command(self.__y_device,
                             22,
                             y_down[0],
                             y_down[1],
                             y_down[2],
                             y_down[3])
        time.sleep(y_time)
        # Stop the robots y movement
        self.__issue_command(self.__y_device,
                             23,
                             0,
                             0,
                             0,
                             0)

        # Correct the overshoot
        self.__issue_command(self.__y_device,
                             22,
                             y_up[0],
                             y_up[1],
                             y_up[2],
                             y_up[3])
        time.sleep(overshoot_time)

        # Stop y movement
        self.__issue_command(self.__y_device,
                             23,
                             0,
                             0,
                             0,
                             0)

        time.sleep(true_delay)


        # Start moving right
        self.__issue_command(self.__x_device,
                             22,
                             x_right[0],
                             x_right[1],
                             x_right[2],
                             x_right[3])
        time.sleep(x_time)
        # Stop x movement
        self.__issue_command(self.__x_device,
                             23,
                             0,
                             0,
                             0,
                             0)
        # Correct the overshoot
        self.__issue_command(self.__x_device,
                             22,
                             x_left[0],
                             x_left[1],
                             x_left[2],
                             x_left[3])
        time.sleep(overshoot_time)
        # Stop x movement
        self.__issue_command(self.__x_device,
                             23,
                             0,
                             0,
                             0,
                             0)

        time.sleep(true_delay)
        # Start moving upward
        self.__issue_command(self.__y_device,
                             22,
                             y_up[0],
                             y_up[1],
                             y_up[2],
                             y_up[3])
        time.sleep(y_time)
        # Stop the robots y movement
        self.__issue_command(self.__y_device,
                             23,
                             0,
                             0,
                             0,
                             0)
        time.sleep(true_delay)
        # Correct the overshoot
        self.__issue_command(self.__y_device,
                             22,
                             y_down[0],
                             y_down[1],
                             y_down[2],
                             y_down[3])
        time.sleep(overshoot_time)
        # Stop y movement
        self.__issue_command(self.__y_device,
                             23,
                             0,
                             0,
                             0,
                             0)

        #stops y and x movement as the robot is done
        self.__issue_command(self.__y_device,
                             23,
                             0,
                             0,
                             0,
                             0)
        self.__issue_command(self.__x_device,
                             23,
                             0,
                             0,
                             0,
                             0)

        # Return to stored position in register 0 (starting position)
        self.__issue_command(
            self.__x_device,
            18,
            0,
            0,
            0,
            0,
        )
        self.__issue_command(
            self.__y_device,
            18,
            0,
            0,
            0,
            0,
        )

        time.sleep(true_delay)

    def figure_eight(self, inverted_x_axis, inverted_y_axis):
        #limits the speeds so that the robot can use a constant speed in each direction
        y_max_speed = 3000.0
        x_max_speed = 1200.0

        #stores the movements for the specified directions
        x_right = _convert_int_to_bytes(x_max_speed)
        x_left = _convert_int_to_bytes(-x_max_speed)
        y_up = _convert_int_to_bytes(y_max_speed)
        y_down = _convert_int_to_bytes(-y_max_speed)

        #the delay for the first command to be processed
        delay = 0.013

        #height of the field (from the center of one gate to the center of the one below)
        height_distance = 1300.0

        #the width of the field (from the center of the left section to the center of the right)
        width_distance = 3400.0

        #the time to travel across the field
        x_time = width_distance / self.__actuator_speed_to_actual_speed(x_max_speed)

        #the time to travel the height of the field (from center of one gate to the other)
        height_time = height_distance / self.__actuator_speed_to_actual_speed(y_max_speed)

        #the time spent only moving in the x-direction
        flat_time = (x_time - height_time * 2) / 2

        #the initial movement in the x direction
        initial_x_time = x_time - flat_time - height_time * 3 / 2

        #right out of top left gate
        self.__issue_command(self.__x_device,
                             22,
                             x_right[0],
                             x_right[1],
                             x_right[2],
                             x_right[3])

        time.sleep(initial_x_time - delay)

        #starts moving the robot down to bottom right gate
        self.__issue_command(self.__y_device,
                             22,
                             y_down[0],
                             y_down[1],
                             y_down[2],
                             y_down[3])

        time.sleep(height_time)

        #stops the robots y movement so it can go through the gate
        self.__issue_command(self.__y_device,
                             23,
                             0,
                             0,
                             0,
                             0)

        time.sleep(flat_time)

        #starts moving the robot up the right side
        self.__issue_command(self.__y_device,
                             22,
                             y_up[0],
                             y_up[1],
                             y_up[2],
                             y_up[3])

        time.sleep(height_time/2)

        #reverses the x direction of the robot
        self.__issue_command(self.__x_device,
                             22,
                             x_left[0],
                             x_left[1],
                             x_left[2],
                             x_left[3])

        time.sleep(height_time/2)

        #allows the robot to go through the top right gate
        self.__issue_command(self.__y_device,
                             23,
                             0,
                             0,
                             0,
                             0)

        time.sleep(flat_time)

        #starts the robot going down for the bottom left gate
        self.__issue_command(self.__y_device,
                             22,
                             y_down[0],
                             y_down[1],
                             y_down[2],
                             y_down[3])

        time.sleep(height_time)

        #stops y movement so the robot can go through the gate
        self.__issue_command(self.__y_device,
                             23,
                             0,
                             0,
                             0,
                             0)

        time.sleep(flat_time)

        #starts moving the robot up the left channel
        self.__issue_command(self.__y_device,
                             22,
                             y_up[0],
                             y_up[1],
                             y_up[2],
                             y_up[3])

        time.sleep(height_time/2)

        #reverses the robots x direction so it can end in the middle
        self.__issue_command(self.__x_device,
                             22,
                             x_right[0],
                             x_right[1],
                             x_right[2],
                             x_right[3])

        time.sleep(height_time/2)

        #stops y movement so the robot can pass through the upper left gate
        self.__issue_command(self.__y_device,
                             23,
                             0,
                             0,
                             0,
                             0)

        time.sleep(flat_time*3/2)

        #stops x movement as the robot is done
        self.__issue_command(self.__x_device,
                             23,
                             0,
                             0,
                             0,
                             0)

    def __actual_speed_to_actuator_speed(self, speed):
        return speed / 9.375 / self.__step_size

    def __actuator_speed_to_actual_speed(self, speed):
        return speed * 9.375 * self.__step_size

    def flush_buffers(self):
        """ Clears the input and output buffer for the serial connection """
        self.__ser.flushInput()
        self.__ser.flushOutput()

    def get_setting(self, device, setting):
        """ Returns the specified setting's value in a list if multiple devices
        are specified (i.e. device = 0) or a single value if a single device is
        chosen. Utilizes a lazy load system for speed.

        Keyword Arguments:
        device -- The actuator to check the settings of. If 0, check all
                  actuators.
        setting -- The setting to return. Must be one from the self._SETTINGS
                   list.

        """
        if setting in self._SETTINGS:
            if setting not in self.__properties:
                self.__properties[setting] = {}

            #if the device settings are not currently stored
            if (device not in self.__properties[setting] and
                (device != 0 or
                 self.__num_devices != len(self.__properties[setting]))):

                response = self.__issue_command(device,
                                                53,
                                                self._SETTINGS[setting],
                                                0,
                                                0,
                                                0)
                print response

                #updates self.__properties with the returned values
                for response_i in response:
                    temp_val = _convert_bytes_to_int(''.join(response_i[2:]))
                    temp_dev_number = ord(response_i[0])
                    self.__properties[setting][temp_dev_number] = temp_val

            #whether to return a list or a single value
            if device == 0:
                return_val = []

                for i in range(self.__num_devices):
                    return_val.append(self.__properties[setting][i + 1])
            else:
                return_val = self.__properties[setting][device]

            return return_val
        else:
            log.log_error("The specified setting '{0}' is not currently " \
                          "supported".format(setting))

    def __init__(self, com_port):
        """ Initializes Actuator Control

        Keyword Arguments:
        com_port -- The com-port the actuators are on.
        num_devices -- The number of actuators being used.

        """
        self.__ser = serial.Serial(com_port)
        self.flush_buffers()

        self.__x_device = 1
        self.__y_device = 2

        self.__num_devices = None
        #TODO: Are we sure it's okay not to issue this command?
        #self.__num_devices = len(self.__issue_command(0, 55, 0, 0, 0, 0))
        log.log_info("Actuators have been initialized.")

    def __issue_command(self, b_0, b_1, b_2, b_3, b_4, b_5):
        """ Sends 6 bytes of information to the actuators. It returns the
        response from the actuators. Available commands can be found at:
        http://www.zaber.com/wiki/Manuals/T-LSR#Detailed_Command_Reference

        Keyword arguments:
        b_i -- the ith byte to send to the actuators
        """
        self.__ser.write(bytearray([b_0, b_1, b_2, b_3, b_4, b_5]))
        return self.__read_input(b_0)

    def end_move(self, vector, invert_x_axis, invert_y_axis):
        """ Given input parameters, moves the robot relative to it's current
        position. It executes first the x component and then the y component.

        Keyword Arguments:
        self -- actuator object the function was called on
        vector -- movement vector
        invert_x_axis -- boolean of whether to invert on the x-axis
        invert_y_axis -- boolean of whether to invert on the y-axis

        """
        if (self.__in_x_movement and vector[0] != 0):
            self.__in_x_movement = False
            self.__x_direction = 0
            log.log_info("stop x")

            #X Axis
            self.__issue_command(self.__x_device,
                                 23,
                                 0,
                                 0,
                                 0,
                                 0)

        if (self.__in_y_movement and vector[1] != 0):
            self.__in_y_movement = False
            self.__y_direction = 0
            log.log_info("stop y")

            #Y Axis
            self.__issue_command(self.__y_device,
                                 23,
                                 0,
                                 0,
                                 0,
                                 0)

    def move(self, vector, invert_x_axis, invert_y_axis):
        """ Given input parameters, moves the robot relative to it's current
        position. It executes first the x component and then the y component.

        Keyword Arguments:
        self -- actuator object the function was called on
        vector -- movement vector
        invert_x_axis -- boolean of whether to invert on the x-axis
        invert_y_axis -- boolean of whether to invert on the y-axis

        """
        vector = [x * self.__variable_step_size for x in vector]

        if (vector[0] != 0 and self.__in_x_movement and self.__x_direction != 0):
            temp = -1 if vector[0] < 0 else 1

            if temp != self.__x_direction:
                self.end_move([temp, 0], invert_x_axis, invert_y_axis)

        if (not self.__in_x_movement and vector[0] != 0):
            self.__in_x_movement = True

            #X Axis
            if invert_x_axis:
                vector[0] *= -1

            log.log_info("start x " + str(vector[0]))

            self.__x_direction = -1 if vector[0] < 0 else 1

            byte_array = _convert_int_to_bytes(vector[0])

            self.__issue_command(self.__x_device,
                                 22,
                                 byte_array[0],
                                 byte_array[1],
                                 byte_array[2],
                                 byte_array[3])

        if (vector[1] != 0 and self.__in_y_movement and self.__y_direction != 0):
            temp = -1 if vector[1] < 0 else 1

            if temp != self.__y_direction:
                self.end_move([0, temp], invert_x_axis, invert_y_axis)

        if (not self.__in_y_movement and vector[1] != 0):
            self.__in_y_movement = True

            #Y Axis
            if invert_y_axis:
                vector[1] *= -1

            log.log_info("start y " + str(vector[1]))

            self.__y_direction = -1 if vector[1] < 0 else 1

            byte_array = _convert_int_to_bytes(vector[1])

            self.__issue_command(self.__y_device,
                                 22,
                                 byte_array[0],
                                 byte_array[1],
                                 byte_array[2],
                                 byte_array[3])

    def move_to(self, position_vector, invert_x_axis, invert_y_axis):
        """ Given input parameters, moves the robot to the specified position.
        It will execute the x component and then the y component.

        Keyword Arguments:
        self -- actuator object the function was called on
        position_vector -- position vector
        invert_x_axis -- boolean of whether to invert on the x-axis
        invert_y_axis -- boolean of whether to invert on the y-axis

        """
        #X Axis
        device = self.__x_device

        """if invert_x_axis:
            max_pos = self.get_setting(device, "MAX_POSITION")
            position_vector[0] = max_pos - position_vector[0]"""

        byte_array = _convert_int_to_bytes(position_vector[0])

        self.__issue_command(device,
                             20,
                             byte_array[0],
                             byte_array[1],
                             byte_array[2],
                             byte_array[3])

        #Y Axis
        device = self.__y_device

        """if invert_y_axis:
            max_pos = self.get_setting(device, "MAX_POSITION")
            position_vector[1] = max_pos - position_vector[1]"""

        byte_array = _convert_int_to_bytes(position_vector[1])

        self.__issue_command(device,
                             20,
                             byte_array[0],
                             byte_array[1],
                             byte_array[2],
                             byte_array[3])

    def __read_input(self, device_num):
        """ Returns input from the actuators. Reads until 6 bytes have
        been read per actuator a response is expected from.

        Keyword arguments:
        device_num -- the device number a response is expected from.

        """
        # TODO: Assess when/whether this should be called when issuing a command
        timeout_limit = 100
        timeout_count = 0

        l=[]
        if device_num:
            l.append(self.__read_byte())
        elif self.__num_devices:
            while len(l) < self.__num_devices:
                l.append(self.__read_byte())
        else:
            time.sleep(1)

            while self.__ser.inWaiting() > 0:
                l.append(self.__read_byte())

        #print l
        return l

    def __read_byte(self):
        """ Reads a byte from the input. """
        temp = []

        #print "Reading bytes..."
        #while len(temp) < 6:
        #    temp.append(self.__ser.read(1)) # TODO: YOLOFUCKIT
        #print "Success."
        #return temp
        return 0

    def renumber_actuators(self):
        """ Sends a command to renumber all the actuators. This must
        be performed after a factory reset of the settings."""
        self.__issue_command(0,2,0,0,0,0)

    def reset_actuators(self):
        """ Factor resets the actuators, flushes the buffers, resets
        all information stored, and returns the actuators to the home
        position. """
        self.__issue_command(0,36,0,0,0,0)
        self.flush_buffers()
        self.__properties = {}
        self.renumber_actuators()
        self.return_to_home(0)

    def return_to_home(self, device):
        """ Returns the specified device to the home position.

        Keyword Arguments:
        device -- the actuator number to send the command to
        """
        self.__issue_command(device,1,0,0,0,0)

    def set_setting(self, device, setting, val):
        """ Sets the desired setting for the desired device to the specified
        value. This will also update the local properties dictionary, thus this
        is the only way settings are allowed to be updated.

        Keyword Arguments:
        device -- the actuator number to send the command to
        setting -- The setting to return. Must be one from the self._SETTINGS
                   list.
        val -- The specified value to set the actuator(s) to.

        """
        if setting in self._SETTINGS:
            byte_array = _convert_int_to_bytes(val)

            self.__issue_command(device,
                                 self._SETTINGS[setting],
                                 byte_array[0],
                                 byte_array[1],
                                 byte_array[2],
                                 byte_array[3])

            if setting not in self.__properties:
                self.__properties[setting] = {}

            if device == 0:
                for i in range(self.__num_devices):
                    self.__properties[setting][i] = val
            else:
                self.__properties[setting][device] = val
        else:
            log.log_error("The specified setting '{0}' is not currently " \
                          "supported".format(setting))

    def switch_actuator_axis(self):
        """ Toggles which device is responsible for x and y axis movement """
        temp = self.__y_device
        self.__y_device = self.__x_device
        self.__x_device = temp

    """
    ---------------------------------------------------------------------------------------------------------------------
    ---------------------------------------------------- ICRA 2016 ------------------------------------------------------
    ---------------------------------------------------------------------------------------------------------------------
    """

    def act_move(self, device, bytes):
        log.log_info("Moving actuators in ??? direction (needs testing)")
        self.__issue_command(
            device,
            22, bytes[0], bytes[1], bytes[2], bytes[3]
        )
        print "move"

    def stop(self, device):
        log.log_info("Stopping actuators")
        self.__issue_command(
            device,
            23, 0, 0, 0, 0
        )

    def save_start_position(self):
        """
        Store current position in register 0,
        to be used to return to in return_to_start_position
        """
        self.__issue_command(
            self.__x_device,
            16, 0, 0, 0, 0
        )
        self.__issue_command(
            self.__y_device,
            16, 0, 0, 0, 0
        )

    def return_to_start_position(self):
        """
        Returns to stored position in register 0 (previously saved start position),
        set in save_start_position
        """
        self.__issue_command(
            self.__x_device,
            18, 0, 0, 0, 0
        )

        self.__issue_command(
            self.__y_device,
            18, 0, 0, 0, 0
        )

    def diagonal_path(self, inverted_x_axis, inverted_y_axis, path_type):  # path_type, x_dir, y_dir, inverted_x_axis, inverted_y_axis):
        """
        For diagonal movement in the mobility challenge.

        Parameters:
        (unused)inverted_y_axis = inversion of actuators for y axis
        (unused)inverted_x_axis = inversion of actuators for x axis
        x_dir = direction string stating "up" or "down"
        y_dir = direction string stating "left" or "right"
        path_type = path type string stating "small" or "large" path (refer to competition field)
        """

        #height: 2mm or 2000+-20um
        #length: 1.25mm or 1250+-20um

        #limits the speeds so that the robot can use a constant speed in each direction
        max_speed = 420.0
        act_overshoot = 300

        triangle_y_max_speed = 400.0
        triangle_x_max_speed = 275.0

        #stores the movements for the specified directions
        x_left = _convert_int_to_bytes(-max_speed)
        x_right = _convert_int_to_bytes(max_speed)  # not used
        y_down = _convert_int_to_bytes(-max_speed)
        y_up = _convert_int_to_bytes(max_speed)  # not used

        x_hypo = _convert_int_to_bytes(triangle_x_max_speed)
        y_hypo = _convert_int_to_bytes(triangle_y_max_speed)

        #the delay for the first command to be processed
        act_delay = 0.50

        if(path_type == "large"):
            #height of the field (from the center of one gate to the center of the one below)
            height_distance = 2100.0 + act_overshoot  # 2000 is actual distance
            #the width of the field (from the center of the left section to the center of the right)
            width_distance = 1200.0 + act_overshoot - 80  # 1250 is actual distance
        elif(path_type == "small"):
            height_distance = 1000.0 + act_overshoot
            width_distance = 500.0 + act_overshoot - 80

        # Note this is not /quite/ accurate as we aren't actually tavelling at max_speed

        diag_time = math.sqrt(
            math.pow(width_distance, 2) + math.pow(height_distance, 2)
            ) / self.__actuator_speed_to_actual_speed(max_speed+100)

        # Store current position in register 0
        #save_start_position()

        ''' Start movement '''
        # TODO: Synchronize start and synchronize stop
        # Start moving diagonally
        thread.start_new_thread(self.act_move, (self.__y_device, y_hypo))
        thread.start_new_thread(self.act_move, (self.__x_device, x_hypo))
        time.sleep(diag_time)

        # Stops y and x movement of actuators
        self.stop(self.__y_device)
        self.stop(self.__x_device)
        ''' End of movement '''

        ''' Overshoot '''
        # Correct overshoot for the y axis
        self.act_move(self.__y_device, y_down)
        time.sleep(self.getOvershootTime(triangle_y_max_speed))
        self.stop(self.__y_device)

        # Correct overshoot for the x axis
        self.act_move(self.__x_device, x_left)
        time.sleep(self.getOvershootTime(triangle_x_max_speed))

        # Stop overshoot
        self.stop(self.__x_device)
        time.sleep(act_delay)
        ''' End of overshoot '''

        # Return to stored start position
        #return_to_start_position()
        time.sleep(act_delay)
<<<<<<< 463aaee0b243d28e731ab9fed2fa0b7218ff0825
=======


>>>>>>> Fix compile time errors
