import cv2 as cv2  
import numpy as np

# Create a video capture feed from first available video input
vc = cv2.VideoCapture(1)

# Create OpenCV window to show output
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

