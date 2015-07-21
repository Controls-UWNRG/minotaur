import log as log
import movement.actuators as actuators
import movement.solenoids as solenoids

_EMMA_ACTUATORS = "EMMA_ACTUATORS"
_EMMA_SOLENOIDS = "EMMA_SOLENOIDS"

class Controller():
    __actuators = None
    __solenoids = None

    def navigate_maze(self, ir, sequence, inverted_x_axis, inverted_y_axis):
        if self.__actuators:
            self.__actuators.maze_navigate(ir, sequence,
                inverted_x_axis, inverted_y_axis)
        else:
            log.log_error("Actuators have not been initialized" \
                          " with a com-port properly.")

    def draw_shapes(self, inverted_x_axis, inverted_y_axis, shape_info):
        for shape in shape_info:
            shape_type = shape["shape"]
            shape_count = shape["count"]
            if shape_type == "circle":
                if (shape_count > 0):
                    self.move_to_circle_start(inverted_x_axis, inverted_y_axis)
            for i in range(0, shape_count):
                if shape_type == "circle":
                    self.circle_path(inverted_x_axis, inverted_y_axis)
                elif shape_type == "triangle":
                    self.triangle_path(inverted_x_axis, inverted_y_axis)
                elif shape_type == "rectangle":
                    self.box_path(inverted_x_axis, inverted_y_axis)
            if shape_type == "circle":
                if (shape_count > 0):
                    self.move_to_top_right(inverted_x_axis, inverted_y_axis)

    def box_path(self, inverted_x_axis, inverted_y_axis):
        if self.__actuators:
            self.__actuators.box_path(inverted_x_axis,
                                          inverted_y_axis)
            #haven't implemented rotation yet
        else:
            log.log_error("Actuators have not been initialized" \
                          " with a com-port properly.")

    def triangle_path(self, inverted_x_axis, inverted_y_axis):
        if self.__actuators:
            self.__actuators.triangle_path(inverted_x_axis,
                                          inverted_y_axis)
            #haven't implemented rotation yet
        else:
            log.log_error("Actuators have not been initialized" \
                          " with a com-port properly.")

    def circle_path(self, inverted_x_axis, inverted_y_axis):
        if self.__actuators:
            self.__actuators.circle_path(inverted_x_axis,
                                          inverted_y_axis)
        else:
            log.log_error("Actuators have not been initialized" \
                          " with a com-port properly.")

    def move_to_circle_start(self, inverted_x_axis, inverted_y_axis):
        if self.__actuators:
            self.__actuators.move_to_circle_start(inverted_x_axis,
                                          inverted_y_axis)
        else:
            log.log_error("Actuators have not been initialized" \
                          " with a com-port properly.")

    def move_to_top_right(self, inverted_x_axis, inverted_y_axis):
        if self.__actuators:
            self.__actuators.move_to_top_right(inverted_x_axis,
                                          inverted_y_axis)
        else:
            log.log_error("Actuators have not been initialized" \
                          " with a com-port properly.")
            
    def figure_eight(self, inverted_x_axis, inverted_y_axis):
        if self.__actuators:
            self.__actuators.figure_eight(inverted_x_axis,
                                          inverted_y_axis)
            #haven't implemented rotation yet
        else:
            log.log_error("Actuators have not been initialized" \
                          " with a com-port properly.")

    def get_available_com_ports(self):
        """ Returns a list of available com-ports """
        return actuators.get_available_com_ports()

    def __init__(self):
        """ Initializes the Controller to use the magnet schema """
        self.__control_schema = _EMMA_ACTUATORS

    def initialize_actuators(self, com_port):
        """ Initializes the actuators given their com-port and the number of
        actuators.

        Keyword Arguments:
        com_port -- The com-port to use to connect to the actuators.

        """
        if not self.__actuators:
            self.__actuators = actuators.Actuators(com_port)
    
    def initialize_solenoids(self):
        """ Initializes the actuators given their com-port and the number of
        actuators.

        Keyword Arguments:
        com_port -- The com-port to use to connect to the actuators.

        """
        if not self.__solenoids:
            self.__solenoids = solenoids.Solenoids()

    def speed_change(self, new_value, increment):
        """  Changes the speed of movement for the controller

        Keyword Arguments:
        increment -- whether the speed is increasing (1) or decreasing (-1)

        """
        if self.__control_schema == _EMMA_ACTUATORS:
            if self.__actuators:
                self.__actuators.step_change(new_value, increment)
            else:
                log.log_error("Actuators have not been initialized" \
                              " with a com-port properly.")

    def get_speed(self):
        if self.__control_schema == _EMMA_ACTUATORS:
            if self.__actuators:
                return self.__actuators.get_step()
            else:
                return actuators.get_default_speed()

    def end_move(self, vector, inverted_x_axis, inverted_y_axis):
        """ Sends the movement instruction to the appropriate control system

        Keyword Arguments:
        vector -- movement vector
        invert_x_axis -- boolean of whether to invert on the x-axis
        invert_y_axis -- boolean of whether to invert on the y-axis

        """
        if self.__control_schema == _EMMA_ACTUATORS:
            if len(vector) != 3:
                log.log_error("3 arguments were expected, " \
                              "{0} were given.".format(len(vector)))
                return

            if self.__actuators:
                self.__actuators.end_move(vector[:2],
                                      inverted_x_axis,
                                      inverted_y_axis)
                #haven't implemented rotation yet
            else:
                log.log_error("Actuators have not been initialized" \
                              " with a com-port properly.")
        elif self.__control_schema == _EMMA_SOLENOIDS:
            if len(vector) != 3:
                log.log_error("3 arguments were expected, " \
                              "{0} were given.".format(len(vector)))
                return

            if self.__solenoids:
                self.__solenoids.end_move(vector[:2],
                                      inverted_x_axis,
                                      inverted_y_axis)
                #haven't implemented rotation yet
            else:
                log.log_error("Solenoids have not been initialized")

    def move(self, vector, inverted_x_axis, inverted_y_axis):
        """ Sends the movement instruction to the appropriate control system

        Keyword Arguments:
        vector -- movement vector
        invert_x_axis -- boolean of whether to invert on the x-axis
        invert_y_axis -- boolean of whether to invert on the y-axis

        """
        if self.__control_schema == _EMMA_ACTUATORS:
            if len(vector) != 3:
                log.log_error("3 arguments were expected, " \
                              "{0} were given.".format(len(vector)))
                return

            if self.__actuators:
                self.__actuators.move(vector[:2],
                                      inverted_x_axis,
                                      inverted_y_axis)
                #haven't implemented rotation yet
            else:
                log.log_error("Actuators have not been initialized" \
                              " with a com-port properly.")
        elif self.__control_schema == _EMMA_SOLENOIDS:
            if len(vector) != 3:
                log.log_error("3 arguments were expected, " \
                              "{0} were given.".format(len(vector)))
                return

            if self.__solenoids:
                self.__solenoids.move(vector[:2],
                                      inverted_x_axis,
                                      inverted_y_axis)
                #haven't implemented rotation yet
            else:
                log.log_error("Solenoids have not been initialized")

    def move_to(self, vector, inverted_x_axis, inverted_y_axis):
        """ Sends the movement instruction to the appropriate control system

        Keyword Arguments:
        vector -- position vector
        invert_x_axis -- boolean of whether to invert on the x-axis
        invert_y_axis -- boolean of whether to invert on the y-axis

        """
        if self.__control_schema == _EMMA_ACTUATORS:
            if len(vector) != 3:
                log.log_error("3 arguments were expected " \
                              "({0} given).".format(len(vector)))
                return

            if self.__actuators:
                self.__actuators.move_to(vector[:2],
                                         inverted_x_axis,
                                         inverted_y_axis)
                #haven't implemented rotation yet
            else:
                log.log_error("Actuators have not been initialized" \
                              " with a com-port properly.")
        elif self.__control_scheme == _EMMA_SOLENOIDS:
            if len(vector) != 3:
                log.log_error("3 arguments were expected " \
                              "({0} given).".format(len(vector)))
                return

            if self.__actuators:
                self.__actuators.move_to(vector[:2],
                                         inverted_x_axis,
                                         inverted_y_axis)
            else:
                log.log_error("Solenoids have not been initialized" \
                              " with a com-port properly.")

    def switch_actuator_axis(self):
        """ Toggles which device is responsible for x and y axis movement """
        if self.__actuators:
            self.__actuators.switch_actuator_axis()
        else:
            log.log_error("Actuators have not been initialized" \
                          " with a com-port properly.")

    def switch_to_EMMA_actuator(self):
        """ Switches the controller to EMMA actuator mode """
        log.log_info("Switched to EMMA actuators mode")
        self.__control_schema = _EMMA_ACTUATORS

    def switch_to_EMMA_solenoid(self):
        """ Switches the controller to EMMA solenoid mode """
        log.log_info("Switched to EMMA solenoids mode")
        self.__control_schema = _EMMA_SOLENOIDS
        self.initialize_solenoids()
