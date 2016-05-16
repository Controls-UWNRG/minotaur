import gtk as gtk
import facade as facade
import log as log
import sys
import cv2 as cv2  
import numpy as nps
from threading import Thread

def startCamera():
    vc = cv2.VideoCapture(0) # TODO: Hook this up to the active camera device
    cv2.namedWindow("Camera Feed - Press ESC to Exit")

    while (True):
        key = cv2.waitKey(1)
        if key == 27: # exit on ESC
            break

        # Read a frame, return value rval will determine if succesful
        rval, frame = vc.read()

        # Terminate when we fail to read a frame
        if ( rval == False ):
            break

        # Show the captured frame
        cv2.imshow("Camera Feed - Press ESC to Exit", frame)

class MainWindow:

    """ main window for the application, has no public methods or variables"""
    def __clear_log(self, menu_item):
        """ Clears the log

        Keyword arguments:
        menu_item -- object the action occured on

        """
        self.__log.clear_log()

    def __enter_movement_instruction(self, button):
        """ Sends movement instruction to facade

        Keyword arguments:
        button -- object the action occured on

        """
        direction_conversion = {0: (-1, 0, 0),
                                1: (1, 0, 0),
                                2: (0, 1, 0),
                                3: (0, -1, 0),
                                4: (0, 0, 1),
                                5: (0, 0, -1)}

        direction = direction_conversion[self.__builder.get_object(
                           "manual_control_instruction_combobox").get_active()]
        magnitude = self.__builder.get_object(
                           "manual_control_entry").get_text()

        if magnitude.isdigit():
            magnitude = int(magnitude)
            facade.move(list(magnitude * x for x in direction),
                                  self.__x_axis_inverted,
                                  self.__y_axis_inverted)
        else:
            log.log_error("The magnitude of a movement must be an integer, " \
                          "'{0}' is not an integer.".format(magnitude))

    def __keyboard_movement_instruction(self, window, event):
        """ Sends movement instruction to facade

        Keyword arguments:
        window -- object the action occured on
        event -- contains information about the key press event

        """
        direction_conversion = {ord('a'): (-1, 0, 0),
                                ord('d'): (1, 0, 0),
                                ord('w'): (0, 1, 0),
                                ord('s'): (0, -1, 0),
                                ord('W'): (0, 1, 0),
                                ord('S'): (0, -1, 0),
                                ord('A'): (-1, 0, 0),
                                ord('D'): (1, 0, 0),
                                ord('e'): (0, 0, 1),
                                ord('q'): (0, 0, -1)}

        speed_change = {45 : -1, 43 : 113}

        key_pressed = event.keyval

        if key_pressed in direction_conversion and self.__keyboard_input:
            self.__activate_arrow(key_pressed)
            direction = direction_conversion[key_pressed]
            direction = [x for x in direction]
            facade.move(direction,
                        self.__x_axis_inverted,
                        self.__y_axis_inverted)
        elif key_pressed in speed_change and self.__keyboard_input:
            facade.change_speed(None, speed_change[key_pressed])

    def __end_keyboard_movement_instruction(self, window, event):
        """ Ends Movment Instruction to facade

        Keyword arguments:
        window -- object the action occured on
        event -- contains information about the key press event

        """
        # 97=a, 100=d, 119=w, 115=s
        direction_conversion = {ord('a'): (-1, 0, 0),
                                ord('d'): (1, 0, 0),
                                ord('w'): (0, 1, 0),
                                ord('s'): (0, -1, 0),
                                ord('W'): (0, 1, 0),
                                ord('S'): (0, -1, 0),
                                ord('A'): (-1, 0, 0),
                                ord('D'): (1, 0, 0),
                                ord('e'): (0, 0, 1),
                                ord('q'): (0, 0, -1)}

        key_pressed = event.keyval

        if key_pressed in direction_conversion and self.__keyboard_input:
            self.__deactivate_arrow(key_pressed)
            direction = direction_conversion[key_pressed]
            direction = [x for x in direction]
            facade.end_move(direction,
                        self.__x_axis_inverted,
                        self.__y_axis_inverted)

    def __init_arrows(self):
        self.base_arrow = self.__builder.get_object("arrow_up")
        self.base_arrow.set_from_file("img/arrow_inactive.png")
        self.base_arrow_pixbuf = self.base_arrow.get_pixbuf()

        self.base_arrow_on = self.__builder.get_object("arrow_up")
        self.base_arrow_on.set_from_file("img/arrow_active.png")
        self.base_arrow_on_pixbuf = self.base_arrow.get_pixbuf()

        for i in [97, 100, 119, 115]:
            self.__deactivate_arrow(i)

    def __deactivate_arrow(self, key):
        # 97=a, 100=d, 119=w, 115=s
        direction_conversion = {ord('a'): "arrow_left",
                                ord('d'): "arrow_right",
                                ord('w'): "arrow_up",
                                ord('s'): "arrow_down",
                                ord('A'): "arrow_left",
                                ord('D'): "arrow_right",
                                ord('W'): "arrow_up",
                                ord('S'): "arrow_down"}
        rotation = {ord('a'): 1,
                    ord('d'): 3,
                    ord('w'): 0,
                    ord('s'): 2,
                    ord('A'): 1,
                    ord('D'): 3,
                    ord('W'): 0,
                    ord('S'): 2}
        if key not in direction_conversion:
            return
        pixbuf = self.base_arrow_pixbuf.rotate_simple(rotation[key] * 90)
        self.__builder.get_object(direction_conversion[key]).set_from_pixbuf(pixbuf)

    def __activate_arrow(self, key):
        # 97=a, 100=d, 119=w, 115=s
        direction_conversion = {ord('a'): "arrow_left",
                                ord('d'): "arrow_right",
                                ord('w'): "arrow_up",
                                ord('s'): "arrow_down",
                                ord('A'): "arrow_left",
                                ord('D'): "arrow_right",
                                ord('W'): "arrow_up",
                                ord('S'): "arrow_down"}
        rotation = {ord('a'): 1,
                    ord('d'): 3,
                    ord('w'): 0,
                    ord('s'): 2,
                    ord('A'): 1,
                    ord('D'): 3,
                    ord('W'): 0,
                    ord('S'): 2}
                    
        if key not in direction_conversion:
            return
        pixbuf = self.base_arrow_on_pixbuf.rotate_simple(rotation[key] * 90)
        self.__builder.get_object(direction_conversion[key]).set_from_pixbuf(pixbuf)
  
    def __open_maze_navigate_dialog(self, menu_item):
        """ Opens the image settings window """

        # TODO: Sometimes this breaks if the pilot closes the window and reopens it
        maze_window = self.__builder.get_object("maze_window")
        field_image = self.__builder.get_object("field_image")
        
        #annotated_frame = facade.get_frame_with_corners()
        annotated_frame = facade.get_frame_with_points()
        
        annotated_pixbuf = gtk.gdk.pixbuf_new_from_array(annotated_frame, gtk.gdk.COLORSPACE_RGB, 8)
        field_image.set_from_pixbuf(annotated_pixbuf)

        maze_window.show()
        #maze_window.hide()

    def __figure_eight(self, menu_item):
        facade.figure_eight(self.__x_axis_inverted, self.__y_axis_inverted)

    def __box_path(self, menu_item):
        facade.box_path(self.__x_axis_inverted, self.__y_axis_inverted)

    def __triangle_path(self, menu_item):
        facade.triangle_path(self.__x_axis_inverted, self.__y_axis_inverted)

    def __circle_path(self, menu_item):
        facade.circle_path(self.__x_axis_inverted, self.__y_axis_inverted)

    def __move_circle_start(self, menu_item):
        facade.move_to_circle_start(self.__x_axis_inverted, self.__y_axis_inverted)

    def __move_top_right(self, menu_item):
        facade.move_to_top_right(self.__x_axis_inverted, self.__y_axis_inverted)
    def __open_pick_shapes_window(self, menu_item):
        shape_window = self.__builder.get_object("pick_shape_window")
        shape_window.show()

    def __set_shape_counts(self, button):
        fields = ["triangle", "circle", "rectangle"]
        shape_info = [{}, {}, {}]
        used_order = [False, False, False]
        for field in fields:
            count_field = self.__builder.get_object(field + "_count")
            count = count_field.get_text()
            order_field = self.__builder.get_object(field + "_order")
            order = order_field.get_text()
            if not order.isdigit() or not count.isdigit():
                log.log_error("Order and count must be numbers")
            else:
                index = int(order)-1
                if used_order[index]:
                    log.log_error("Duplicate order number {0}".format(index+1))
                    return

                used_order[index] = True
                shape_info[index]["shape"] = field
                shape_info[index]["count"] = int(count)
        self.__close_pick_shapes_window(button)
        facade.draw_shapes(self.__x_axis_inverted, self.__y_axis_inverted, shape_info)

    def __close_pick_shapes_window(self, button):
        shape_window = self.__builder.get_object("pick_shape_window")
        shape_window.hide()

    """
    ---------------------------------------------------------------------------------------------------------------------
    ---------------------------------------------------- ICRA 2016 ------------------------------------------------------
    ---------------------------------------------------------------------------------------------------------------------
    """
    def __open_pick_path_window(self, menu_item):
        path_window = self.__builder.get_object("pick_path_window")
        path_window.show()

    # TODO: get proper data from the GUI
    def __set_node_path(self, button):
        log.log_info("Setting node path")
        node_num = 14
        path_info = [None] * node_num
        used_order = [False] * node_num
        # count = self.__builder.get_object("count")

        # for n in range(0, count):
        for node in range(0, node_num):
            order_object = self.__builder.get_object("order_node" + node)
            order = order_object.get_text()
            if (not order.isdigit()):
                log.log_error("Order must be numbers")
            elif int(order) <= 0:
                # node not used
                continue
            else:
                index = int(order)-1
                if used_order[index]:
                    log.log_error("Duplicate order number {0}".format(index+1))
                    return

                used_order[index] = True
                print node+1
                path_info[index] = "node" + str(node+1)

        self.__close_pick_path_window(button)
        facade.draw_path(self.__x_axis_inverted, self.__y_axis_inverted, path_info)

    def __close_pick_path_window(self, button):
        path_window = self.__builder.get_object("pick_path_window")
        path_window.hide()

    """
    ---------------------------------------------------------------------------------------------------------------------
    ------------------------------------------------------ END ----------------------------------------------------------
    ---------------------------------------------------------------------------------------------------------------------
    """

    def __navigate_maze(self, menu_item):
        """ Strip out the selected paths and pass them to the movement controller """

        gate1 = self.__builder.get_object("gate1_top")
        gate2 = self.__builder.get_object("gate2_top")
        gate3 = self.__builder.get_object("gate3_top")
        gate4 = self.__builder.get_object("gate4_top")
        gate5 = self.__builder.get_object("gate5_top")
        gate6 = self.__builder.get_object("gate6_top")

        gate1_active = [r for r in gate1.get_group() if r.get_active()] 
        gate2_active = [r for r in gate1.get_group() if r.get_active()] 
        gate3_active = [r for r in gate1.get_group() if r.get_active()] 
        gate4_active = [r for r in gate1.get_group() if r.get_active()] 
        gate5_active = [r for r in gate1.get_group() if r.get_active()] 
        gate6_active = [r for r in gate1.get_group() if r.get_active()] 

        sequence = (gate1_active[0].get_label(), gate2_active[0].get_label(), gate3_active[0].get_label(),
                    gate4_active[0].get_label(), gate5_active[0].get_label(), gate6_active[0].get_label())

        numseq = {}

        # TODO: Hypothetically, this should probably be moved lower down in the abstrction layers
        for i in range(0, 6):
            if sequence[i] == "top":
                numseq[i] = 0
            elif sequence[i] == "mid":
                numseq[i] = 1
            elif sequence[i] == "bot":
                numseq[i] = 2

        _window = self.__builder.get_object("maze_window")
        facade.navigate_maze(numseq, self.__x_axis_inverted, self.__y_axis_inverted)

    def __video_camera(self, menu_item):
        t = Thread(target=startCamera)
        t.start()

    def __maze_navigate(self):
        facade.maze_navigate(sequence, self.__x_axis_inverted, self.__y_axis_inverted)

    def __init__(self):
        filename = "gui.glade"
        handlers = {
            "on_setup_menu_exit_activate" : gtk.main_quit,
            "on_main_window_destroy" : gtk.main_quit,
            "on_browse_image_clicked" : self.__select_image_file,
            "on_manual_control_enter_button_clicked" :
                                             self.__enter_movement_instruction,
            "on_refresh_ir_cam_image_clicked" : self.__refresh_ir_cam_frame,
            "on_edit_menu_invert_x_axis_toggled" : self.__invert_x_axis,
            "on_edit_menu_invert_y_axis_toggled" : self.__invert_y_axis,
            "on_help_menu_about_activate" : self.__open_about_window,
            "on_help_menu_help_activate" : self.__open_help_window,
            "on_tools_menu_manual_keyboard_input_toggled" :
                                                  self.__toggle_keyboard_input,
            # TODO: Add a camera settings menu (for choosing video source)
            "on_main_window_key_press_event" :
                                          self.__keyboard_movement_instruction,
            "on_edit_menu_clear_log_activate" : self.__clear_log,
            "on_emma_mode_actuator_radio_toggled" : self.__switch_mode_EMMA_actuator,
            "on_emma_mode_solenoid_radio_toggled" : self.__switch_mode_EMMA_solenoid,
            "on_maze_frame_refresh" : self.__refresh_maze_frame,
            "on_maze_frame_confirm" : self.__confirm_maze_frame,
            "on_ir_preview_activate" : self.__preview_image_recognition,
            #"on_field_image_butt:on_press_event" : self.__mark_corner,
            "on_field_image_button_press_event" : self.__mark_path,
            "on_maze_frame_key_release_event" : self.__path_reset,
            "on_setup_menu_actuators_activate" :
                                            self.__open_actuator_setup_window,
            "on_setup_menu_solenoids_activate" :
                                            self.__open_solenoid_setup_window,
            "on_figure_eight_activate" : self.__figure_eight,
            "on_box_path_activate" : self.__box_path,
            "on_triangle_path_activate" : self.__triangle_path,
            "on_circle_path_activate" : self.__circle_path,
            "on_move_to_circle_start_activate" : self.__move_circle_start,
            "on_move_to_top_right_activate" : self.__move_top_right,
            "on_pick_shapes" : self.__open_pick_shapes_window,
            "on_shape_ok_clicked" : self.__set_shape_counts,
            "on_shape_cancel_clicked" : self.__close_pick_shapes_window,
            ### ---- ICRA 2016 ---- ###
            "on_pick_path" : self.__open_pick_path_window,
            "on_path_ok_clicked" : self.__set_node_path,
            "on_path_cancel_clicked": self.__close_pick_path_window,
            ########## END ############
            "on_video_camera_activate" : self.__video_camera,
            "on_navigate_maze" : self.__open_maze_navigate_dialog,
            "on_main_window_key_release_event" :
                                          self.__end_keyboard_movement_instruction,
            "on_video_menu_web_cam_toggled" : self.__video_menu_web_cam_toggle,
            "on_video_menu_micro_cam_toggled" : self.__video_menu_micro_cam_toggle,
            "on_saveIRSettings_activate" : self.__update_ir_settings
        }

        self.__builder = gtk.Builder()
        self.__builder.add_from_file(filename)
        self.__builder.connect_signals(handlers)
        self.__builder.get_object("main_window").show_all()

        self.__keyboard_input = True
        self.__log = log.Log()
        self.__x_axis_inverted = False
        self.__y_axis_inverted = False
        self.__solenoid_step = 1

        self.__log.set_buffer(self.__builder.get_object(
                "vertical_log_scroll_window_text_view").get_property('buffer'))

        self.__init_arrows()

        constant_entry = self.__builder.get_object("constant_entry")
        block_entry = self.__builder.get_object("block_entry")
        aperture_entry = self.__builder.get_object("aperture_entry")

        #TODO: Does this cause a hang under certain conditions (no COM port?)
        #?? this still a thing if it hangs just use --noport

        if "--noport" not in sys.argv:
            self.__initialize_com_port()

    def __update_ir_settings(self, item):
        constant_entry = self.__builder.get_object("constant_entry")
        block_entry = self.__builder.get_object("block_entry")
        aperture_entry = self.__builder.get_object("aperture_entry")

        constant = float(constant_entry.get_text())
        block = int(block_entry.get_text())
        aperture = int(aperture_entry.get_text())

        facade.update_ir_settings(constant, block, aperture)


    def __video_menu_web_cam_toggle(self, *args, **kwargs):
        print "setting feed to webcam"
        facade.set_feed(camera_feed=0)

    def __video_menu_micro_cam_toggle(self, *args, **kwargs):
        print "setting feed to microscope"
        facade.set_feed(camera_feed=1)
        
    def __invert_x_axis(self, check_menu_item):
        """ Updates x inversion variable

        Keyword arguments:
        check_menu_item -- object the action occured on

        """
        self.__x_axis_inverted ^= True;

    def __invert_y_axis(self, check_menu_item):
        """ Updates y inversion variable

        Keyword arguments:
        check_menu_item -- object the action occured on

        """
        self.__y_axis_inverted ^= True;

    def __open_about_window(self, menu_item):
        """ Opens the about program window

        Keyword arguments:
        menu_item -- object the action occured on

        """
        about_window = self.__builder.get_object("about_window")

        # do not listen for close events in order for the close button on the
        # window to work, as you are unable to add a signal to the close button
        about_window.run()
        about_window.hide()

    def __open_help_window(self, menu_item):
        """ Opens the help program window

        Keyword arguments:
        menu_item -- object the action occured on

        """
        help_window = self.__builder.get_object("help_window")

        # do not listen for close events in order for the close button on the
        # window to work, as you are unable to add a signal to the close button
        help_window.run()
        help_window.hide()

    def __initialize_com_port(self):
        """ Initializes to the first available COM port """
        available_com_ports = facade.get_available_com_ports()

        if (len(available_com_ports) > 0):
            facade.set_com_port(available_com_ports[0][0])
    
    def __open_solenoid_setup_window(self, menu_item):
        """ Opens the solenoid setup window

        Keyword arguments:
        menu_item -- object the action occured on

        """
        #set the current solenoid step value in the textbox
        solenoid_step_entry = self.__builder.get_object("solenoid_step_entry1")
        solenoid_step_entry.set_text(str(self.__solenoid_step))

        #set the desired current value in the textbox
        solenoid_desired_current_entry = self.__builder.get_object("solenoid_adc_entry")
        solenoid_desired_current_entry.set_text(str(facade.get_desired_current()))

        solenoid_setup_window = self.__builder.get_object("solenoid_setup_window")
        # do not listen for close events in order for the close button on the
        # window to work, as you are unable to add a signal to the close button
        solenoid_setup_window.run()
        solenoid_setup_window.hide()

        #sets the solenoid step
        solenoid_step = solenoid_step_entry.get_text()

        if solenoid_step.isdigit():
            self.__solenoid_step = int(solenoid_step)
        else:
            log.log_error("The magnitude of solenoid time must be an integer,"\
                          " '{0}' is not an integer.".format(magnitude))

        #sets the desired current for solenoids
        solenoid_desired_current = solenoid_desired_current_entry.get_text()

        try:
            facade.set_desired_current(float(solenoid_desired_current))
        except ValueError:
            log.log_error("The desired current must be a decimal number,"\
                          " '{0}' is not an integer.".format(solenoid_desired_current))

        #switches the adc
        toggle_solenoid_adc = self.__builder.get_object("toggle_solenoid_adc")
        if toggle_solenoid_adc.get_active():
            response = facade.toggle_solenoid_adc()

            if response != None:
                switch_actuator_axis.set_active(response)

    def __open_actuator_setup_window(self, menu_item):
        """ Opens the actuator setup window

        Keyword arguments:
        menu_item -- object the action occured on

        """
        #set the combo box values
        com_port_combo = self.__builder.get_object("com_port_combo")
        available_com_ports = facade.get_available_com_ports()
        com_port_liststore = self.__builder.get_object("com_port_liststore")
        com_port_liststore.clear()

        for com_port_info in available_com_ports:
            com_port_combo.append_text(com_port_info[0])

        com_port_combo.set_active(0)

        #set the current actuator step value in the textbox
        actuator_step_entry = self.__builder.get_object("actuator_step_entry")
        actuator_step_entry.set_text(str(facade.get_speed()))

        actuator_setup_window = self.__builder.get_object("actuator_setup_window")
        # do not listen for close events in order for the close button on the
        # window to work, as you are unable to add a signal to the close button
        actuator_setup_window.run()
        actuator_setup_window.hide()

        #sets the com-port for the actuators
        facade.set_com_port(com_port_combo.get_active_text())

        #sets the actuator step
        actuator_step = actuator_step_entry.get_text()

        if actuator_step.isdigit():
            facade.change_speed(int(actuator_step), None)
        else:
            log.log_error("The magnitude of actuator step must be an integer,"\
                          " '{0}' is not an integer.".format(magnitude))

        #switches the actuator axis if the box was checked
        switch_actuator_axis = self.__builder.get_object("switch_actuator_axis")

        if switch_actuator_axis.get_active():
            facade.switch_actuator_axis()
            switch_actuator_axis.set_active(False)

    def __refresh_maze_frame(self, item):
        """ Refresh camera frame in maze window,
        clearing the corner configuration clicks. """
        field_image = self.__builder.get_object("field_image")
        #field_image.set_from_pixbuf(gtk.gdk.pixbuf_new_from_array(facade.get_frame_with_corners(), gtk.gdk.COLORSPACE_RGB, 8))
        field_image.set_from_pixbuf(gtk.gdk.pixbuf_new_from_array(facade.get_frame_with_points(), gtk.gdk.COLORSPACE_RGB, 8))
        #log.log_info("Refreshing maze image...")

    def __confirm_maze_frame(self, item):
        """ Confirm the corners of the maze that have been set up """
        log.log_info("Navigating maze...")

        # Cleanup maze window 
        maze_window = self.__builder.get_object("maze_window")
        maze_window.hide()

        self.__navigate_maze(item)
    
    def __mark_corner(self, item, mouse_event):
        """ Marks a corner of the field on the camera frame
        (thus allowing us to determine acceptable alignments
        for the robot during maze navigation) """
        
        # Current order of marking is top left, top right, bot left, bot right
        facade.mark_corner(mouse_event)
        self.__refresh_maze_frame(item)

    def __mark_path(self, item, mouse_event):
        """ Marks a path of the field on the camera frame
        (thus allowing us to determine a path for the robot to follow) """
        facade.mark_path(mouse_event)
        self.__refresh_maze_frame(item)
    
    def __path_reset(self, item, event):
        """ Resets path of the field on the camera frame of the maze window """
        if event.keyval == 114:   #Resets with key 'r'
            facade.reset_path()

        self.__refresh_maze_frame(item)

    def __preview_camera_feed(self, menu_item):
        """ Display the output of the camera (crudely) """
        facade.display_feed()


    def __preview_image_recognition(self, menu_item):
        """ Display the image recognition feed preview window """
        ir_window = self.__builder.get_object("ir_window")
        self.__refresh_ir_cam_frame(menu_item)
        ir_window.queue_draw()
        ir_window.show()

    def __scale_with_aspect_ratio(self, image, new_x, new_y):
        fx = image.get_width()
        fy = image.get_height()

        if (fy > fx):
            new_x = (int)(((float)(fx)/fy)*new_y)
        elif (fx > fy):
            new_y = (int)(((float)(fy)/fx)*new_x)
        else:
            pass

        return image.scale_simple(new_x, new_y, gtk.gdk.INTERP_BILINEAR)


    def __refresh_ir_cam_frame(self, item):
        """ Refresh the camera frame for the IR preview """
        cam_image = self.__builder.get_object("cam_image")
        ir_image = self.__builder.get_object("ir_image")

        frame = facade.get_frame_bgr_to_rgb()
        ir_frame = facade.find_robot_in_frame(frame)

        cam_image.set_from_pixbuf(self.__scale_with_aspect_ratio(gtk.gdk.pixbuf_new_from_array(frame, gtk.gdk.COLORSPACE_RGB, 8), 400, 400))
        ir_image.set_from_pixbuf(self.__scale_with_aspect_ratio(gtk.gdk.pixbuf_new_from_array(ir_frame, gtk.gdk.COLORSPACE_RGB, 8), 400, 400))

    def __select_image_file(self, item):
        """ Open the image selector for testing various images
        with the image recognition """
        cam_image = self.__builder.get_object("cam_image")
        ir_image = self.__builder.get_object("ir_image")
        chooser = gtk.FileChooserDialog(title="Select an image to preview image recognition",action=gtk.FILE_CHOOSER_ACTION_OPEN,
                                          buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
        filter = gtk.FileFilter()
        filter.set_name("Images")
        filter.add_mime_type("image/png")
        filter.add_mime_type("image/jpeg")
        filter.add_mime_type("image/gif")
        filter.add_pattern("*.png")
        filter.add_pattern("*.jpg")
        filter.add_pattern("*.gif")
        filter.add_pattern("*.tif")
        filter.add_pattern("*.xpm")
        chooser.add_filter(filter)

        response = chooser.run()
        if response == gtk.RESPONSE_OK:
            # Refresh image if one was successfully chosen
            frame = facade.get_image_from_file(chooser.get_filename())
            preview_frame = gtk.gdk.pixbuf_new_from_file_at_size(chooser.get_filename(), 400, 400)
            cam_image.set_from_pixbuf(preview_frame)
            ir_frame = facade.find_robot_in_frame(frame)

            # Scale IR frame to preview dimensions
            ir_image.set_from_pixbuf(self.__scale_with_aspect_ratio(gtk.gdk.pixbuf_new_from_array(ir_frame, gtk.gdk.COLORSPACE_RGB, 8), 400, 400))

            #print chooser.get_filename(), 'selected'
        elif response == gtk.RESPONSE_CANCEL:
            pass
            #print 'Closed, no files selected'
        chooser.destroy()

    def __switch_mode_EMMA_solenoid(self, check_menu_item):
        """ Checks to see if EMMA mode is being enabled

        Keyword arguments:
        check_menu_item -- object the action occured on

        """
        if check_menu_item.active:
            facade.switch_to_EMMA_solenoid()

    def __switch_mode_EMMA_actuator(self, check_menu_item):
        """ Checks to see if EMMA mode is being enabled

        Keyword arguments:
        check_menu_item -- object the action occured on

        """
        if check_menu_item.active:
            facade.switch_to_EMMA_actuator()

    def __toggle_keyboard_input(self, menu_item):
        """ Updates keyboard input variable

        Keyword arguments:
        check_menu_item -- object the action occured on

        """
        self.__keyboard_input ^= True;

app = MainWindow()
gtk.gdk.threads_init()
gtk.main()
