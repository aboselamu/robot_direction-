#!/usr/bin/python


# THE FUNCTION WHICH CALCULATE THE CENTER OF THE OBJECT 
def calculate_Center(red_mask,blue_mask,yellow_mask) :
	# defining the variable
	go_to = None
	center_of_red = list()
	center_of_blue = list()
	center_of_yellow  = list()

	(X_red, Y_red) = red_mask.shape
	(X_blue, Y_blue) = blue_mask.shape
	(X_yellow, Y_yellow) = yellow_mask.shape
	m_red = np.zeros((X_red, Y_red))
	m_blue = np.zeros((X_blue, Y_blue))
	m_yellow = np.zeros((X_yellow, Y_yellow))

	# Determining the center for YELLOW Object
	if yellow_mask.any(): # To check the color object is available
		for x1 in range(X_yellow):
			for y1 in range(Y_yellow):
				if yellow_mask[(x1,y1)]:
					m_yellow[x1, y1] = yellow_mask[x1, y1]
		m_yellow = m_yellow / np.sum(np.sum(m_yellow))
		dx1 = np.sum(m_yellow, 1)
		dy1 = np.sum(m_yellow, 0)
		# expected values
		cy_yellow = np.sum(dx1 * np.arange(X_yellow))
		cx_yellow = np.sum(dy1 * np.arange(Y_yellow))
		center_of_yellow.append(cx_yellow)
		center_of_yellow.append(cy_yellow)

	# Determining the center for BLUE Object
	if blue_mask.any():  # To check the color object is available
		for x in range(X_blue):
			for y in range(Y_blue):
				if blue_mask[(x,y)]:
					m_blue[x, y] = blue_mask[x, y]
		m_blue = m_blue / np.sum(np.sum(m_blue))
		dx = np.sum(m_blue, 1)
		dy = np.sum(m_blue, 0)
		# expected values
		cy_blue = np.sum(dx * np.arange(X_blue))
		cx_blue = np.sum(dy * np.arange(Y_blue))
		center_of_blue.append(cx_blue)
		center_of_blue.append(cy_blue)

	# Determining the center for RED Object
	if red_mask.any():  # To check the color object is available
		for x2 in range(X_red):
			for y2 in range(Y_red):
				if red_mask[x2,y2]:
					m_red[x2,y2] = red_mask[x2,y2]
		m_red = m_red/np.sum(np.sum(m_red))
		dx2 = np.sum(m_red,1)
		dy2 = np.sum(m_red,0)
		cx_red = np.sum(dx2 * np.arange(X_red))
		cy_red = np.sum(dy2 * np.arange(Y_red))
		center_of_red.append(cx_red)
		center_of_red.append(cy_red)
	# Determine the direction of the Robot
	if blue_mask.any() and yellow_mask.any():
		if (cy_blue < cy_yellow) :
			print "blue is on the Top"
			go_to = "Left"
		else:
			print "yellow is on the Top" 
			go_to = "Right"
	return go_to,center_of_yellow,center_of_blue,center_of_red
#THE END OF CALCULATE_CENTER FUNCTION


def color_range(hsv):
	Cmask = None
	# define range of blue color in HSV
	lower_blue = np.array([75,175,100])
	upper_blue = np.array([138,255,255])
	blue_mask = cv2.inRange(hsv,lower_blue,upper_blue)

	# Dilate image to make white blobs larger
	new_hsv = cv2.dilate(hsv, None, iterations = 1)

	#define range of red color in HSV
	lower_red = np.array([174, 90, 110])
	upper_red = np.array([179, 255, 255]) 
	red_mask = cv2.inRange(hsv,lower_red,upper_red)

	#define range of green color in HSV
	lower_green = np.array([52, 100, 100])
	upper_green = np.array([75, 255, 255])
	green_mask = cv2.inRange(hsv,lower_green,upper_green)
	#define range of blue yellow in HSV
	lower_yellow = np.array([20,  80,  50]) #lower_yellow = np.array([20, 180, 150]) if the Yellow is very light 
	upper_yellow = np.array([40, 255, 255])
	yellow_mask = cv2.inRange(hsv,lower_yellow, upper_yellow)
	#new_mask = red_mask
	if red_mask.any() and not (blue_mask.any()) and not(yellow_mask.any()):
		print "red found"
		Cmask = red_mask
		direction,C_yellow,C_blue,C_red = calculate_Center(Cmask,blue_mask,yellow_mask)
	
	elif yellow_mask.any() and blue_mask.any() and not(red_mask.any()):
		Cmask = blue_mask + yellow_mask
		direction,C_yellow,C_blue,C_red = calculate_Center(red_mask,blue_mask,yellow_mask)
		print direction
		# print "yellow center"
		# print C_yellow
		# print blue_mask.size
		# print yellow_mask.size

	else:
		# print "NOT THE RIGHT DIRECTION"
		exit()
	return Cmask

import cv2
import numpy as np;
 
def main ():
	img2 = cv2.imread("Blue_on_Top.png") #different_color,onlyYandBlue
	#(X, Y) = img2.size
	# print img2.size
	hsv = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)
	# print " the shape of image"
	# print img2.shape[0:2] # get the size of the images
	mask = color_range(hsv)
	res = cv2.bitwise_and(img2,img2, mask= mask)
	cv2.imshow('mask',mask)
	cv2.imshow('RED',res)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

if __name__ == '__main__':
	main()
