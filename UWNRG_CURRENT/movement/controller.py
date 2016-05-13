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
        log.log_error("No figure eight")

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

    """
    ---------------------------------------------------------------------------------------------------------------------
    ---------------------------------------------------- ICRA 2016 ------------------------------------------------------
    ---------------------------------------------------------------------------------------------------------------------
    """
    def node_dictionary(name):
        return {
            "node1": "03",
            "node2": "11",
            "node3": "15",
            "node4": "20",
            "node5": "26",
            "node6": "31",
            "node7": "35",
            "node8": "40",
            "node9": "43",
            "node10": "46",
            "node11": "52",
            "node12": "64",
            "node13": "73",
            "node14": "76"
        }[name]

    def draw_path(self, inverted_x_axis, inverted_y_axis, path_info):
        nodes = []
        for i in range(len(path_info)):
            nodes.append(node_dictionary(path_info[i]))
        get_path(self, inverted_x_axis, inverted_y_axis, nodes)

    def get_path(self, inverted_x_axis, inverted_y_axis, nodes):
        for i in range(len(nodes) - 1):
            self.move_between_nodes(inverted_x_axis, inverted_y_axis, nodes[i], nodes[i+1])
        return

    def move_between_nodes(self, inverted_x_axis, inverted_y_axis, start_node, dest_node):
        if start_node == "03":
            if dest_node == "20":
                # Go down 1 unit, go right 1 unit
                self.box_path(inverted_x_axis, inverted_y_axis, "DOWN", 1)
                self.box_path(inverted_x_axis, inverted_y_axis, "RIGHT", 1)
            elif dest_node == "26":
                # Go up 1 unit, go right 1 unit
                self.box_path(inverted_x_axis, inverted_y_axis, "UP", 1)
                self.box_path(inverted_x_axis, inverted_y_axis, "RIGHT", 1)
            elif dest_node == "11":
                # Circle(radius = 1, start = 180, end = 225)
                self.circle_path(inverted_x_axis, inverted_y_axis, 1, 180, 225)
            elif dest_node == "15":
                # Circle(radius = 1, start = 180, end = 135)
                self.circle_path(inverted_x_axis, inverted_y_axis, 1, 180, 135)
            else:
                #invalid node
                log.log_info("Invalid node")
                return
            log.log_info(start_node + " to " + dest_node)
            return

        if start_node == "11":
            if dest_node == "03":
                self.circle_path(inverted_x_axis, inverted_y_axis, 1, 225, 180)
            elif dest_node == "15":
                self.box_path(inverted_x_axis, inverted_y_axis, "UP", 1.5)
            elif dest_node == "20":
                self.circle_path(inverted_x_axis, inverted_y_axis, 1, 225, 270)
            elif dest_node == "31":
                self.box_path(inverted_x_axis, inverted_y_axis, "RIGHT", 1.5)
            else:
                #invalid node
                log.log_info("Invalid node")
                return
            log.log_info(start_node + " to " + dest_node)
            return

        if start_node == "15":
            if dest_node in start_node.__adj_nodes:
                if dest_node == "26":
                    self.circle_path(inverted_x_axis, inverted_y_axis, 1, 135, 90)
                elif dest_node == "11":
                    self.box_path(inverted_x_axis, inverted_y_axis, "DOWN", 1.5)
                elif dest_node == "03":
                    self.circle_path(inverted_x_axis, inverted_y_axis, 1, 135, 180)
                elif dest_node == "35":
                    self.box_path(inverted_x_axis, inverted_y_axis, "RIGHT", 1.5)
                else:
                    #invalid node
                    log.log_info("Invalid node")
                    return
                log.log_info(start_node + " to " + dest_node)
            else:
                #invalid node
                log.log_info("Invalid node")
            return

        if start_node == "20":
            if dest_node == "03":
                self.box_path(inverted_x_axis, inverted_y_axis, "LEFT", 1)
                self.box_path(inverted_x_axis, inverted_y_axis, "UP", 1)
            elif dest_node == "40":
                self.box_path(inverted_x_axis, inverted_y_axis, "RIGHT", 1)
            elif dest_node == "11":
                self.circle_path(inverted_x_axis, inverted_y_axis, 1, 270, 225)
            elif dest_node == "31":
                self.circle_path(inverted_x_axis, inverted_y_axis, 1, 270, 315)
            else:
                #invalid node
                log.log_info("Invalid node")
                return
            log.log_info(start_node + " to " + dest_node)
            return

        if start_node == "26":
            if dest_node == "03":
                self.box_path(inverted_x_axis, inverted_y_axis, "LEFT", 1)
                self.box_path(inverted_x_axis, inverted_y_axis, "DOWN", 1)
            elif dest_node == "46":
                self.box_path(inverted_x_axis, inverted_y_axis, "RIGHT", 1)
            elif dest_node == "35":
                self.circle_path(inverted_x_axis, inverted_y_axis, 1, 90, 45)
            elif dest_node == "15":
                self.circle_path(inverted_x_axis, inverted_y_axis, 1, 90, 135)
            else:
                #invalid node
                log.log_info("Invalid node")
                return
            log.log_info(start_node + " to " + dest_node)
            return

        if start_node == "31":
            if dest_node == "43":
                self.circle_path(inverted_x_axis, inverted_y_axis, 1, 315, 360)
            elif dest_node == "35":
                self.box_path(inverted_x_axis, inverted_y_axis, "UP", 1.5)
            elif dest_node == "20":
                self.circle_path(inverted_x_axis, inverted_y_axis, 1, 315, 270)
            elif dest_node == "15":
                self.box_path(inverted_x_axis, inverted_y_axis, "LEFT", 1.5)
            else:
                #invalid node
                log.log_info("Invalid node")
                return
            log.log_info(start_node + " to " + dest_node)
            return

        if start_node == "35":
            if dest_node == "26":
                self.circle_path(inverted_x_axis, inverted_y_axis, 1, 45, 90)
            elif dest_node == "31":
                self.box_path(inverted_x_axis, inverted_y_axis, "DOWN", 1.5)
            elif dest_node == "43":
                self.circle_path(inverted_x_axis, inverted_y_axis, 1, 45, 0)
            elif dest_node == "15":
                self.box_path(inverted_x_axis, inverted_y_axis, "LEFT", 1.5)
            else:
                #invalid node
                log.log_info("Invalid node")
                return
            log.log_info(start_node + " to " + dest_node)
            return

        if start_node  == "40":
            if dest_node  == "20":
                self.box_path(inverted_x_axis, inverted_y_axis, "LEFT", 1)
            elif dest_node  == "43":
                self.box_path(inverted_x_axis, inverted_y_axis, "UP", 1)
            elif dest_node  == "52":
                self.triangle_path(inverted_x_axis, inverted_y_axis, ["UP", "RIGHT"], 0.5)
            elif dest_node  == "73":
                self.box_path(inverted_x_axis, inverted_y_axis, "RIGHT", 1)
                self.box_path(inverted_x_axis, inverted_y_axis, "UP", 1)
            else:
                #invalid node
                log.log_info("Invalid node")
                return
            log.log_info(start_node  + " to " + dest_node )
            return

        if start_node  == "46":
            if dest_node  == "26":
                self.box_path(inverted_x_axis, inverted_y_axis, "LEFT", 1)
            elif dest_node  == "43":
                self.box_path(inverted_x_axis, inverted_y_axis, "DOWN", 1)
            elif dest_node  == "76":
                self.box_path(inverted_x_axis, inverted_y_axis, "RIGHT", 1)
            else:
                #invalid node
                log.log_info("Invalid node")
                return
            log.log_info(start_node  + " to " + dest_node )
            return

        if start_node  == "43":
            if dest_node  == "31":
                self.circle_path(inverted_x_axis, inverted_y_axis, 1, 360, 315)
            elif dest_node  == "40":
                self.box_path(inverted_x_axis, inverted_y_axis, "DOWN", 1)
            elif dest_node  == "35":
                self.circle_path(inverted_x_axis, inverted_y_axis, 1, 0, 45)
            elif dest_node  == "46":
                self.box_path(inverted_x_axis, inverted_y_axis, "UP", 1)
            elif dest_node  == "52":
                self.circle_path(inverted_x_axis, inverted_y_axis, 0.5, 180, 225)
            elif dest_node  == "64":
                self.circle_path(inverted_x_axis, inverted_y_axis, 0.5, 180, 45)
            else:
                #invalid node
                log.log_info("Invalid node")
                return
            log.log_info(start_node  + " to " + dest_node )
            return

        if start_node  == "52":
            if dest_node  == "40":
                self.triangle_path(inverted_x_axis, inverted_y_axis, ["DOWN", "LEFT"], 0.5)
            elif dest_node  == "43":
                self.circle_path(inverted_x_axis, inverted_y_axis, 0.5, 225, 180)
            elif dest_node  == "64":
                self.triangle_path(inverted_x_axis, inverted_y_axis, ["UP", "RIGHT"], 1)
            elif dest_node  == "73":
                self.circle_path(inverted_x_axis, inverted_y_axis, 0.5, 225, 360)
            else:
                #invalid node
                log.log_info("Invalid node")
                return
            log.log_info(start_node  + " to " + dest_node )
            return

        if start_node == "64":
            if dest_node == "52":
                self.triangle_path(inverted_x_axis, inverted_y_axis, ["DOWN", "LEFT"], 1)
            elif dest_node == "43":
                self.circle_path(inverted_x_axis, inverted_y_axis, 0.5, 45, 180)
            elif dest_node == "76":
                self.triangle_path(inverted_x_axis, inverted_y_axis, ["UP", "RIGHT"], 0.5)
            elif dest_node == "73":
                self.circle_path(inverted_x_axis, inverted_y_axis, 0.5, 45, 0)
            else:
                #invalid node
                log.log_info("Invalid node")
                return
            log.log_info(start_node + " to " + dest_node)
            return

        if start_node == "73":
            if dest_node == "40":
                self.box_path(inverted_x_axis, inverted_y_axis, "DOWN", 1)
                self.box_path(inverted_x_axis, inverted_y_axis, "LEFT", 1)
            elif dest_node == "76":
                self.box_path(inverted_x_axis, inverted_y_axis, "UP", 1)
            elif dest_node == "52":
                self.circle_path(inverted_x_axis, inverted_y_axis, 0.5, 360, 225)
            elif dest_node == "64":
                self.circle_path(inverted_x_axis, inverted_y_axis, 0.5, 0, 45)
            else:
                #invalid node
                log.log_info("Invalid node")
                return
            log.log_info(start_node + " to " + dest_node)
            return

        if start_node == "76":
            if dest_node == "46":
                self.box_path(inverted_x_axis, inverted_y_axis, "LEFT", 1)
            elif dest_node == "73":
                self.box_path(inverted_x_axis, inverted_y_axis, "DOWN", 1)
            elif dest_node == "64":
                self.triangle_path(inverted_x_axis, inverted_y_axis, ["DOWN", "LEFT"], 0.5)
            else:
                #invalid node
                log.log_info("Invalid node")
                return
            log.log_info(start_node + " to " + dest_node)
            return


    def initialize_nodes(self):
        log.log_info("Nodes initialized.")
        nodes = {
            Node("03", {"11", "20", "15", "26"}),
            Node("11", {"03", "15", "20", "31"}),
            Node("15", {"26", "11", "03", "35"}),
            Node("20", {"11", "03", "31", "40"}),
            Node("26", {"15", "03", "35", "46"}),
            Node("31", {"43", "35", "20", "15"}),
            Node("35", {"26", "31", "43", "15"}),
            Node("40", {"20", "43", "52", "73"}),
            Node("46", {"26", "43", "76"}),
            Node("43", {"31", "40", "35", "46", "52", "64"}),
            Node("52", {"40", "43", "64", "73"}),
            Node("64", {"52", "43", "76", "73"}),
            Node("73", {"40", "52", "64", "76"}),
            Node("76", {"46", "64", "73"})
        }

    def log_actuator_init_error(self):
        log.log_error("Actuators have not been initialized"
                      " with a com-port properly.")

    ''' HIJACKED ICRA 2015 CODE!!!!!!! ACTUAL CODE IS COMMENTED OUT ABOVE '''
    # This is the LARGE diagonal path
    def triangle_path(self, inverted_x_axis, inverted_y_axis, dir, size):
        if self.__actuators:
            self.__actuators.diagonal_path(inverted_x_axis, inverted_y_axis, dir, "LARGE")
        else:
            self.log_actuator_init_error()

    # This is the straight path
    def box_path(self, inverted_x_axis, inverted_y_axis, dir, size):
        if self.__actuators:
            self.__actuators.straight_path(inverted_x_axis, inverted_y_axis, "DOWN", "LARGE")
        else:
            self.log_actuator_init_error()

    def circle_path(self, inverted_x_axis, inverted_y_axis, rad, start, end):
        if self.__actuators:
            self.__actuators.circle_path(inverted_x_axis,
                                         inverted_y_axis, rad, start, end)
        else:
            self.log_actuator_init_error()
