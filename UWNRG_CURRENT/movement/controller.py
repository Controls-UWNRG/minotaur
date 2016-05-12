import log as log
import movement.actuators as actuators
import movement.solenoids as solenoids
import node as node

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

    #NOT SURE IF NEEDED
    '''def follow_path(self, path_x, path_y, inverted_x_axis, inverted_y_axis):    #currently only moves accurators
        if self.__actuators:
            self.__actuators.follow_path(inverted_x_axis, inverted_y_axis)
        else:
            log.log_error("Actuators have not been initialized" \
                          "with a com-port properly")
    '''
    # def box_path(self, inverted_x_axis, inverted_y_axis):
    #     if self.__actuators:
    #         self.__actuators.box_path(inverted_x_axis,
    #                                       inverted_y_axis)
    #         #haven't implemented rotation yet
    #     else:
    #         log.log_error("Actuators have not been initialized" \
    #                       " with a com-port properly.")

    # def triangle_path(self, inverted_x_axis, inverted_y_axis):
    #     if self.__actuators:
    #         self.__actuators.triangle_path(inverted_x_axis, inverted_y_axis)
    #         #haven't implemented rotation yet
    #     else:
    #         log.log_error("Actuators have not been initialized" \
    #                       " with a com-port properly.")

    # def circle_path(self, inverted_x_axis, inverted_y_axis):
    #     if self.__actuators:
    #         self.__actuators.circle_path(inverted_x_axis,
    #                                       inverted_y_axis)
    #         #haven't implemented rotation yet
    #     else:
    #         log.log_error("Actuators have not been initialized" \
    #                       " with a com-port properly.")
    #def figure_eight(self, inverted_x_axis, inverted_y_axis):

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

    """----------------------------------ICRA 2016!!!---------------------------------"""
    # def move_between_nodes(self, start_node, dest_node):
    #     if start_node.__name == "03":
    #         if dest_node.__name in start_node.__adj_nodes:
    #             if dest_node.__name == "02":
    #                 # Go down 1 unit, go right 1 unit
    #                 log.log_info("a")
    #             elif dest_node.__name == "26":
    #                 # Go up 1 unit, go right 1 unit
    #                 log.log_info("a")
    #             elif dest_node.__name == "11":
    #                 # Circle(radius = 1, start = 180, end = 225)
    #                 log.log_info("a")
    #             elif dest_node.__name == "15":
    #                 # Circle(radius = 1, start = 180, end = 135)
    #                 log.log_info("a")
    #             else:
    #                 #invalid node
    #                 log.log_info("Invalid node")
    #         else:
    #             #invalid node
    #             log.log_info("Invalid node")
    #
    #         return
    #
    #     if start_node.__name == "11":
    #         if dest_node.__name in start_node.__adj_nodes:
    #             if dest_node.__name == "02":
    #                 # Go down 1 unit, go right 1 unit
    #                 log.log_info("a")
    #             elif dest_node.__name == "26":
    #                 # Go up 1 unit, go right 1 unit
    #                 log.log_info("a")
    #             elif dest_node.__name == "11":
    #                 # Circle(radius = 1, start = 180, end = 225)
    #                 log.log_info("a")
    #             elif dest_node.__name == "15":
    #                 # Circle(radius = 1, start = 180, end = 135)
    #                 log.log_info("a")
    #             else:
    #                 #invalid node
    #                 log.log_info("Invalid node")
    #         else:
    #             #invalid node
    #             log.log_info("Invalid node")
    #
    #         return

    def initialize_nodes(self):
        log.log_info("Nodes initialized.")
        nodes = {
            Node("03", {"11", "02", "15", "26"}),
            Node("11", {"03", "15", "02", "31"}),
            Node("15", {"26", "11", "03", "35"})
        }

    def log_actuator_init_error(self):
        log.log_error("Actuators have not been initialized" \
                          " with a com-port properly.")

    ''' HIJACKED ICRA 2015 CODE!!!!!!! ACTUAL CODE IS COMMENTED OUT ABOVE '''
    # This is the LARGE diagonal path
    def triangle_path(self, inverted_x_axis, inverted_y_axis):
        if self.__actuators:
            self.__actuators.diagonal_path(inverted_x_axis, inverted_y_axis, ["DOWN", "LEFT"], "LARGE")
        else:
            self.log_actuator_init_error()

    # This is the straight path
    def box_path(self, inverted_x_axis, inverted_y_axis):
        if self.__actuators:
            self.__actuators.straight_path(inverted_x_axis, inverted_y_axis, "DOWN", "LARGE")
        else:
            self.log_actuator_init_error()

    def circle_path(self, inverted_x_axis, inverted_y_axis):
        if self.__actuators:
            self.__actuators.circle_path(inverted_x_axis, inverted_y_axis)
            #haven't implemented rotation yet
        else:
            self.log_actuator_init_error()
