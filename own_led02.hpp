#ifndef _own_led02_hpp_
#define _own_led02_hpp_

#include <iostream>
#include <cstdlib>
#include <pigpio.h>
#include <stdio.h>
#include <string.h>

#define PWM_CONFIG 0  //0 to config via #define; 1 to config with cli
//#define ONE_PIN_INTERACTIVE //not working anymore, use old version if necessary 

#define GPIO_PIN 17 //not used anymore

//************* PWM CONFIG ***********************
// default sample rate is 5 -> 5us per step
// pwm real range (n of steps) is ((1/PWM_FREQUENCY) * 1'000'000) / SAMPLE_RATE
// examples: 	FREQUENCY=200Hz,	T=5000us, 	RANGE=1000
//		FREQUENCY=500Hz, 	T=2000us, 	RANGE=400
//200hz and 1000steps is probably a good setting
//alternative: 255 steps (=8bit-rgb mixing)
//		2550 steps (=8-bit w/better fade) BUT low frequency or change sample rate (currently not possible

#define PWM_RANGE 1000
#define PWM_FREQUENCY 200

//currently interactive value
#define FADE_DELAY_US 1000

#define SIMULTANEOUS_DELAY_FACTOR 3 //factor to multiply the delay in simultaneous fade mode

#define COLORS 4 //number of different leds, currently wrgb, maybe soon w/ autodetect



//******************* VARIABLES ****************************

//pins		w, r, g, b
extern int pins[4];
extern uint16_t targetBrightness[4];
extern uint16_t currentBrightness[4];
extern int fadeAlgorithm;
extern int realPWMrange;
extern int PWMrange;
extern int fadeDelayUs;


//**************** FUNCTIONS ********************************
bool initGeneral(void); //initializes the libary
bool initPins(uint16_t mode); //initializes all pins
bool initPin(int pin, uint16_t mode); //initializes all pins
void fadeSuccessively(uint16_t delay, uint16_t targetBrightness[]);
void fadeSimultaneous(uint16_t delay, uint16_t targetBrightness[]);
void fadeDirectly(uint16_t targetBrightness[]);

#endif
