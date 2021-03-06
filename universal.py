#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import time
import pickle

#           r    g   b
pins_rgb = [17, 18, 22] # red, green, blue pins
pins_white = [25]
pins = [] # pins list to work with later


white = 2  # set to 1 for only white, to 0 for only rgb and to 2 for both

experimental=1
exp1factor=0.01
exp2factor=3
firststepwidth=0.001 #stepwidth at currentLuminance=0 in exp1
verschiebungY=1

if(white == 1):
	pins = pins_white
elif(white == 0):
	pins = pins_rgb
elif(white == 2):
	pins = pins_white
	pins.extend(pins_rgb)

print "pins: "	
print pins

speedfactor=2

currentLuminances = {}
filename = "/tmp/luminances.p"
try:
	currentLuminances = pickle.load(open(filename, "rb"))
	if(len(currentLuminances) == 0):
		raise Exception("currentLuminances must have at least one value")
except Exception:
	for pin in range(len(pins)): # create file if it doesn't exist
		currentLuminances[pins[pin]] = 0
	pickle.dump(currentLuminances, open(filename, "wb"))
printLuminance=0

linear=0
#experimental=1



args = sys.argv # get the arguments php gave us when calling the script
fade = args[1] 
# targeted luminance: white,  red,    green,    blue
targetLuminances = {} # empty dictionary, will be filled right next:
for i in range(0, len(pins)):
	targetLuminances[pins[i]] = (int(args[i + 2]) * 10) # we have to add 2 because pins start with the third argument (1st is name of script, 2nd fade)

print "fade: "
print fade
steps=1000
stepwidth=0

standard_output = sys.stdout

piblaster = open("/dev/pi-blaster", "w")

def switch_leds(pin, pwm_value):
	sys.stdout = piblaster # set stdout so that the command is sent to /dev/pi-blaster
	print str(pin) + "=" + str(pwm_value)
	sys.stdout = standard_output # set stdout to the original value so that we can debug

# turn all leds off
#for pinNr in range(len(pins)):
#	switch_leds(pins[pinNr], 0)
print "currentLuminances: "
print currentLuminances

stepwidth=0

if int(fade) == 0: # Fade-Level 0: Nicht faden, hart ein- / ausschalten
	print "Fadelevel 0"
	for color in range(0, len(pins)):
		##
		colorPin = pins[color] # pin for the current color
		print "colorPin: "
		print colorPin
		colorTargetLuminance = float(targetLuminances[colorPin]) # targetLuminance for the current color
		#stepwidth=0
		currentLuminance = currentLuminances[colorPin]
		print "currentLuminance: "
		print currentLuminance
		if int(colorTargetLuminance) == -10:
			continue # abbrechen. -1 (* 10) ist Zeichen, um nichts zu verändern
		##
		switch_leds(colorPin, float(colorTargetLuminance) / steps)
		currentLuminance = colorTargetLuminance
		currentLuminances[colorPin] = currentLuminance # update currentLuminance
		print "targetLuminance: "
		print colorTargetLuminance	
elif int(fade) == 1: # Fade-Level 1: nacheinander Faden
	print "Fadelevel 1"
	for color in range(0, len(pins)):
		##
		colorPin = pins[color] # pin for the current color
		print "colorPin: "
		print colorPin
		
		colorTargetLuminance = float(targetLuminances[colorPin]) # targetLuminance for the current color
		currentLuminance = currentLuminances[colorPin]
		print "currentLuminance: "
		print currentLuminance
		if int(colorTargetLuminance) == -10:
			continue # abbrechen. -1 (* 10) ist Zeichen, um nichts zu verändern
		##
		if currentLuminance < colorTargetLuminance: # hochfaden
			
			while currentLuminance < colorTargetLuminance:
				if experimental==1:
					stepwidth = float(currentLuminance-currentLuminances[colorPin]) * float(exp1factor)	
					if stepwidth < 0.005:
						stepwidth = stepwidth + 0.001
					stepwidth += verschiebungY
				if experimental==2:
					stepwidth = float(steps) / ((colorTargetLuminance - currentLuminance)*exp2factor)		
				nextLuminance = currentLuminance + stepwidth 
				print stepwidth
				
				
				print nextLuminance
				if(nextLuminance > colorTargetLuminance):
					nextLuminance = colorTargetLuminance
				printLuminance = float(nextLuminance)/steps
				switch_leds(colorPin, printLuminance)
				currentLuminance = nextLuminance
		elif currentLuminance > colorTargetLuminance: # runterfaden
			#stepwidth = (currentLuminance/1000) + 1
			while currentLuminance > colorTargetLuminance:
				if experimental==1:
					stepwidth = float(currentLuminance) * float(exp1factor)	
					#if stepwidth < 0.005:
					#	stepwidth = stepwidth + 0.001
					stepwidth += verschiebungY
				if experimental==2:
					stepwidth = float(steps) / ((currentLuminance - colorTargetLuminance)*exp2factor)		
				nextLuminance = currentLuminance - stepwidth
				print stepwidth
				print nextLuminance
				if(nextLuminance < colorTargetLuminance):
					nextLuminance = colorTargetLuminance	
				printLuminance = float(nextLuminance)/steps
				switch_leds(colorPin, printLuminance)
				currentLuminance = nextLuminance
		switch_leds(colorPin, float(colorTargetLuminance) / steps)
		currentLuminance = colorTargetLuminance
		currentLuminances[colorPin] = currentLuminance # update currentLuminance
		print "targetLuminance: "
		print colorTargetLuminance
elif int(fade) == 2: # Fadel-Level 2: gleichzeitig Faden
	print "Fadelevel 2"
	for step in range(0, steps):
		for color in range(0, len(pins)):
			colorPin = pins[color] # pin for the current color
			colorTargetLuminance = float(targetLuminances[colorPin]) # targetLuminance for the current color
			currentLuminance = currentLuminances[colorPin]
#			print "c: " + str(color) + " target: " + str(colorTargetLuminance) + " current: " + str(currentLuminance)
			if int(colorTargetLuminance) == -10:
				continue # abbrechen. -1 (* 10) ist Zeichen, um nichts zu verändern
			##
			if currentLuminance < colorTargetLuminance: # = hochfaden
				if experimental==1:
					stepwidth = float(currentLuminance-currentLuminances[colorPin]) * float(exp1factor)	
					if stepwidth < 0.005:
						stepwidth = stepwidth + 0.001
					stepwidth += verschiebungY
				if experimental==2:
					stepwidth = float(steps) / ((colorTargetLuminance - currentLuminance)*exp2factor)		
				nextLuminance = currentLuminance + stepwidth
			elif currentLuminance > colorTargetLuminance: # = runterfaden
				if experimental==1:
					stepwidth = float(currentLuminance) * float(exp1factor)	
					#if stepwidth < 0.005:
					#	stepwidth = stepwidth + 0.001
					stepwidth += verschiebungY
				if experimental==2:
					stepwidth = float(steps) / ((colorTargetLuminance - currentLuminance)*exp2factor)		
				nextLuminance = currentLuminance - stepwidth
			elif currentLuminance == colorTargetLuminance:
				continue
			switch_leds(colorPin, float(nextLuminance) / steps)
			currentLuminance = nextLuminance
			currentLuminances[colorPin] = currentLuminance # update currentLuminance			
	
			
pickle.dump(currentLuminances, open(filename, "wb")) # and dump them
