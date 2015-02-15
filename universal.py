#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import time
import cPickle as pickle


#           r    g   b
pins_rgb = [17, 18, 22] # red, green, blue pins
pins_white = [27]
pins = [] # pins list to work with later

white = 1 # set to 1 for only white, to 0 for only rgb and to 2 for both

if(white == 0):
	pins = pins_white
elif(white == 1):
	pins = pins_rgb
elif(white == 2):
	pins = pins_white
	pins.extend(pins_rgb)

speedfactor=2

actualLuminances = {}
filename = ".luminances.p"
try:
	pickle.load(open(filename, "rb"))
except Exception:
	for pin in range(len(pins)):
		actualLuminances[pins[pin]] = 0
	pickle.dump(actualLuminances, open(filename, "wb")
actualLuminance = 0
printLuminance=0

linear=0
experimental=0
exp2factor=3


args = sys.argv # get the arguments php gave us when calling the script
fade = args[1] 
# targeted luminance: white,  red,    green,    blue
targetLuminances = {} # empty dictionary, will be filled right next:
for i in range(0, len(pins)):
	targetLuminances[pins[i]] = (int(args[i + 2]) * 10) # we have to add 2 because pins start with the third argument (1st is name of script, 2nd fade)


steps=1000
stepwidth=1

standard_output = sys.stdout

piblaster = open("/dev/pi-blaster", "w")

def switch_leds(pin, pwm_value):
	sys.stdout = piblaster # set stdout so that the command is sent to /dev/pi-blaster
	print str(pin) + "=" + str(pwm_value)
	sys.stdout = standard_output # set stdout to the original value so that we can debug


#if fade:
#	while actualLuminance < targetLuminance:
#		if experimental==1:
#			stepwidth = float(steps) / (targetLuminance - actualLuminance)	
#		if experimental==2:
#			stepwidth = float(steps) / ((targetLuminance - actualLuminance)*exp2factor)		
#		nextLuminance = actualLuminance + stepwidth	
#		printLuminance = float(nextLuminance)/steps
#		switch_leds(pin, printLuminance)
#		actualLuminance = nextLuminance



# turn all leds off
for pinNr in range(len(pins)):
	switch_leds(pins[pinNr], 0)


for color in range(0, len(pins)):
	if fade:
		colorPin = pins[color] # pin for the current color
#		print colorPin
		colorTargetLuminance = float(targetLuminances[colorPin]) # targetLuminance for the current color
		actualLuminance = 0
		if actualLuminance < colorTargetLuminance:
			while actualLuminance < colorTargetLuminance:
				if experimental==1:
					stepwidth = float(steps) / (colorTargetLuminance - actualLuminance)	
				if experimental==2:
					stepwidth = float(steps) / ((colorTargetLuminance - actualLuminance)*exp2factor)		
				nextLuminance = actualLuminance + stepwidth	
				printLuminance = float(nextLuminance)/steps
				switch_leds(colorPin, printLuminance)
				actualLuminance = nextLuminance
		elif actualLuminance > colorTargetLuminance:
			while actualLuminance > colorTargetLuminance:
				if experimental==1:
					stepwidth = float(steps) / (actualLuminance - colorTargetLuminance)	
				if experimental==2:
					stepwidth = float(steps) / ((actualLuminance - colorTargetLuminance)*exp2factor)		
				nextLuminance = actualLuminance - stepwidth	
				printLuminance = float(nextLuminance)/steps
				print printLuminance
				switch_leds(colorPin, printLuminance)
				actualLuminance = nextLuminance
