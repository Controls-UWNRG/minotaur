import log as log
import movement.controller as controller
import imaging.image_recognition as ir

_movement_controller = controller.Controller()
_ir = ir.ImageRecognition()

def move(vector, inverted_x_axis, inverted_y_axis):
    """ Sends the movement instruction to the appropriate control system

    Keyword Arguments:
    vector -- movement vector
    invert_x_axis -- boolean of whether to invert on the x-axis
    invert_y_axis -- boolean of whether to invert on the y-axis

    """
    _movement_controller.move(vector, inverted_x_axis, inverted_y_axis)

def display_feed():
    """ Display camera feed """
    _ir.start_camera_feed()

def end_move(vector, inverted_x_axis, inverted_y_axis):
    """ Sends the end movement instruction to the appropriate control system

    Keyword Arguments:
    vector -- movement vector
    invert_x_axis -- boolean of whether to invert on the x-axis
    invert_y_axis -- boolean of whether to invert on the y-axis

    """
    _movement_controller.end_move(vector, inverted_x_axis, inverted_y_axis)

def navigate_maze(sequence, x_axis_inverted, y_axis_inverted):
    log.log_info("Navigating maze...")
    _movement_controller.navigate_maze(_ir, sequence, x_axis_inverted, y_axis_inverted)

def mark_corner(mouse_event):
    _ir.mark_corner(mouse_event.x, mouse_event.y)
    log.log_info("Corner marked at " + (str)(mouse_event.x) + ", " + (str)(mouse_event.y) + ".")

def mark_path(mouse_event):
    _ir.mark_point(mouse_event.x, mouse_event.y)
    log.log_info("Point marked at " + (str)(mouse_event.x) + ", "  + (str)(mouse_event.y) + ".")

def box_path(x_axis_inverted, y_axis_inverted):
    _movement_controller.box_path(x_axis_inverted, y_axis_inverted, "RIGHT", 1)

def draw_shapes(x_axis_inverted, y_axis_inverted, shape_info):
    _movement_controller.draw_shapes(x_axis_inverted, y_axis_inverted, shape_info)

def triangle_path(x_axis_inverted, y_axis_inverted):
    _movement_controller.triangle_path(x_axis_inverted, y_axis_inverted, ["UP", "RIGHT"], 0.5)

def circle_path(x_axis_inverted, y_axis_inverted):
    _movement_controller.circle_path(x_axis_inverted, y_axis_inverted, 1, 0, 90)
    #_movement_controller.get_path(x_axis_inverted, y_axis_inverted, ["03", "11", "03"])

def move_to_circle_start(x_axis_inverted, y_axis_inverted):
    _movement_controller.move_to_circle_start(x_axis_inverted, y_axis_inverted)

def move_to_top_right(x_axis_inverted, y_axis_inverted):
    _movement_controller.move_to_top_right(x_axis_inverted, y_axis_inverted)

def figure_eight(x_axis_inverted, y_axis_inverted):
    _movement_controller.figure_eight(x_axis_inverted, y_axis_inverted)

def move_to(vector, inverted_x_axis, inverted_y_axis):
    """ Sends the movement instruction to the appropriate control system

    Keyword Arguments:
    vector -- position vector
    invert_x_axis -- boolean of whether to invert on the x-axis
    invert_y_axis -- boolean of whether to invert on the y-axis

    """
    _movement_controller.move_to(vector, inverted_x_axis, inverted_y_axis)

def move_to_and_verify(vector, inverted_x_axis, inverted_y_axis):
    """ Sends the movement instruction to the appropriate control system

    Keyword Arguments:
    vector -- position vector
    invert_x_axis -- boolean of whether to invert on the x-axis
    invert_y_axis -- boolean of whether to invert on the y-axis

    """
    _movement_controller.move_to(vector, inverted_x_axis, inverted_y_axis)
    # TODO: Verify movement, adjust balance of controller values according to result,
    # attempt to correct course.

def switch_to_EMMA_solenoid():
    """ Switches the controller to EMMA solenoid mode """
    _movement_controller.switch_to_EMMA_solenoid()

def set_feed(camera_feed=None):
    _ir.set_feed(camera_feed=camera_feed)

def switch_to_EMMA_actuator():
    """ Switches the controller to EMMA actuator mode """
    _movement_controller.switch_to_EMMA_actuator()

def get_available_com_ports():
    """ Returns a list of available com-ports """
    return _movement_controller.get_available_com_ports()

def set_com_port(com_port):
    """ Sets the com-port to use for actuator communication """
    _movement_controller.initialize_actuators(com_port)

def switch_actuator_axis():
    """ Toggles which device is responsible for x and y axis movement """
    _movement_controller.switch_actuator_axis()

def get_speed():
    """  Changes the speed of movement for the controller

    Keyword Arguments:
    increment -- whether the speed is increasing (1) or decreasing (-1)

    """
    return _movement_controller.get_speed()

def change_speed(new_value, increment):
    """  Changes the speed of movement for the controller

    Keyword Arguments:
    increment -- whether the speed is increasing (1) or decreasing (-1)

    """
    _movement_controller.speed_change(new_value, increment)

def init_field():
    return field.Field()

def configure_field(med_width, ad_bsize, ad_const, can_low, can_high):
    """ Update value of filters and boundaries 

    Keyword Arguments:
    med_width -- Median filter width
    ad_bsize -- Adaptive filter block size
    ad_const -- Adaptive filter constant offset
    can_low -- Canny filter lower threshold
    can_high -- Canny filter upper threshold

    """
    field.medfilt_width = med_width
    field.adaptive_blocksize = ab_bsize
    field.adaptive_c = ad_const
    field.canny_thresh1 = can_low
    field.canny_thresh2= can_high

def find_robot_in_frame(frame):
    return _ir.find_robot_in_frame(frame)

def get_frame_with_points():
    """ Returns a numpy frame with points drawn on """
    return _ir.get_frame_with_points()

def reset_path():
    log.log_info("Path reset.")
    return _ir.reset_points()

def get_frame_with_corners():
    """ Returns a numpy frame with corners drawn on """
    return _ir.get_frame_with_corners()

def get_frame():
    """ Return a single frame from the camera """
    return _ir.get_frame()

def get_frame_bgr_to_rgb():
    """ Return a single frame from the camera """
    return _ir.get_frame_bgr_to_rgb()

def get_frame_np():
    """ Get a numpy array frame to display in the main window """
    return _ir.get_frame_np() 

def get_image_from_file(path):
    """ Returns an image from a given path """
    return _ir.get_image_from_file(path)

def update_ir_settings(constant, block, aperture):
    """ Updates the settings of the IR system """
    return _ir.update_ir_settings(constant, block, aperture)
    