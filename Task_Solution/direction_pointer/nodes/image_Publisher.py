#!/usr/bin/env python
import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge,CvBridgeError 	

def send_image(img):
	cvbridge = CvBridge()
	image_pub = rospy.Publisher('Camera_image', Image,queue_size=100) # topic 
	rospy.init_node('image_publisher', anonymous=True)
	rate = rospy.Rate(2) # 10hz
	try:
		image_pub.publish(cvbridge.cv2_to_imgmsg(img, "bgr8"))
	except CvBridgeError, e:
		print e
def main ():
	cap = cv2.VideoCapture(0)
	if cap.isOpened():
		ret,frame = cap.read()
	else:
		ret = False
	while ret:
		ret,frame = cap.read()
		send_image(frame)
		cv2.imshow("from camera",frame)

		if cv2.waitKey(1) & 0xFF == ord('q') :
			break

	cv2.waitKey(0)
	cv2.destroyAllWindows()
if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException:
		pass


# ????????????????????????????????????????????????????????????????????????????????????????????