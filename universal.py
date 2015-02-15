#!/usr/bin/env python
import os
import sys

pins = [27, 17, 18, 22] # white, red, green, blue pins

speedfactor=2

actualLuminance=0
printLuminance=0

linear=0
experimental=2
exp2factor=3


args = sys.argv # get the arguments php gave us when calling the script
fade = args[1] 

# targeted luminance: white,  red,    green,    blue
targetLuminances = {} # empty dictionary, will be filled right next:
for i in range(0, len(pins)):
	targetLuminances[pins[i]] = args[i + 2] # we have to add 2 because pins start with the third argument (1st is name of script, 2nd fade)

schrittweite=1
steps=1000
stepwidth=1

standard_output = sys.stdout

piblaster = open("/dev/pi-blaster", "w")

def switch_leds(pin, pwm_value):
	sys.stdout = piblaster # set stdout so that the command is sent to /dev/pi-blaster
	print str(pin) + "=" + str(pwm_value)
	sys.stdout = standard_output # set stdout to the original value so that we can debug

# turn all leds off
for pinNr in range(len(pins)):
	switch_leds(pins[pinNr], 0)


for color in range(0, len(pins)):
	if fade:
		colorPin = pins[color] # pin for the current color
		print colorPin
		colorTargetLuminance = float(targetLuminances[colorPin]) # targetLuminance for the current color
		actualLuminance = 0
		while actualLuminance < colorTargetLuminance:
			if experimental==1:
				stepwidth = float(steps) / (colorTargetLuminance - actualLuminance)	
			if experimental==2:
				stepwidth = float(steps) / ((colorTargetLuminance - actualLuminance)*exp2factor)		
			nextLuminance = actualLuminance + stepwidth	
			printLuminance = float(nextLuminance)/steps
			switch_leds(colorPin, printLuminance)
			actualLuminance = nextLuminance
