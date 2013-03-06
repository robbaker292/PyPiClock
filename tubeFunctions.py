import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

#BCM pins
#PINS = [4,7,8,9,10,11,17,18,21,22]

#Raspberry Pi Pins
#PINS = [7,26,24,21,19,23,11,12,13,15]

#PWM Pins
PINS = [4,17,18,21,22,23,24,10,9,25,11,8,9]

#Setup each pin as an input
for p in PINS:
	#GPIO.setup(p, GPIO.OUT)
	GPIO.setup(p, GPIO.OUT, pull_up_down=GPIO.PUD_OFF)
GPIO.setup(24, GPIO.OUT, pull_up_down=GPIO.PUD_OFF)

#Ouput a particular Digit
def outputDigit(digit):
	#Create an array containing all pins but the one needed
	#localPins = PINS[:digit] + PINS[digit+1:]
	#for pin in localPins:
	#	#set pin low
	#	GPIO.output(pin, False)
	#	#print (pin, False),
	off()
	#Set the needed pin high
	GPIO.output(PINS[digit], True)
	#print (PINS[digit], "True")


#Switch off all pins
def off():
	for pin in PINS:
		#set low
		GPIO.output(pin, False)


#Loop through all digits in order with wait gap between digits & for iteration number times
def loopDigits(wait, iterations):
	i= 0
	while i < iterations:
		for n in range(10):
			outputDigit(n)
			time.sleep(wait)
		i = i + 1

#Switch on or off the backlight
def ledStatus(status):
	if status:
		GPIO.output(24, True)
	else:
		GPIO.output(24, False)

#Sets some shorthand for terminal commands
od=outputDigit
ld=loopDigits
