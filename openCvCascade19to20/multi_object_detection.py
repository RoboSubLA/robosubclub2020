import cv2
from std_msgs.msg import String
from time import sleep

axe_cascader = cv2.CascadeClassifier('axeCas/Axe_cascade.xml') 		#Which cascade file to use
bootlegger_cascade= cv2.CascadeClassifier('bootleggerCas/Bootlegger_cascade.xml') 		#Which cascade file to use

the_camera = cv2.VideoCapture('testVideos/axeVid2.mp4')			
# the_camera = cv2.VideoCapture('testVideos/bootleggerVid.mp4')
# the_camera = cv2.VideoCapture('testVideos/testVideo.mp4')
while True:							#Until the break
    # fps = the_camera.get(cv2.CAP_PROP_FPS)
    # print("Fps : {0}".format(fps))
    if not the_camera.isOpened():				#If no camera is detected
        print("There's no camera plugged in dummy")				#
        sleep(5)								#
        pass									#Do nothing

    ret, frame = the_camera.read()				#Record the frame

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # gray_frame = frame
    
    bootlegger = bootlegger_cascade.detectMultiScale(gray_frame, scaleFactor=1.1 , minNeighbors=3 , minSize=(75,75))
    axe = axe_cascader.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=3, minSize=(24, 24))


    #MAKE BOUNDING BOX AROUND AXE
    for (x, y, w, h) in axe:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        rect_center_yaw = (x + (w/2))
        rect_center_pitch = (y + (h/2))

    #MAKE BOUNDING BOX AROUND BOOTLEGGER
    for (x, y, w, h) in bootlegger:		
        cv2.rectangle(frame, (x, y), (x+w, y+h), (125, 30, 218), 2)
        rect_center_yaw = (x + (w/2))
        rect_center_pitch = (y + (h/2))

    cv2.imshow('Upside Down Pi Finder', frame)			#Show final frame


    if cv2.waitKey(1) == ord('q'):				#If q is pressed, break the true loop
        break

    if len(axe) != 0:
        scr_center_yaw = (cv2.getWindowImageRect('Upside Down Pi Finder')[2] / 2)   #center of x-axis
        scr_center_pitch = (cv2.getWindowImageRect('Upside Down Pi Finder')[3] / 2) #center of y-axis
        yaw_error = rect_center_yaw - scr_center_yaw		#Object distance to screen center (x)
        pitch_error = rect_center_pitch - scr_center_pitch	#Object distance to screen center (y)
        axe_coordinates = "%s , %s" % (yaw_error, pitch_error)
        print ("Axe_location - " + axe_coordinates)

    
    if len(bootlegger) != 0:
        scr_center_yaw = (cv2.getWindowImageRect('Upside Down Pi Finder')[2] / 2)   #center of x-axis
        scr_center_pitch = (cv2.getWindowImageRect('Upside Down Pi Finder')[3] / 2) #center of y-axis
        yaw_error = rect_center_yaw - scr_center_yaw		#Object distance to screen center (x)
        pitch_error = rect_center_pitch - scr_center_pitch	#Object distance to screen center (y)
        bootlegger_coordinates = "%s , %s" % (yaw_error, pitch_error)
        print ("Bootlegger_location - " + bootlegger_coordinates)

    
the_camera.release()						#Turn off the camera
cv2.destroyAllWindows()