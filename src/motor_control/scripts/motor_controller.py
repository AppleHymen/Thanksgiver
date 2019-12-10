#! /usr/bin/env python


import rospy
from sensor_msgs.msg import Joy
from roboclaw_driver.roboclaw_driver import Roboclaw

# Initializes global variables

# The object that communicates with the the motor controllers

left_Wheels_Motor_Controller = None
right_Wheels_Motor_Controller = None

# The address of each motor controller

left_Wheels_ID = None
right_Wheels_ID = None


def assign_Movement(joy_msg):


# Defines the index in joy.buttons for the button to be used as the "safety"
safety_Trigger_Index = 4

# Defines the index in joy.axes that corresponds with the up/down movement of the left joystick
left_Joy_Index = 1

# Defines the index in joy.axes that corresponds with the up/down movement of the right joystick
right_Joy_Index = 4

# 32768 is the max speed of the motor and it has to be divided in half to accomadate the 24 volt power supply protecting the motors from shorting
max_speed = 32768 / 2

# Checks if Safety is triggered
if (joy.msg.buttons[safety_Trigger_Index] is True):

	# sets variables for the value/position of each joystick
	left_Joy_Position = joy_msg.axes[left_Joy_Index]
	right_Joy_Position = joy_msg.axes[right_Joy_Index]

	# uses the value of the joystick position which is always between -1 and 1 to calculate a percentage of max speed
	left_Wheel_Speed = int(max_speed * left_Joy_Position)
	right_Wheel_Speed = int(
		-1 * max_speed * right_Joy_Position)  # -1 is used to reverse the value due to coordinate direction with left wheel

	# uses the function from the manafacture provided code for the motor controller to assign to wheel speed to both wheels with the left or right wheels ID or address
	left_Wheels_Motor_Controller.DutyM1M2(left_Wheels_ID, left_Wheel_Speed, left_Wheel_Speed)
	right_Wheels_Motor_Controller.DutyM1M2(right_Wheels_ID, right_Wheel_Speed, right_Wheel_Speed)
else:
	# if safety is not triggered then set speed for wheels to 0 or rather stopped
	left_Wheels_Motor_Controller.DutyM1M2(left_Wheels_ID, 0, 0)
	right_Wheels_Motor_Controller.DutyM1M2(right_Wheels_ID, 0, 0)


def listener():
	global left_Wheels_Motor_Controller
	global right_Wheels_Motor_Controller
	global left_Wheels_ID
	global right_Wheels_ID

	rospy.init_node('motor_controller', anonymous=True)

	left_Wheels_ID = int(rospy.get_param("~leftAddress", 129))
	right_Wheels_ID = int(rospy.get_param("~rightAddress", 134))
	left_dev = rospy.get_param("~leftdev", "/dev/ttyACM1")
	right_dev = rospy.get_param("~rightdev", "/dev/ttyACM0")

	left_Wheels_Motor_Controller = Roboclaw(left_dev, 115200)
	right_Wheels_Motor_Controller = Roboclaw(right_dev, 115200)

	left_Wheels_Motor_Controller.Open()
	right_Wheels_Motor_Controller.Open()
	rospy.Subscriber("joy", Joy, assign_Movement)
	rospy.spin()

if __name__ == '__main__':
listener()
