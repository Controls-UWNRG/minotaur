""" Image Recognition Module """

import math as math
import log as log
import cv2 as cv2
from cv2 import cv
import numpy as np

class ImageRecognition:
    # Video input source.
    __vc = {}
    '''
    corner_count = 0 
    corner_x = {}
    corner_y = {}
    '''
    point_count = 0
    point_x = {}
    point_y = {}

    __constant = 3.4
    __aperture_width = 17
    __block_size = 53

    def __init__(self):
        # Use the video feed from the camera.
        # TODO: Only activate the camera if set to do so in a settings menu -- keep this code here til waterloo looks at it
        self.__vc = cv2.VideoCapture(0)

        # Use the video feed from a test video
        #self.__vc = cv2.VideoCapture("test3.avi")
        pass

    def get_robot_location(self, monoframe):
        """ Finds the square most likely to be EMMA and returns its center point

        Keyword Arguments:
        monoframe -- the thresholded frame from the camera
        detail -- look at every 'n' pixels
        
        """
        return self.find_blob(monoframe, 3, 255)

        """
        # NOTE: This is actually somewhat excessive, given our aggressive thresholding

    	# Detect squares
    	img = cv2.GaussianBlur(monoframe, (5, 5), 0)
    	squares = []
    	
        for gray in cv2.split(img):
    	    for thrs in xrange(0, 255, 26):
    		if thrs == 0:
    		    bin = cv2.Canny(gray, 0, 50, apertureSize=5)
    		    bin = cv2.dilate(bin, None)
    		else:
    		    retval, bin = cv2.threshold(gray, thrs, 255, cv2.THRESH_BINARY)
    		bin, contours, hierarchy = cv2.findContours(bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    		for cnt in contours:
    		    cnt_len = cv2.arcLength(cnt, True)
    		    cnt = cv2.approxPolyDP(cnt, 0.02*cnt_len, True)
    		    if len(cnt) == 4 and cv2.contourArea(cnt) > 1000 and cv2.isContourConvex(cnt):
    			cnt = cnt.reshape(-1, 2)
    			max_cos = np.max([angle_cos( cnt[i], cnt[(i+1) % 4], cnt[(i+2) % 4] ) for i in xrange(4)])
    			if max_cos < 0.1:
    			    squares.append(cnt)
        # TODO: Determine which square is likely our robot, and return its center
        return squares

        """

    def mark_corner(self, x, y):
        #TODO: Reduce since we only really need top left corner and bottom right
        self.corner_x[self.corner_count] = x
        self.corner_y[self.corner_count] = y
        self.corner_count += 1
        #print(self.corner_count)

    def reset_corners(self):
        for i in range(0, self.corner_count):
            self.corner_x[i] = -1
            self.corner_y[i] = -1
        self.corner_count = 0

    def mark_point(self, x, y):
        self.point_x[self.point_count] = x
        self.point_y[self.point_count] = y
        self.point_count += 1

    def reset_points(self):
        for i in range(0, self.point_count):
            self.point_x[i] = -1
            self.point_y[i] = -1
        self.point_count = 0

    def find_robot_in_frame(self, frame):
        """ Returns a frame post-image recognition with the robot
        clearly marked """
        proc_frame = self.process_frame(frame)

        # Find the robot
        point = self.get_robot_location(proc_frame)
        #point = (100, 100)

        # Copy processed image to a colour frame
        col_frame = cv2.cvtColor(proc_frame, cv.CV_GRAY2BGR)

        # Annotate the new image
        cv2.circle(col_frame, point, 10, (255, 0, 0), -1)
        
        return col_frame
  
    def get_frame_with_points(self):
        frame = self.get_frame()
        
        for i in range(0, self.point_count):
            cv2.circle(frame, ((int)(self.point_x[i]), (int)(self.point_y[i])), 5, (160,160,250))
            for j in range(0, i):
                cv2.line(frame, ((int)(self.point_x[j]), (int)(self.point_y[j])), ((int)(self.point_x[j+1]),(int)(self.point_y[j+1])), (255, 255, 255))
       
        return np.asarray(frame)
    
    def get_frame_with_corners(self):
        """ Get numpy frame with corners drawn on, and alignment lines if relevant """
        '''
        frame = self.get_frame()
		
        for i in range(0, self.corner_count):
            cv2.circle(frame, ((int)(self.corner_x[i]), (int)(self.corner_y[i])), 5, (255, 0, 255))

        if self.corner_count == 4:
            # TODO: These should be globals
            ALIGN_TOP = (int) (1.25*(self.corner_y[3] - self.corner_y[0])/10)
            ALIGN_MID = (int) (5*(self.corner_y[3] - self.corner_y[0])/10)
            ALIGN_BOT = (int) (8.75*(self.corner_y[3] - self.corner_y[0])/10)
            ALIGN_LEFT = (int) (1.2*(self.corner_x[3] - self.corner_x[0])/10)
            ALIGN_MID_L = (int) (3.55*(self.corner_x[3] - self.corner_x[0])/10)
            ALIGN_MID_R = (int) (6.45*(self.corner_x[3] - self.corner_x[0])/10)
            ALIGN_RIGHT = (int) (8.8*(self.corner_x[3] - self.corner_x[0])/10)

            cv2.line(frame, (((int)(self.corner_x[0]))+ALIGN_LEFT, (int)(self.corner_y[0])),
                (((int)(self.corner_x[0]))+ALIGN_LEFT, (int)(self.corner_y[3])),
                (140, 140, 140))

            cv2.line(frame, (((int)(self.corner_x[0]))+ALIGN_MID_L, (int)(self.corner_y[0])),
                (((int)(self.corner_x[0]))+ALIGN_MID_L, (int)(self.corner_y[3])),
                (140, 140, 140))

            cv2.line(frame, (((int)(self.corner_x[0]))+ALIGN_MID_R, (int)(self.corner_y[0])),
                (((int)(self.corner_x[0]))+ALIGN_MID_R, (int)(self.corner_y[3])),
                (140, 140, 140))

            cv2.line(frame, (((int)(self.corner_x[0]))+ALIGN_RIGHT, (int)(self.corner_y[0])),
                (((int)(self.corner_x[0]))+ALIGN_RIGHT, (int)(self.corner_y[3])),
                (140, 140, 140))

            # Draw alignment lines TODO: These should be purely dependent on top-left and bottom-right corner
            cv2.line(frame, (((int)(self.corner_x[0])), ALIGN_TOP+(int)(self.corner_y[0])),
                (((int)(self.corner_x[1])), ALIGN_TOP+(int)(self.corner_y[0])),
                (255, 0, 0))

            cv2.line(frame, (((int)(self.corner_x[0])), ALIGN_MID+(int)(self.corner_y[0])),
                (((int)(self.corner_x[1])), ALIGN_MID+(int)(self.corner_y[0])),
                (255, 255, 0))

            cv2.line(frame, (((int)(self.corner_x[0])), ALIGN_BOT+(int)(self.corner_y[0])),
                (((int)(self.corner_x[1])), ALIGN_BOT+(int)(self.corner_y[0])),
                (0, 255, 255))

            # Draw borders around image
            cv2.line(frame, ((int)(self.corner_x[0]), (int)(self.corner_y[0])),
                ((int)(self.corner_x[0]), (int)(self.corner_y[3])),
                (255, 255, 255))

            cv2.line(frame, ((int)(self.corner_x[0]), (int)(self.corner_y[0])),
                ((int)(self.corner_x[3]), (int)(self.corner_y[0])),
                (255, 255, 255))

            cv2.line(frame, ((int)(self.corner_x[0]), (int)(self.corner_y[3])),
                ((int)(self.corner_x[3]), (int)(self.corner_y[3])),
                (255, 255, 255))

            cv2.line(frame, ((int)(self.corner_x[3]), (int)(self.corner_y[0])),
                ((int)(self.corner_x[3]), (int)(self.corner_y[3])),
                (255, 255, 255))

            base_x = self.corner_x[0];
            base_y = self.corner_y[0];

            x_size = self.corner_x[3]-self.corner_x[0]
            y_size = self.corner_y[3]-self.corner_y[0]

            frame[(int)(0.17*y_size+base_y):(int)(0.48*y_size+base_y), (int)(0.18*x_size+base_x):(int)(0.30*x_size+base_x)] = 0xFFFFFF
            frame[(int)(0.17*y_size+base_y):(int)(0.48*y_size+base_y), (int)(0.42*x_size+base_x):(int)(0.60*x_size+base_x)] = 0xFFFFFF
            frame[(int)(0.17*y_size+base_y):(int)(0.48*y_size+base_y), (int)(0.70*x_size+base_x):(int)(0.85*x_size+base_x)] = 0xFFFFFF
            frame[(int)(0.56*y_size+base_y):(int)(0.84*y_size+base_y), (int)(0.18*x_size+base_x):(int)(0.30*x_size+base_x)] = 0xFFFFFF
            frame[(int)(0.56*y_size+base_y):(int)(0.84*y_size+base_y), (int)(0.42*x_size+base_x):(int)(0.60*x_size+base_x)] = 0xFFFFFF
            frame[(int)(0.56*y_size+base_y):(int)(0.84*y_size+base_y), (int)(0.70*x_size+base_x):(int)(0.85*x_size+base_x)] = 0xFFFFFF
   
        return np.asarray(frame)
        '''
    def get_image_from_file(self, path):
        """ Return an OpenCV image from the specified path """
        return cv2.imread(path)

    def get_frame_bgr_to_rgb(self):
        """ Get frame and convert to rgb colorspace """
        frame = self.get_frame()
        rgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        return rgb

    def get_frame_np(self):
        """ Get frame as an array """
        return np.asarray(self.get_frame())

    def get_frame(self):
        """ Get frame as an image """
        rval, frame = self.__vc.read()

        if rval:
            return frame 
        else:
            log.log_error("Could not get frame from video source.")
            return False

    def start_camera_feed(self):
        frame = self.__vc.read()

        if self.__vc.isOpened(): # try to get the first frame
            rval, frame = self.__vc.read()
        else:
            rval = False

        cv2.namedWindow("Camera Feed - Press ESC to Exit")
        bigimage = (())

        while rval:
            rval, frame = self.__vc.read()

            if (rval==0):
                break

            frame = self.get_frame()

            # Simple hack for large resolution viewing.
            bigimage = cv2.resize(frame, (840, 630))

            cv2.imshow("Camera Feed - Press ESC to Exit", bigimage)

            key = cv2.waitKey(5)
            if key == 27: # exit on ESC (TODO: Make it sensitive to the X in the corner)
                break

        cv2.destroyWindow("Camera Feed - Press ESC to Exit")

    def process_frame(self, frame):
        """ Process a (BGR) frame and return it """

        # TODO: This should be encapsulated and abstracted into IR callbacks in the field class or something
        #base_x = self.corner_x[0];
        #base_y = self.corner_y[0];

        #x_size = self.corner_x[3]-self.corner_x[0]
        #y_size = self.corner_y[3]-self.corner_y[0]

	    # This was designed to blot out the pegs in the maze
        #frame[(int)(0.20*y_size+base_y):(int)(0.40*y_size+base_y), (int)(0.18*x_size+base_x):(int)(0.30*x_size+base_x)] = 0xFFFFFF
        #frame[(int)(0.20*y_size+base_y):(int)(0.40*y_size+base_y), (int)(0.42*x_size+base_x):(int)(0.60*x_size+base_x)] = 0xFFFFFF
        #frame[(int)(0.20*y_size+base_y):(int)(0.40*y_size+base_y), (int)(0.70*x_size+base_x):(int)(0.85*x_size+base_x)] = 0xFFFFFF
        #frame[(int)(0.60*y_size+base_y):(int)(0.80*y_size+base_y), (int)(0.18*x_size+base_x):(int)(0.30*x_size+base_x)] = 0xFFFFFF
        #frame[(int)(0.60*y_size+base_y):(int)(0.78*y_size+base_y), (int)(0.42*x_size+base_x):(int)(0.60*x_size+base_x)] = 0xFFFFFF
        #frame[(int)(0.60*y_size+base_y):(int)(0.78*y_size+base_y), (int)(0.70*x_size+base_x):(int)(0.85*x_size+base_x)] = 0xFFFFFF

        #roi = frame[self.corner_y[0]:self.corner_y[3], self.corner_x[0]:self.corner_x[3]]

        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        medfilt=cv2.medianBlur(gray, self.__aperture_width)    # aperture width must be odd
        #tr=cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
        # adaptiveThreshold(image, color, method, type, blcok size, constant C)
        final=cv2.adaptiveThreshold(medfilt,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,self.__block_size,self.__constant)

        #tr=cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
        #final=cv2.medianBlur(tr, 17)    # aperture width must be odd.

        return final
    
    def set_feed(self, camera_feed=None):
        print "feed set"+str(camera_feed)
        self.__vc = cv2.VideoCapture(camera_feed)

    def find_blob(self, monoframe, detail, value):
        """Finds largest blob of (value) pixels in a monochromatic square frame,
        provided the blob is the largest object by far in the area.
        Returns a point at approximately the center, returns -1, -1 if no blob found

        Keyword Arguments:
        monoframe -- the thresholded frame from the camera
        detail -- look at every 'n' pixels
        
        """
        # TODO
        # ie: Use advanced image recognition to find robot for sure at the start,
        # remove robot and ask "What other stuff *almost* looks like a robot
        # and ignore that stuff from now on.

        y_maxloc = -1
        y_max = 0
        rowcount = 0

        for rows in monoframe:
            count = 0
            i = 0

            while i < rows.size:
                if rows[i] == value: # TODO: Add parameter for either black/white blob detect
                    count += 1
                i += detail

            if count > y_max:
                y_max = count
                y_maxloc = rowcount

            rowcount += 1

        x_maxloc = -1
        x_max = 0
        rowcount = 0

        for rows in monoframe.T:
            count = 0
            i = 0

            while i < rows.size:
                if rows[i] == value:
                    count += 1
                i += detail

            if count > x_max:
                x_max = count
                x_maxloc = rowcount

            rowcount += 1

        return (x_maxloc, y_maxloc)

    def find_blob_y(self, monoframe, detail):
        """Finds largest blob of white pixels in a monochromatic square frame,
        provided the blob is the largest object by far in the area.
        Only search on the y-axis.
        Returns a point at approximately the center, returns -1, -1 if no blob found

        Keyword Arguments:
        monoframe -- the thresholded frame from the camera
        detail -- look at every 'n' pixels
        
        """
        
        # Find the x-coordinate with the largest number of white pixels

        y_maxloc = -1
        y_max = 0
        rowcount = 0

        for rows in monoframe:
            count = 0
            i = 0

            # TODO: If necessary, ignore pegs during blobfinding 
            # if row > 60 && row < 80

            while i < rows.size:
                if rows[i] == 0:
                    count += 1
                i += detail

            if count > y_max:
                y_max = count
                y_maxloc = rowcount

            rowcount += 1

        return y_maxloc

    def find_blob_x(self, monoframe, detail):
        """Finds largest blob of white pixels in a monochromatic square frame,
        provided the blob is the largest object by far in the area.
        Only search on the x-axis.
        Returns a point at approximately the center, returns -1, -1 if no blob found

        Keyword Arguments:
        monoframe -- the thresholded frame from the camera
        detail -- look at every 'n' pixels
        
        """
        # Find the x-coordinate with the largest number of white pixels
        x_maxloc = -1
        x_max = 0
        rowcount = 0

        for rows in monoframe.T:
            count = 0
            i = 0

            while i < rows.size:
                if rows[i] == 0:
                    count += 1
                i += detail

            if count > x_max:
                x_max = count
                x_maxloc = rowcount

            rowcount += 1

        return x_maxloc


    def get_distance_to_alignment_x(self, alignment):
        # TODO: Make these globals
        ALIGN_LEFT = (int) (1.2*(self.corner_x[3] - self.corner_x[0])/10)
        ALIGN_MID_L = (int) (3.55*(self.corner_x[3] - self.corner_x[0])/10)
        ALIGN_MID_R = (int) (6.45*(self.corner_x[3] - self.corner_x[0])/10)
        ALIGN_RIGHT = (int) (8.8*(self.corner_x[3] - self.corner_x[0])/10)

        alignpos = -1

        if alignment == 0:
            alignpos = ALIGN_LEFT
        elif alignment == 1:
            alignpos = ALIGN_MID_L
        elif alignment == 2:
            alignpos = ALIGN_MID_R
        else:
            alignpos = ALIGN_RIGHT

        newframe = self.get_frame()
        robo_loc = self.find_blob_x(self.get_field_from_frame(newframe), 2) #TODO: Assess detail resolution

        if (robo_loc == -1):
            print("ROBOT LOST, ABANDON ALL HOPE")

        key = cv2.waitKey(2)
        return (robo_loc-alignpos)

    def get_distance_to_alignment_y(self, alignment):

        # TODO: Make these globals
        ALIGN_TOP = (int) (1.25*(self.corner_y[3] - self.corner_y[0])/10)
        ALIGN_MID = (int) (5*(self.corner_y[3] - self.corner_y[0])/10)
        ALIGN_BOT = (int) (8.75*(self.corner_y[3] - self.corner_y[0])/10)

        alignpos = -1

        if alignment == 0:
            alignpos = ALIGN_TOP
        elif alignment == 1:
            alignpos = ALIGN_MID
        else:
            alignpos = ALIGN_BOT

        newframe = self.get_frame()
        robo_loc = self.find_blob_y(self.get_field_from_frame(newframe), 2) #TODO: Assess detail resolution

        if (robo_loc == -1):
            print("ROBOT LOST, ABANDON ALL HOPE")

        key = cv2.waitKey(2)
        return (robo_loc-alignpos)

    def update_ir_settings(self, constant, block, aperture):
        """ Update settings for image recognition. """
        #TODO: Verification and error handling
        self.__constant = constant
        self.__block = block
        self.__aperture_width = aperture
