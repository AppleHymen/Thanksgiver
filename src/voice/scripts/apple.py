#! /usr/bin/env python
import rospy
from sensor_msgs.msg import Joy
import os
import threading

#global variables
lastButtonPressed = None
spd_say_thread = None
timeoutOccurred = False 

def systemCalled():
	global lastButtonPressed
	global timeoutOccurred

	thingsToSay = ['"We lie best when we lie to ourselves"', '"No one ever does live happily ever after, but we leave the children to find that out for themselves"','"When all else fails, give up and go to the library"','"If you do not control your temper, your temper will control you"','"The world had teeth and it could bite you with them anytime it wanted"','"People do not get better, they just get smarter. When you get smarter you do not stop pulling the wings of flies, you just think of better reasons for doing it"','"Sometimes loving eyes do not see what they do not want to see"','"It is best to be ruthless with the past"']
	if lastButtonPressed is not None and lastButtonPressed < len(thingsToSay): # if phrase defined
		os.system('spd-say ' + thingsToSay[lastButtonPressed] + ' --wait') #Calls spd-say pkg from system and waits until phrase is completed
	else:
		# if phrase not defined
		os.system('spd-say ' + '"Button Undefined"' + ' --wait')
	timeoutOccurred = True

def callback(joy_input):
	global lastButtonPressed
	global timeoutOccurred
	global spd_say_thread

	if lastButtonPressed is None: # if waiting for a button
		#create list of indices containing only buttons pressed
		pressed = [index for index in range(0, len(joy_input.buttons)) if joy_input.buttons[index]] 
		if len(pressed) > 0: # if there are buttons pressed
			lastButtonPressed = pressed[0] #sets the last button pressed to the first index in the list pressed 
			spd_say_thread = threading.Thread(target=systemCalled)	# sets thread to system call function
			spd_say_thread.start() # starts thread
	else: # if button already pressed
		# determines if something has been said and if the button is no longer pressed if so - resets global variables
		if timeoutOccurred and not joy_input.buttons[lastButtonPressed]: 
			timeoutOccurred = False
			lastButtonPressed = None

def listener():
	rospy.init_node('voice_controller', anonymous=True)
	rospy.Subscriber("joy", Joy,callback) # (topic, msg, function) defines func called when a msg is recieved
	rospy.spin() #keeps us in the function servicing callbacks

if __name__ == '__main__':
	listener()

