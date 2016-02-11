#! /usr/bin/env python

import rospy
from sensor_msgs.msg import Joy
from roboclaw_driver.roboclaw_driver import Roboclaw

left_wheels = None
left_address = None
right_wheels = None
right_address = None

def motor_cb(joy_msg):
	global left_wheels
	global right_wheels
	global left_address
	global right_address	
	# the left bumper will be safety
	safety_key_index = 4
	# left joystick, up down axis
	left_wheel_index = 1
	# right joystick, up down axis
	right_wheel_index = 4
	# half of the range, to protect the motors
	max_duty = 32768 / 2
	
	#print ("in cb") 

	if (joy_msg.buttons[safety_key_index]):
		left_wheel_percentage = joy_msg.axes[left_wheel_index]
		right_wheel_percentage = joy_msg.axes[right_wheel_index]
		left_wheel_duty = int(max_duty * left_wheel_percentage)
		right_wheel_duty = int(-1 * max_duty * right_wheel_percentage)
		left_wheels.DutyM1M2(left_address, left_wheel_duty, left_wheel_duty)
		right_wheels.DutyM1M2(right_address, right_wheel_duty, right_wheel_duty)	
		#print (left_wheel_duty)
		#print (right_wheel_duty)	
	else:
		# stop the wheels
		left_wheels.DutyM1M2(left_address, 0, 0)
		right_wheels.DutyM1M2(right_address, 0, 0)
#		print ("stopping")

def listener():
	global left_wheels
	global right_wheels
	global left_address
	global right_address

	rospy.init_node('motor_controller', anonymous=True)
	
	left_address = int(rospy.get_param("~leftAddress", 129))
	right_address = int(rospy.get_param("~rightAddress", 134))
	left_dev = rospy.get_param("~leftdev", "/dev/ttyACM1")
	right_dev = rospy.get_param("~rightdev", "/dev/ttyACM0")

	#if not left_dev or not right_dev:
#		rospy.signal_shutdown("Failed to get device") 

#	if not left_address or not right_address:
#		rospy.signal_shutdown("Failed to get address")
	
	left_wheels = Roboclaw(left_dev, 115200)
	right_wheels = Roboclaw(right_dev, 115200)	

	left_wheels.Open()
	right_wheels.Open()
	print ("in listener")
	rospy.Subscriber("joy", Joy, motor_cb)
	rospy.spin()

if __name__ == '__main__':
	listener()
