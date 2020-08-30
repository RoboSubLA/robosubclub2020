import cv2
from std_msgs.msg import String
from time import sleep

#the_cascade = cv2.CascadeClassifier('axeCas/Axe_cascade.xml') 		#Which cascade file to use
#the_cascade = cv2.CascadeClassifier('bootleggerCas/cascade.xml') 		#Which cascade file to use

the_cascade = cv2.CascadeClassifier('axeAndbootleggerCascade.xml')
the_camera = cv2.VideoCapture('bootleggerVid.mp4')				#Turn on the camera

while True:							#Until the break

    if not the_camera.isOpened():				#If no camera is detected
        print("There's no camera plugged in dummy")				#
        sleep(5)								#
        pass									#Do nothing

    ret, frame = the_camera.read()				#Record the frame

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)	#This doesnt have to be gray scaled,
    #but the object detection is faster when it doesn't have to scan through 3 extra layers of colors

    upside_down_pi_detection = the_cascade.detectMultiScale(	#Detects objects from cascade
                               gray_frame, scaleFactor=1.1, minNeighbors=3, minSize=(24, 24))

    for (x, y, w, h) in upside_down_pi_detection:		#Make a rectange around detections
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        rect_center_yaw = (x + (w/2))
        rect_center_pitch = (y + (h/2))

    cv2.imshow('Upside Down Pi Finder', frame)			#Show final frame


    if cv2.waitKey(1) == ord('q'):				#If q is pressed, break the true loop
        break

    if len(upside_down_pi_detection) != 0:
        scr_center_yaw = (cv2.getWindowImageRect('Upside Down Pi Finder')[2] / 2)   #center of x-axis
        scr_center_pitch = (cv2.getWindowImageRect('Upside Down Pi Finder')[3] / 2) #center of y-axis
        yaw_error = rect_center_yaw - scr_center_yaw		#Object distance to screen center (x)
        pitch_error = rect_center_pitch - scr_center_pitch	#Object distance to screen center (y)
        object_location = "%s , %s" % (yaw_error, pitch_error)
        print (object_location)

the_camera.release()						#Turn off the camera
cv2.destroyAllWindows()
