#!/usr/bin/env python
import numpy as np
import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import String

def calculate_Center(blue_mask1,yellow_mask1,red_mask1):
	center_of_blue = list()
	center_of_yellow  = list()
	center_of_red = list()

	(X_red, Y_red) = red_mask1.shape
	(X_blue, Y_blue) = blue_mask1.shape
	(X_yellow, Y_yellow) = yellow_mask1.shape
	m_red = np.zeros((X_red, Y_red))
	m_blue = np.zeros((X_blue, Y_blue))
	m_yellow = np.zeros((X_yellow, Y_yellow))

	# Determining the center for YELLOW Object
	if yellow_mask1.any(): # To check the color object is available
		for x1 in range(X_yellow):
			for y1 in range(Y_yellow):
				if yellow_mask1[(x1,y1)]:
					m_yellow[x1, y1] = yellow_mask1[x1, y1]
		m_yellow = m_yellow / np.sum(np.sum(m_yellow))
		dx1 = np.sum(m_yellow, 1)
		dy1 = np.sum(m_yellow, 0)
		# expected values
		cy_yellow = np.sum(dx1 * np.arange(X_yellow))
		cx_yellow = np.sum(dy1 * np.arange(Y_yellow))
		center_of_yellow.append(cx_yellow)
		center_of_yellow.append(cy_yellow)

	# Determining the center for BLUE Object
	if blue_mask1.any():  # To check the color object is available
		for x in range(X_blue):
			for y in range(Y_blue):
				if blue_mask1[(x,y)]:
					m_blue[x, y] = blue_mask1[x, y]
		m_blue = m_blue / np.sum(np.sum(m_blue))
		dx = np.sum(m_blue, 1)
		dy = np.sum(m_blue, 0)
		# expected values
		cy_blue = np.sum(dx * np.arange(X_blue))
		cx_blue = np.sum(dy * np.arange(Y_blue))
		center_of_blue.append(cx_blue)
		center_of_blue.append(cy_blue)

	# Determining the center for RED Object
	if red_mask1.any():  # To check the color object is available
		for x2 in range(X_red):
			for y2 in range(Y_red):
				if red_mask1[x2,y2]:
					m_red[x2,y2] = red_mask1[x2,y2]
		m_red = m_red/np.sum(np.sum(m_red))
		dx2 = np.sum(m_red,1)
		dy2 = np.sum(m_red,0)
		cx_red = np.sum(dx2 * np.arange(X_red))
		cy_red = np.sum(dy2 * np.arange(Y_red))
		center_of_red.append(cx_red)
		center_of_red.append(cy_red)
	Calculated_center_BYR = [center_of_blue, center_of_yellow, center_of_red] # Lists of List
	return Calculated_center_BYR

def color_range(hsv1):
	Cmask = None
	RedColor = None
	BlueColor = None
	YellowColor = None
	# define range of blue color in HSV
	lower_blue = np.array([75,175,100])
	upper_blue = np.array([138,255,255])
	blue_mask = cv2.inRange(hsv1,lower_blue,upper_blue)

	# Dilate image to make white blobs larger
	new_hsv = cv2.dilate(hsv1, None, iterations = 1)

	#define range of red color in HSV
	lower_red = np.array([174, 90, 110])
	upper_red = np.array([179, 255, 255]) 
	red_mask = cv2.inRange(hsv1,lower_red,upper_red)

	#define range of green color in HSV
	lower_green = np.array([52, 100, 100])
	upper_green = np.array([75, 255, 255])
	green_mask = cv2.inRange(hsv1,lower_green,upper_green)
	#define range of blue yellow in HSV
	lower_yellow = np.array([20,  80,  150]) #lower_yellow = np.array([20, 180, 150]) if the Yellow is very light 
	upper_yellow = np.array([40, 255, 255])
	yellow_mask = cv2.inRange(hsv1,lower_yellow, upper_yellow)
	#new_mask = red_mask
	
	if red_mask.any() and not (blue_mask.any()) and not(yellow_mask.any()):
		#print "red found"
		RedColor = "RED"
	elif red_mask.any() and blue_mask.any() and not(yellow_mask.any()):
		RedColor = "RED"
		BlueColor = "BLUE"
		Cmask = red_mask
	elif red_mask.any() and yellow_mask.any() and not(blue_mask.any()):
		RedColor = "RED"
		YellowColor = "YELLO'W"
		Cmask = yellow_mask + red_mask
	elif blue_mask.any() and not(red_mask.any()) and not(yellow_mask.any()):
		BlueColor = "BLUE"
		Cmask = blue_mask

	elif blue_mask.any() and yellow_mask.any() and not(red_mask.any()):
		BlueColor = "BLUE"
		YellowColor = "YELLOW"
		Cmask = blue_mask + yellow_mask
	elif yellow_mask.any() and not(blue_mask.any()) and not(red_mask.any()):
		YellowColor = "YELLOW"
		Cmask = yellow_mask
	elif yellow_mask.any() and blue_mask.any() and red_mask.any():
		RedColor   = "RED"
		BlueColor  = "BLUE"
		YellowColor= "YELLOW"
		Cmask = red_mask + blue_mask + yellow_mask
		#print yellow_mask.size

	else:
		exit()
		Cmask = None
	# cv2.imshow("the mask",Cmask)
		#List_of_Color_in_BYR = list()
	# TO Calculate the center of the object(BLOB) on the image 
	Center_of_blobs_in_BYR = calculate_Center(blue_mask,yellow_mask,red_mask) # Lists of List of int values
	List_of_Color_in_BYR = [BlueColor,YellowColor,RedColor] # List of String Values
	# cv2.imshow("yellow mask",yellow_mask)

	return List_of_Color_in_BYR,Center_of_blobs_in_BYR,Cmask

def callback(data):
	cvbridge = CvBridge()
	windos_name = "hsv_formatted_image"
    #into opencv type 
	cv_image = cvbridge.imgmsg_to_cv2(data, "bgr8")
    # Convert to HSV type
	hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV) 

	colors_BYR,Locations_BYR,color_Mask = color_range(hsv)
	print "The ditected Colors(blobs)"
	for i in colors_BYR:
		print i
	print "The Right direction is........."


	# rospy.init_node("image_subscriber",anonymous = True)

	pub = rospy.Publisher('Blob_values', String,queue_size = 1)
	rate = rospy.Rate(2) # 10hz
	while not rospy.is_shutdown():
		try:

			hello_str = [colors_BYR,Locations_BYR]
			if Locations_BYR:
				hello_str = str(hello_str)
			#	print type(hello_str)
			#	print hello_str

				pub.publish(hello_str)
				rate.sleep()

			else :
				continue
		except :
			pass 
	# if color_Mask != None:
	# 	res = cv2.bitwise_and(cv_image,img2, mask= mask)

rospy.init_node("image_subscriber",anonymous = True)
sub = rospy.Subscriber("Camera_image", Image, callback)
rospy.spin()

# if __name__ == '__main__':
# 	# listener()
# 	main()
