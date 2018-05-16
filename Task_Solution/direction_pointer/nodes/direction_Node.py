#!/usr/bin/env python
import numpy as np
import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import String
import re

def determine_Direction(data):
	# data: [[None, 'YELLOW', None], [[], [296.98000000000002, 277.44], []]]
	data2 = eval(data.data)
	# print "starting of determine_Direction"
	# color_Type =data1[0]
	blu =  list()
	yb = None
	y_yelo =None
	direction = None
	if data2:
		# print "inside while loop"
		data1 = eval(data.data)
		color_Type = data1[0] # [blue,yellow,red] 
		cordinate_BYR = data1[1] # [[x,y],[x,y],[x,y]]
		if cordinate_BYR[0] and not(data2[0][2]):
			blu = cordinate_BYR[0] # x,y for blue
			xb =blu[0]
			yb =blu[1]
		if cordinate_BYR[1] and not(data2[0][2]):
			yelo = cordinate_BYR[1] # x,y for yellow 
			x_yelo = yelo[0] # x cordinate of yellow
			y_yelo = yelo[1]
		if  yb and y_yelo:
			
			if (yb < y_yelo):
			#print "blue is on the Top"
				direction= "go left"
			elif yb > y_yelo:
			#print "yellow is on the Top" 
				direction = "go Right"
		else:
			pass
	else:
		pass
	if direction != None:
		print direction
# while :
# 	pass
def main():

	while not rospy.is_shutdown():
		# print "inside rospy.is_sho"


		rospy.init_node("direction_node")  # initiate a node named 'image_publisher3'

		sub = rospy.Subscriber('Blob_values', String, determine_Direction)
		# print "The Right direction is........."

		rospy.spin()

if __name__ == '__main__':
	main()
